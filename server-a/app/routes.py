from fastapi import APIRouter
from typing import List
import os
import requests
from app.schemas import Item    # adjust import if needed
from app.services import validate_and_split_ips, fetch_geolocation_data, format_geolocation_results

router = APIRouter()


SERVER_B_HOST = os.getenv("SERVER_B_HOST","server-b")
SERVER_B_PORT = os.getenv("SERVER_B_PORT","8000")  
SERVER_B_TIMEOUT = int(os.getenv("SERVER_B_TIMEOUT","5"))

DESTINATION_URL = f"http://{SERVER_B_HOST}:{SERVER_B_PORT}/list-ip-from-server-a"

@router.post("/geolocations")
def process_and_forward_ips(list_ip: List[Item]):
    """
    Receive list of IPs from client, call external geolocation,
    clean results, then send coordinates to Service B.
    """
    # 1. Convert Pydantic models to dicts
    raw_ip_data = [ip.model_dump(mode="json") for ip in list_ip]

    # 2. Filter/clean IPs
    invalid_ip, valid_ip = validate_and_split_ips(raw_ip_data)

    # 3. Call external IP geolocation service for each valid IP
    geo_response = [fetch_geolocation_data(ip["ip"]) for ip in valid_ip]

    # 4. Clean response into final structures
    processed_details, failures, http_errors = format_geolocation_results(geo_response)

    # 5. Send to Service B's /list-ip-from-server-a endpoint
    try:
        resp = requests.post(DESTINATION_URL, json=processed_details, timeout=SERVER_B_TIMEOUT)
        resp.raise_for_status()
        server_b_result = resp.json()
    except requests.exceptions.Timeout:
        server_b_result = {"error": "Server B is taking too long to respond"}
    except requests.exceptions.ConnectionError:
        server_b_result = {"error": "Could not connect to Server B. Check Service name/DNS"}
    except requests.exceptions.HTTPError as err:
        server_b_result = {"error": f"Server B returned an error: {err.response.status_code}"}
    except Exception as exc:
        server_b_result = {"error": f"Unexpected error: {str(exc)}"}
    # 6. Return combined result to the client
    return {
        "wrong_ip": invalid_ip,
        "right_ip": valid_ip,
        "details_ip": processed_details,
        "no_details_on_ip": failures,
        "http_fail": http_errors,
        "server_b_result": server_b_result,
    }


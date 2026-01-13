# server-a/app/routes.py
from fastapi import APIRouter
from typing import List
import os
import requests

from app.schemas import Item    # adjust import if needed
from app.services import clean_wrong_ip, get_info_ip, clean_response

router = APIRouter()

# Service B URL
SERVICE_B_URL = os.getenv(
    "SERVICE_B_URL",
    "http://server-b:8000/list-ip-from-server-a",  
)


@router.post("/ip")
def insert_ip(list_ip: List[Item]):
    """
    Receive list of IPs from client, call external geolocation,
    clean results, then send coordinates to Service B.
    """
    # 1. Convert Pydantic models to dicts
    ip_addresses = [ip.model_dump(mode="json") for ip in list_ip]

    # 2. Filter/clean IPs
    wrong_ip, right_ip = clean_wrong_ip(ip_addresses)

    # 3. Call external IP geolocation service for each valid IP
    response = [get_info_ip(ip["ip"]) for ip in right_ip]

    # 4. Clean response into final structures
    details_ip, no_details, http_fail = clean_response(response)

    # 5. Send to Service B's /list-ip-from-server-a endpoint
    try:
        resp = requests.post(SERVICE_B_URL, json=details_ip, timeout=5)
        resp.raise_for_status()
        server_b_result = resp.json()
    except Exception as exc:
        server_b_result = {"error": str(exc)}

    # 6. Return combined result to the client
    return {
        "wrong_ip": wrong_ip,
        "right_ip": right_ip,
        "details_ip": details_ip,
        "no_details_on_ip": no_details,
        "http_fail": http_fail,
        "server_b_result": server_b_result,
    }


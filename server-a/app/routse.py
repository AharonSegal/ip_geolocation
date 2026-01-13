from fastapi import APIRouter
import requests
from schemas import  IPModel, Item
from pydantic import TypeAdapter, ValidationError

router = APIRouter()
IP_API_ADDRESS = "http://ip-api.com/json/"
FIELDES = "?fields=status,message,lat,lon,query"

@router.post("/ip")
def insert_ip(list_ip : list[Item]):
    ip_addresses = [ip.model_dump(mode='json') for ip in list_ip]
    ip_category = clean_wrong_ip(ip_addresses)
    wrong_ip = ip_category[0]
    right_ip = ip_category[1]
    
    response = [get_info_ip(ip['ip']) for ip in right_ip]
    
    details_ip , no_details = clean_response(response)
    
    # insert_to_database(details_ip)
    return {'wrong ip':wrong_ip,'right ip':right_ip,'no details on ip':no_details}

def clean_response(ip_addresses:list[dict]):
    ip_with_detalis = ip_addresses.copy()
    ip_no_details = ip_addresses.copy()
    for ip in ip_addresses:
        if ip['status'] =='fail' or not valdation_coordinates(ip['lot'],ip['lat']):
            ip_with_detalis.remove(ip)
        else:
            ip_no_details.remove(ip)
    return ip_with_detalis, ip_no_details


def valdation_coordinates(lon:float,lat:float)->bool:
    if lon > 180 or lon < -180:
        return False
    if lat > 90 or lat < -90:
        return False
    return True


def validation_http(response:list|dict):
    if isinstance(response,dict):
        if response.get('error'):
            return {'massege':'http fail','detals':response}
    

def validation_ip(ip:dict):
    adapter = TypeAdapter(IPModel)
    try: 
 
        validated_data = adapter.validate_python(ip)
        
        return validated_data.model_dump(mode='json')
    except ValidationError as e:
        return {"ip": ip, "error": 'not valid ip'}


def get_info_ip(ip:str):
    try:
        response = requests.get(IP_API_ADDRESS + ip + FIELDES)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        return {"error":e}


def insert_to_database(data:list):
    requests.post()

def clean_wrong_ip(ip_addresses:list[dict]) -> tuple[list]:
    validated_ips = [validation_ip(ip) for ip in ip_addresses]
    wrong_ip = []
    right_ip = []
    for ip in validated_ips:
        if ip.get('error'):
            wrong_ip.append(ip)
        else:
            right_ip.append(ip)
    return wrong_ip, right_ip



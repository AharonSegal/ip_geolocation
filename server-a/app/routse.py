from fastapi import APIRouter
import requests
from schemas import  IPModel, Item
from pydantic import TypeAdapter, ValidationError


IP_API_ADDRESS = "http://ip-api.com/json/"
FIELDES = "?fields=status,message,lat,lon,query"

router = APIRouter()


@router.post("/ip")
def insert_ip(list_ip : list[Item]):
    ip_addresses = [ip.model_dump(mode='json') for ip in list_ip]
    wrong_ip ,right_ip = clean_wrong_ip(ip_addresses)
    
    response = [get_info_ip(ip['ip']) for ip in right_ip]
    
    details_ip , no_details = clean_response(response)
    
    # insert_to_database(details_ip)
    #TODO: INN=TEGRATE TO SERVER-B
    return {'wrong ip':wrong_ip,'right ip':right_ip,'details ip':details_ip,'no details on ip':no_details}


def clean_response(ip_addresses:list[dict]):
    ip_with_detalis = []
    ip_no_details = []
    for ip in ip_addresses:
        if ip['status'] =='fail' or not valdation_coordinates(ip['lon'],ip['lat']):
            ip_no_details.append(ip)
        else:
            new_ip = {'ip':ip['query'],'coordinates':{ "latitude": ip['lat'], "longitude": ip['lon']}}
            ip_with_detalis.append(new_ip)
    return ip_with_detalis, ip_no_details


def valdation_coordinates(lon:float,lat:float)->bool:
    # TODO: consider pydantic convertion
    if lon > 180 or lon < -180:
        return False
    if lat > 90 or lat < -90:
        return False
    return True


def validation_http(response:list|dict):
    # TODO: check for helth endpoint
    if isinstance(response,dict):
        if response.get('error'):
            return {'massege':'http fail','detals':response}
    

def validation_ip(ip:dict):
    adapter = TypeAdapter(IPModel)
    try: 
        validated_data = adapter.validate_python(ip)
        return validated_data.model_dump(mode='json')
    except ValidationError:
        return {"ip": ip, "error": 'not valid ip'}


def get_info_ip(ip:str):
    try:
        response = requests.get(IP_API_ADDRESS + ip + FIELDES)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        return {"error":e}


def insert_to_database(data:list):
    # TODO: HERE IS THE SERVE-1 IMPLEMENTATION
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



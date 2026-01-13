from fastapi import APIRouter
from schemas import   Item
from services import *


router = APIRouter()


@router.post("/ip")
def insert_ip(list_ip : list[Item]):
    
    ip_addresses = [ip.model_dump(mode='json') for ip in list_ip]
    wrong_ip ,right_ip = clean_wrong_ip(ip_addresses)
    
    response = [get_info_ip(ip['ip']) for ip in right_ip]
    details_ip , no_details, http_fail = clean_response(response)

    # insert_to_database(details_ip)
    #TODO: INN=TEGRATE TO SERVER-B
    
    return {'wrong ip':wrong_ip,'right ip':right_ip,'details ip':details_ip,'no details on ip':no_details, 'http fail':http_fail}







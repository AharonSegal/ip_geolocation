from fastapi import APIRouter, status 
from app.schemas import IpWithCoordinates, IpWithCoordinatesList
from app.storage import save_singe_ip_coordinates
from typing import List
import logging

"""
input example:
[
  {
    "ip": "1.1.1.1",
    "coordinates": { "latitude": 10.0, "longitude": 20.0 }
  },
  {
    "ip": "8.8.8.8",
    "coordinates": { "latitude": 30.0, "longitude": 40.0 }
  }
]
"""
# ---------------------------------------------------
# Logger init
# ---------------------------------------------------

logger = logging.getLogger("server-b.routes")

# ---------------------------------------------------
# Routs
# ---------------------------------------------------

router = APIRouter(tags=["Server-B endpoints"])

@router.get("/server-b-health")
def health_check():
    logger.debug("Health check endpoint called")
    return {"status": "ok"}

# send one ip to the DB
def post_single_ip(ip: IpWithCoordinates):
    """
    Receive a single IP + coordinates from Service A and store it in Redis.
    """
    # blue line for cli visuals
    print("\033[94m" + "=" * 40 + "\033[0m")
    logger.info("Received new IP from Service A: %s", ip.ip)
    logger.debug("Full request data: %s", ip.model_dump())

    # Pydantic has already validated basic structure + ranges at this point.
    save_singe_ip_coordinates(ip)

    logger.info("Finished handling IP %s", ip.ip)

    return {"message": "IP coordinates stored"}


# `POST` List_IP from Service 
@router.post(
    "/list-ip-from-server-a",
    status_code=status.HTTP_201_CREATED,
    summary="Store IP coordinates received from Service A",
)
def post_ip_list(raw_list: List[IpWithCoordinates]):
    """
    Receive a list IP + coordinates from Service A and store it in Redis.
    """
    # set raw list to Pydantic list model
    ip_list = IpWithCoordinatesList(items=raw_list)
    # green line for cli visuals
    print("\033[92m" + "=" * 40 + "\033[0m")
    logger.info("Received new IP list from Service A with %d item(s)", len(ip_list.items))
    logger.debug("Full request data: %s", ip_list.model_dump())

    # Pydantic has already validated basic structure + ranges at this point.
    for ip in ip_list.items:
      post_single_ip(ip)

    logger.info("Finished handling IP %s", ip_list.items)

    return {"message": "IP coordinates stored"}


# `GET` from User to retrieve stored coordinates
@router.get("/view-saved-ip")
def get_view_ip():
    ...

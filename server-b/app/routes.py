from fastapi import APIRouter, status 
from app.schemas import IpWithCoordinatesList, IpWithCoordinates
from app.storage import save_singe_ip_coordinates
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

# `POST` from Service A with coordinates to store
@router.post(
    "/single-ip-from-server-a",
    status_code=status.HTTP_201_CREATED,
    summary="Store IP coordinates received from Service A",
)
def get_new_ip_single(ip: IpWithCoordinates):
    """
    Receive a single IP + coordinates from Service A and store it in Redis.
    """
    logger.info("Received new IP from Service A: %s", ip.ip)
    logger.debug("Full request data: %s", ip.model_dump())

    # Pydantic has already validated basic structure + ranges at this point.
    save_singe_ip_coordinates(ip)

    logger.info("Finished handling IP %s", ip.ip)

    return {"message": "IP coordinates stored"}


# `GET` from User to retrieve stored coordinates
@router.get("/view-saved-ip")
def get_view_ip():
    ...

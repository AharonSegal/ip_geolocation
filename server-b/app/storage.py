from fastapi import FastAPI, HTTPException,APIRouter
import os
import redis
from typing import List
import logging

from app.schemas import IpWithCoordinates

# ---------------------------------------------------
# Logger init
# ---------------------------------------------------
logger = logging.getLogger("server-b.storage")

# ===================================================
# Redis connection config 
# ===================================================

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    decode_responses=True,  # get strings instead of bytes
)

# ===================================================
# Redis routs
# ===================================================

def save_singe_ip_coordinates(ip_data: IpWithCoordinates) -> None:
    """
    Store coordinates for a single IP in Redis.

    - Key:  ip_geolocation:ip:<ip>
    - Data: JSON representation of IpWithCoordinates
    """
    #extract ip to serve as the key
    key = str(ip_data.ip)

    # start log
    logger.debug("Preparing to save IP data to Redis: %s", ip_data.model_dump())
    logger.info("Saving IP %s to Redis with key '%s'", ip_data.ip, key)

    # Save the full object as JSON
    try:
        redis_client.set(key, ip_data.model_dump_json())
    except Exception as exc:
        logger.error("Error saving IP %s to Redis: %s", ip_data.ip, exc, exc_info=True)
        raise
    logger.info("Successfully saved IP %s to Redis", ip_data.ip)


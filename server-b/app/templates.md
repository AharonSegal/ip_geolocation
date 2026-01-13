# service-b/app/storage.py
import os
import json
from typing import List

import redis  # pip install redis

from .schemas import IpWithCoordinates

# Configure Redis connection from env, with sensible defaults
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    decode_responses=True,  # return str instead of bytes
)

# We keep a set of all IPs so we can list them later
ALL_IPS_SET_KEY = "ip_geolocation:all_ips"
IP_KEY_PREFIX = "ip_geolocation:ip:"


def _ip_key(ip: str) -> str:
    """Build the Redis key for a single IP."""
    return f"{IP_KEY_PREFIX}{ip}"


def save_ip_coordinates(ip_data: IpWithCoordinates) -> None:
    """
    Store coordinates for a single IP in Redis.

    - Key:  ip_geolocation:ip:<ip>
    - Data: JSON representation of IpWithCoordinates
    - Also track the IP in a set so we can list all saved IPs later.
    """
    ip_str = str(ip_data.ip)
    key = _ip_key(ip_str)

    # Save the full object as JSON
    redis_client.set(key, ip_data.model_dump_json())

    # Track the IP in a set
    redis_client.sadd(ALL_IPS_SET_KEY, ip_str)


def get_all_ip_coordinates() -> List[IpWithCoordinates]:
    """
    Read all stored coordinates from Redis and return them as Pydantic models.
    """
    ips = redis_client.smembers(ALL_IPS_SET_KEY)
    results: List[IpWithCoordinates] = []

    for ip_str in ips:
        key = _ip_key(ip_str)
        raw = redis_client.get(key)
        if not raw:
            # If key is missing but IP is in set, skip it
            continue
        data = json.loads(raw)
        # Re-validate into Pydantic model (safety + consistent shape)
        results.append(IpWithCoordinates.model_validate(data))

    return results



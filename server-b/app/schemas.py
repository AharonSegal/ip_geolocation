from pydantic import BaseModel, Field, IPvAnyAddress
from typing import List

class Coordinates(BaseModel):
    # latitude must be between -90 and 90 (inclusive)
    latitude: float = Field(
        ...,
        ge=-90,  
        le=90,   
        description="Latitude in decimal degrees, between -90 and 90",
    )
    # longitude must be between -180 and 180 (inclusive)
    longitude: float = Field(
        ...,
        ge=-180,
        le=180,
        description="Longitude in decimal degrees, between -180 and 180",
    )

class IpWithCoordinates(BaseModel):
    ip: IPvAnyAddress
    coordinates: Coordinates

class IpWithCoordinatesList(BaseModel):
    items: List[IpWithCoordinates]


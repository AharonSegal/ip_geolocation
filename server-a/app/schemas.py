from pydantic import BaseModel, HttpUrl
from pydantic.networks import IPvAnyAddress


class IPModel(BaseModel):
    ip:IPvAnyAddress

class URLModel(BaseModel):
    url:HttpUrl

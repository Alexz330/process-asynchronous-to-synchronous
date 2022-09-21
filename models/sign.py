from pickletools import bytes1
from pydantic import BaseModel,constr
from typing import Optional,List
class Sign_model(BaseModel):
    username: str
    password: str
    pin: str
    format: str
    billing_username: str
    billing_password: str
    file_in: List[bytes]
    url_out: str
    urlback: str
    level: str
    env: str

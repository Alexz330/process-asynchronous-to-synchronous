from pickletools import bytes1
from pydantic import BaseModel,constr
from typing import Any, Dict, Optional,List
class Sign_model(BaseModel):
    username: str
    password: str
    pin: str
    format: str
    billing_username: str
    billing_password: str
    img:str
    paragraph_format:str
    img_size:str
    position:str
    npage:str
    reason:str
    location:str
    file_in: List[Dict]
    url_out: str
    urlback: str
    level: str
    env: str

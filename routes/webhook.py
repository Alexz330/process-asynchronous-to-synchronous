
from fastapi import APIRouter, Request
import base64
import json


webhook = APIRouter()
result_setted = {
    "result": False,
    "services": False
}

state = {
    "id_transaccion": "",
    "firmado": False,
    "documento_base64": ""
}


@webhook.post("/result")
async def get_document(req: Request):
    global result_setted
    data = await req.body()
    state["documento_base64"] = base64.b64encode(data)
    state["firmado"] = True
    result_setted['result'] = True


@webhook.post("/services")
async def save_log_document(req: Request):
    doc =  await req.body()
    result_setted['services'] = True
    data:str = str(await req.body())
    log = data.split("id")
    id = log[1][1:]
    print(id)
    state["id_transaccion"] = id
    return ""
    

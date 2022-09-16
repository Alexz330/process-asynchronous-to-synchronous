
from fastapi import APIRouter, Request
import base64


webhook = APIRouter()
result_setted = {
    "result": False
}

state = {
    "sing": False,
    "document": ""
}


@webhook.post("/result")
async def get_document(req: Request):
    global result_setted
    data = await req.body()
    state["document"] = base64.b64encode(data)
    state["sing"] = True
    result_setted['result'] = True
    print("event seted")


@webhook.post("/services")
async def get_document(req: Request):
    doc = await req.body()
    print(doc)

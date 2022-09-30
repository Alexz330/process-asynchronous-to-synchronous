from fastapi import APIRouter, Request
import base64
import asyncio

from src.models.sign import Sign_model
from src.services.Sign import Sing

sign = APIRouter()
sign_services = Sing()


@sign.post("/sign")
async def sign_request(sign: Sign_model):
    return await sign_services.sign_document(sign)


@sign.post("/sign/result/{uuid}")
async def get_document(req: Request, uuid):

    # await asyncio.sleep(3)
    data = base64.b64encode(await req.body())
    await sign_services.get_document(data,uuid)
    return ""

@sign.post("/sign/log/{uuid}")
async def get_logs(req: Request, uuid):
    # await asyncio.sleep(3)
    log: bytes = await req.body()
    await sign_services.get_logs(log, uuid)
    return""
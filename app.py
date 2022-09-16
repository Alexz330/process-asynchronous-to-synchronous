from re import S
from fastapi import FastAPI
from routes.webhook import webhook, state, result_setted
import requests
import asyncio
import aiohttp
# import time


app = FastAPI()

app.include_router(webhook)


@app.get("/")
async def hello():
    global result_setted
    resArray = []
    data = {
        "username": "5192351",
        "password": "J94:VqDt",
        "pin": "abc123**",
        "format": "pades",
        "billing_username": "ccg@ccg",
        "billing_password": "D6eXbdSJ",
        "check": "0",
        "url_in": "https://uanataca.pythonanywhere.com/sample.pdf",
        "url_out": "http://192.168.11.5:8000/result",
        "urlback": "http://192.168.11.5:8000/services",
        "level": "BES",
        "env": "test",
        "identifier": "DS0"

    }
    for i in range(10):
        print(i)
        async with aiohttp.ClientSession() as session:
            async with session.post('http://192.168.1.61/api/sign', data=data) as response:
                await asyncio.sleep(0.5)

                id = await response.text()
                print(id)
                # state["id_transaccion"] = str(id)[3:]

    # WAIT FOR RESULT WEBHOOK
    for i in range(10):
        print(i)
        state["documento_base64"] = ""
        state["firmado"] = False
        state["id_transaccion"] = ""
        print("Call webhook")

        print(state)
        while True:

            if ((result_setted['result'] and result_setted['services']) or (result_setted["services"])):
                print("webhook visitado")
                current_status = state.copy()

                resArray.append(current_status)

                break
            else:
                await asyncio.sleep(0.0005)

        result_setted['result'] = False
        result_setted['services'] = False

    print("Proceso")
    return {"data": resArray}

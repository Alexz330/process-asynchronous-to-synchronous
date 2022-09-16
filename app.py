from fastapi import FastAPI
from routes.webhook import webhook, state, result_setted
# import requests
import asyncio
import aiohttp
# import time


app = FastAPI()

app.include_router(webhook)


@app.get("/")
async def hello():
    global result_setted
    data = {
        "username": "5192351",
        "password": "J94:VqDt",
        "pin": "abc123**",
        "format": "pades",
        "billing_username": "ccg@ccg",
        "billing_password": "D6eXbdSJ",
        "check": "0",
        "url_in": "https://uanataca.pythonanywhere.com/sample.pdf",
        "url_out": "http://192.168.0.101:8000/result",
        "urlback": "http://192.168.0.101:8000/services",
        "level": "BES",
        "env": "test",
        "identifier": "DS0"

    }

    async with aiohttp.ClientSession() as session:
        async with session.post('http://192.168.0.14/api/sign', data=data) as response:
            id = await response.text()
            print("Call webhook")

            # WAIT FOR RESULT WEBHOOK
            while True:
                if result_setted['result']:
                    break
                else:
                    await asyncio.sleep(0.01)
                    

            return state

    # res = requests.post('http://192.168.0.14/api/sign',data)
    # time.sleep(1)
    # print(res)
    # print(state)#
    # return state

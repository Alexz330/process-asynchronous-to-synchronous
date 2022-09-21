import asyncio
import json
import time
from uuid import uuid4

import aiohttp
import json
from models.sign import Sign_model


class Sing:

    def __init__(self) -> None:
        self.res = {
            "id": "",
            "uuid": "",
            "firmado": False,
            "errores": [],
            "documento_base64": ""
        }
        self.resList = []
        self.state_webhooks = {
            "log": False,
            "sign": False
        }

    async def sign_document(self, payload: Sign_model):

        for document in payload.file_in:
            uuid_system = uuid4()

            data = {

                "username": payload.username,
                "password": payload.password,
                "pin": payload.pin,
                "format": payload.format,
                "billing_username": payload.billing_username,
                "billing_password": payload.billing_password,
                "check": "0",
                "file_in": document.decode(),
                "url_out": payload.url_out+"/"+str(uuid_system),
                "urlback": payload.urlback+"/"+str(uuid_system),

                "level": payload.level,
                "version": "v1",
                "detached": "0",
                "env": payload.env,
                "identifier": "DS0"

            }
            data_json = json.dumps(data)

            async with aiohttp.ClientSession(headers={"content-type": "application/json"}) as session:

                async with session.post('http://192.168.1.61/api/sign', data=data_json) as response:
                    id = await response.text()
                    print("---------------------------")
                    print(uuid_system)
                    print(id)
                    print("---------------------------")

        # WAIT FOR RESULT WEBHOOK
        for _ in range(len(payload.file_in)):

            while True:

                if ((self.state_webhooks['sign'] and self.state_webhooks['log']) or (self.state_webhooks["log"])):
                    current_status = self.res.copy()
                    self.res["documento_base64"] = ""
                    self.res["firmado"] = False
                    self.res["uuid"] = ""
                    self.res["errores"] = []

                    self.resList.append(current_status)

                    print("---------------IM HERE----------------")
                    break

                else:

                    await asyncio.sleep(3)

            self.state_webhooks['sign'] = False
            self.state_webhooks['log'] = False
        list_Document_res = self.resList.copy()
        self.resList = []
        return list_Document_res

    async def get_document(self, d_base64, uuid) -> None:
 

        self.res["documento_base64"] = d_base64

        self.res["firmado"] = True
        self.state_webhooks['sign'] = True

    async def get_logs(self, log, uuid) -> None:
   
        text_log = log.decode()
        log_dict = json.loads(text_log)
        self.res["uuid"] = uuid
        self.res["id"] = log_dict["id"]
        try:
            if (log_dict["message"]):
                self.res["errores"].append(log_dict["message"])
        except:
            pass
        self.state_webhooks['log'] = True

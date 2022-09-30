import asyncio
import json
import re
import time
from uuid import uuid4

import aiohttp
import json
from src.models.sign import Sign_model


class Sing:
    def __init__(self) -> None:
        self.res = {
            "id": "",
            "uuid": "",
            "firmado": False,
            "errores": [],
            "documento_base64": ""
        }
        self.list_documents_signed = []
        self.list_logs_documents = []
        # self.state_webhooks = {
        #     "log": False,
        #     "sign": False
        # }

    async def sign_document(self, payload: Sign_model):
        print(len(payload.file_in))
        for document in payload.file_in:
          

            data = {

                "username": payload.username,
                "password": payload.password,
                "pin": payload.pin,
                "format": payload.format,
                "billing_username": payload.billing_username,
                "billing_password": payload.billing_password,
                "check": "0",
                "file_in": document["documento"],
                "url_out": payload.url_out+"/"+str(document["id"]),
                "urlback": payload.urlback+"/"+str(document["id"]),
                "img": payload.img,
                "img_size": payload.img_size,
                "position": payload.position,
                "npage": payload.npage,
                "reason": payload.reason,
                "location": payload.location,
                "level": payload.level,
                "paragraph_format": payload.paragraph_format.replace("'", '"'),
                "env": payload.env,

            }
            
            data_json = json.dumps(data)

            async with aiohttp.ClientSession(headers={"content-type": "application/json"}) as session:
                time.sleep(0.5)
                async with session.post('http://192.168.1.62/api/sign', data=data_json) as response:
                    id = await response.text()
                    print("---------------------------")
                    print(id)
                    print("---------------------------")

        # WAIT FOR RESULT WEBHOOK
        # for i in range(len(payload.file_in)):
        # for i in range(len(payload.file_in)):
        #     time_wait = 0.01*len(payload.file_in)*i
        #     print(time)
        #     await asyncio.sleep(time_wait)

        while True:
            await asyncio.sleep(1)
            print(f"espedando validacion tamaño de lista de logs {str(len(self.list_logs_documents))}")      
            if len(payload.file_in) == len(self.list_logs_documents):       
                break

        list_Document_res = self.list_documents_signed.copy()
        self.list_documents_signed = []
        list_log_res = self.list_logs_documents.copy()
        self.list_logs_documents = []
        return {"no.documentos_enviados": len(payload.file_in), "no.documentos_firmados": len(list_Document_res), "logs": list_log_res, "documentos_firmados": list_Document_res}

    async def get_document(self, d_base64, uuid) -> None:
        self.list_documents_signed.append(
            {"uuid": uuid, "documento_base64": d_base64})

    async def get_logs(self, log, uuid) -> None:
        log_dict = json.loads(log)

        message_error = log_dict["message"]
        validation_error = re.search("(ProcessTerminated)", message_error)
        if validation_error is not None:

            data = {
                "firmado": True,
                "uuid": uuid,
                "id": log_dict["id"],
                "errores": ""
            }
            self.list_logs_documents.append(data)
        elif validation_error is None:
            data = {
                "firmado": False,
                "uuid": uuid,
                "id": log_dict["id"],
                "errores": log_dict["message"]
            }
            self.list_logs_documents.append(data)

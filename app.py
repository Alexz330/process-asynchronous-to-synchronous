from fastapi import FastAPI
import uvicorn
from routes.sign import sign


app = FastAPI()

app.include_router(sign)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
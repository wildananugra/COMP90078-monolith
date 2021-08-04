from typing import Optional
from fastapi import FastAPI, Header, Request
import json

app = FastAPI()

@app.post("/sim/{merchant_path}")
async def root(request: Request, action: Optional[str] = Header(None)):
    print(f"action: {request.headers['Action']}")

    action = request.headers['Action']
    merchant_path = request.path_params['merchant_path']

    output = ""
    with open(f"{merchant_path}/{action}.json",'r') as f:
        output = f.read()
    return json.loads(output)
import uvicorn
import logging
import os, sys
import uuid
from pydantic import BaseModel

from fastapi import FastAPI, Depends, Request, Header, APIRouter

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

app = FastAPI()

@app.get("/chat")
async def _chat(request: Request, authorization = Header(default=None)) -> dict:
    return {}

if __name__ == '__main__':
    options = {
        'port': 8080,
        'workers': 1,
        'host': '0.0.0.0',
        'reload': True,
    }
    uvicorn.run("main:app", **options)

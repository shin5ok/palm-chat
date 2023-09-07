import uvicorn
import logging
import os, sys
import uuid
from pydantic import BaseModel
from fastapi import FastAPI, Depends, Request, Header, APIRouter
from routers import chat
import common

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

app = FastAPI()
llm = None

app.include_router(
        chat.routers,
        prefix="/chat",
        # dependencies=[Depends(common.get_llm)]
    )

if __name__ == '__main__':
    options = {
        'port': 8080,
        'workers': 2,
        'host': '0.0.0.0',
        'reload': True,
    }
    uvicorn.run("main:app", **options)

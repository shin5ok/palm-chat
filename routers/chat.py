import sys
from fastapi import FastAPI, Depends, Header, Request, APIRouter, Response
from pydantic import BaseModel, Field, EmailStr
import logging

import common

app = FastAPI()

routers = APIRouter()

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

class Message(BaseModel):
    text: str

class RequestBody(BaseModel):
    message: Message

@routers.post("/google_chat")
def _google_chat(body: RequestBody, request: Request, authorization = Header(default=None), chat_model = Depends(common.get_llm), project = Depends(common.project)):
    if not common.verify_id_token(project['number'], authorization):
        return Response("Invalid Token", 403)
    return chat_model.predict(input=str(body.message))

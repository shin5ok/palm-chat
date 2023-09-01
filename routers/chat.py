import sys
from fastapi import FastAPI, Depends, Header, Request, APIRouter
from pydantic import BaseModel, Field, EmailStr
import logging

from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

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
def _google_chat(body: RequestBody, request: Request, authorization = Header(default=None), chat_model = Depends(common.get_llm)):
    return chat_model.predict(input=str(body.message))

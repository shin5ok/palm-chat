import sys
from typing import Annotated, Optional, List
from fastapi import FastAPI, Depends, Header, Request, APIRouter, Response, Body
from pydantic import BaseModel, Field, EmailStr
import logging
import common
from storategy import GoogleChat, Slack

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

    v = GoogleChat(project)
    v.validation(authorization)

    return v.say(str(body.message))


class SlackRequest(BaseModel):
    team_id: str
    token: str
    text: str

@routers.post("/slack")
def _slack(slack_request: SlackRequest, chat_model = Depends(common.get_llm), project = Depends(common.project)):

    print(slack_request.model_dump())
    v = Slack(project)
    print(slack_request.text)
    return v.say(str(slack_request.text))

@routers.post("/slack2")
def _slack2(body: str = Body(embed=False), authorization = Header(default=None), chat_model = Depends(common.get_llm), project = Depends(common.project)):
    return body


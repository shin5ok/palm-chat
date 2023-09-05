import sys
from typing import Annotated, Optional, List
from fastapi import FastAPI, Depends, Header, Request, APIRouter, Response, HTTPException, Body
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


@routers.post("/slack")
def _slack(body: str = Body(embed=False), authorization = Header(default=None), chat_model = Depends(common.get_llm), project = Depends(common.project)):
    import os
    import urllib

    config = dict(token=os.environ.get("SLACK_TOKEN"))
    v = Slack(project, config)
    p = urllib.parse.parse_qs(body)

    if p['user_name'][0] == 'slackbot':
        raise HTTPException(status_code=204, detail="slackbot")

    v.validation(p['token'])

    gen_message = v.say(str(p['text'][0]))

    return gen_message

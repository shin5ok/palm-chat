import sys
from typing import List
from fastapi import FastAPI, Depends, Header, Request, APIRouter, HTTPException, Body
from pydantic import BaseModel, EmailStr
import logging
import common
from storategy import GoogleChat, Slack, Test

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


@routers.post("/justtestapi")
async def _test(body: RequestBody, request: Request, authorization = Header(default=None), chat_model = Depends(common.get_llm), project = Depends(common.project)):

    if request.client.host != "127.0.0.1":
        raise HTTPException(status_code=403, detail="This api is allowed only from localhost")

    logger.info(str(body.message))
    v = Test(project)
    return v.say(str(body.message))

@routers.post("/google_chat")
async def _google_chat(body: RequestBody, request: Request, authorization = Header(default=None), chat_model = Depends(common.get_llm), project = Depends(common.project)):

    v = GoogleChat(project)
    v.validation(authorization)

    return v.say(str(body.message))


@routers.post("/slack")
async def _slack(body: str = Body(embed=False), authorization = Header(default=None), chat_model = Depends(common.get_llm), project = Depends(common.project)):
    import os
    from urllib import parse

    config = dict(token=os.environ.get("SLACK_TOKEN"))
    v = Slack(project, config)
    p = parse.parse_qs(body)

    if p['user_name'][0] == 'slackbot':
        raise HTTPException(status_code=204, detail="slackbot")

    v.validation(str(p['token']))

    gen_message = v.say(str(p['text'][0]))
    return gen_message

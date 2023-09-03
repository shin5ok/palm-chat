from abc import ABCMeta, abstractmethod
import logging
import common
from fastapi import HTTPException

class ChatContext(metaclass=ABCMeta):

    def __init__(self, project: dict):
        self.project_number = project['number']
        self.project_id = project['id']

    @abstractmethod
    def validation() -> None:
        ...
    
    @abstractmethod
    def say() -> str:
        ...
    
    def predict(self, message) -> str:
        chat_model = common.get_llm()
        gen_message = chat_model.predict(input=message)
        return gen_message


class GoogleChat(ChatContext):

    def validation(self, authorization: str) -> None:
        from oauth2client import client

        audience = self.project_number
        chat_issuer = 'chat@system.gserviceaccount.com'
        public_cert_url_prefix = 'https://www.googleapis.com/service_accounts/v1/metadata/x509/'

        token = str(authorization.split(" ")[1])
        logging.debug(token)

        try:
            t = client.verify_id_token(token, audience, cert_uri=public_cert_url_prefix + chat_issuer)

            if t['iss'] != chat_issuer:
              raise HTTPException(status_code=403, detail="Invalid issuer")

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def say(self, message: str) -> dict:
        return dict(text=self.predict(message))

class Slack(ChatContext):
    
    def validation(self, token: str) -> None:
        should_be_token = "..."
        token = should_be_token
        if token == should_be_token:
            raise HTTPException(status_code=403, detail="Invalid token")
        ...
    
    def say(self, message: str) -> dict:
        from slack_sdk.webhook import WebhookClient
        webhook = "https://..."
        WebhookClient(webhook).send(text=self.predict(message))
        return {}

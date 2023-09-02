from abc import ABCMeta, abstractmethod
import logging
import common

class ChatContext(metaclass=ABCMeta):

    def __init__(self, project: dict):
        self.project_number = project['number']
        self.project_id = project['id']

    @abstractmethod
    def validation() -> bool:
        ...
    
    @abstractmethod
    def say() -> str:
        ...
    
    def predict(self, message) -> str:
        chat_model = common.get_llm()
        gen_message = chat_model.predict(input=message)
        return gen_message


class GoogleChat(ChatContext):

    def validation(self, authorization: str) -> bool:
        from oauth2client import client

        audience = self.project_number
        chat_issuer = 'chat@system.gserviceaccount.com'
        public_cert_url_prefix = 'https://www.googleapis.com/service_accounts/v1/metadata/x509/'

        token = str(authorization.split(" ")[1])
        logging.debug(token)

        try:
            t = client.verify_id_token(token, audience, cert_uri=public_cert_url_prefix + chat_issuer)

            if t['iss'] != chat_issuer:
              raise Exception('Invalid issuer')
        except Exception as e:
            print("Exception", e)
            return False
        return True

    def say(self, message: str) -> dict:
        return dict(text=self.predict(message))
 
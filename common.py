import os
from oauth2client import client

from langchain.chat_models import ChatVertexAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

llm = None
memory = ConversationBufferMemory()

parameters = {
            "temperature": 0.2,
            "max_output_tokens": 1024,
            "top_p": 0.8,
            "top_k": 40
        }

def get_llm() -> ConversationChain:
    global llm, memory
    if not llm:
        llm = ChatVertexAI(**parameters)
        print("generated llm")

    chat_model = ConversationChain(
        llm=llm,
        verbose=True,
        memory=memory,
    )

    return chat_model

def verify_id_token(project_number: int, authorization: str) -> bool:
    audience = project_number
    chat_issuer = 'chat@system.gserviceaccount.com'
    public_cert_url_prefix = 'https://www.googleapis.com/service_accounts/v1/metadata/x509/'

    token = str(authorization.split(" ")[1])

    try:
      t = client.verify_id_token(token, audience, cert_uri=public_cert_url_prefix + chat_issuer)

      if t['iss'] != chat_issuer:
        raise Exception('Invalid issuer')
    except Exception as e:
      print("Exception", e)
      return False

    return True


def project():
    return {
        'id': os.environ.get('GOOGLE_CLOUD_PROJECT'),
        'number': os.environ.get('PROJECT_NUMBER'),
    }

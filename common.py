import os
from oauth2client import client

from langchain.chat_models import ChatVertexAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

llm = None
memory = ConversationBufferMemory()

parameters = {
            "temperature": 0.6,
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

def project():
    return {
        'id': os.environ.get('GOOGLE_CLOUD_PROJECT'),
        'number': os.environ.get('PROJECT_NUMBER'),
    }

def is_debug():
    return "DEBUG" in os.environ

import os

from langchain.chat_models import ChatVertexAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

llm = None
memory = ConversationBufferMemory()
_debug: bool = 'DEBUG' in os.environ
default_model = 'chat-bison@002'

parameters = {
            "model_name": default_model,
            "temperature": 0.6,
            "max_output_tokens": 1024,
            "top_p": 0.8,
            "top_k": 40
        }

def get_llm() -> ConversationChain:
    global llm, memory, parameters
    if not llm:
        llm = ChatVertexAI(**parameters)
        print("Generating LLM instance")

    return ConversationChain(
        llm=llm,
        verbose=True,
        memory=memory,
    )

def project() -> dict:
    return {
        'id': os.environ.get('GOOGLE_CLOUD_PROJECT'),
        'number': os.environ.get('PROJECT_NUMBER'),
    }

def is_debug():
    return _debug

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

def get_llm():
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

from .bot import conversation
from .bot import persist_embeddings


def embedding():
    persist_embeddings()

def qa():
    conversation()

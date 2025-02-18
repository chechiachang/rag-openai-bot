from dotenv import find_dotenv
from dotenv import load_dotenv

from .bot import run_bot
from .tool import k8s_qa
from .tool import persist_embeddings


def embedding():
    load_dotenv(find_dotenv(raise_error_if_not_found=True, usecwd=True))

    persist_embeddings()

def qa():
    load_dotenv(find_dotenv(raise_error_if_not_found=True, usecwd=True))
    k8s_qa()

def bot():
    run_bot()

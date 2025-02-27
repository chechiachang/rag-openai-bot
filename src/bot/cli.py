from dotenv import find_dotenv
from dotenv import load_dotenv

from .slack_bot import start_bot as run_slack_bot
from .telegram_bot import run_bot as run_telegram_bot
from .tool import k8s_qa
from .tool import persist_embeddings


def embedding_k8s():
    load_dotenv(find_dotenv(raise_error_if_not_found=True, usecwd=True))
    persist_embeddings(data_path="data/kubernetes-docs/", collection_name="demo_collection")

def embedding_quip():
    load_dotenv(find_dotenv(raise_error_if_not_found=True, usecwd=True))
    persist_embeddings(data_path="data/quip/", collection_name="quip")

def qa():
    load_dotenv(find_dotenv(raise_error_if_not_found=True, usecwd=True))
    k8s_qa()

def run_telegram():
    run_telegram_bot()

def run_slack():
    run_slack_bot()

from dotenv import find_dotenv
from dotenv import load_dotenv

from .slack_bot import start_bot as run_slack_bot
from .telegram_bot import run_bot as run_telegram_bot
from .tool import k8s_qa
from .tool import persist_embeddings


def embedding():
    load_dotenv(find_dotenv(raise_error_if_not_found=True, usecwd=True))

    persist_embeddings()

def qa():
    load_dotenv(find_dotenv(raise_error_if_not_found=True, usecwd=True))
    k8s_qa()

def run_telegram():
    run_telegram_bot()

def run_slack():
    run_slack_bot()

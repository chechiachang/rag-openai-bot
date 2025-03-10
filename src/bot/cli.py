import os

from dotenv import find_dotenv
from dotenv import load_dotenv

from .conversational_retrieval_agent import ConversationalRetrievalAgent
from .document_loader.html import HTMLDocumentManager
from .document_loader.markdown import MarkdownDocumentManager
from .embedding_manager import EmbeddingManager
from .slack_bot import start_bot as run_slack_bot
from .telegram_bot import run_bot as run_telegram_bot

# functions

def persist_embeddings(doc_manager, collection_name, dry_run=True):
    embed_manager = EmbeddingManager(collection_name)

    doc_manager = doc_manager
    doc_manager.load_documents()
    doc_manager.split_documents()
    if not dry_run:
        embed_manager.create_and_persist_embeddings(doc_manager.all_sections)

# k8s

def embedding_k8s():
    load_dotenv(find_dotenv(raise_error_if_not_found=True, usecwd=True))
    persist_embeddings(
        MarkdownDocumentManager(
            directory_path=os.environ.get("DATA_PATH_K8S")
        ),
        collection_name=os.environ.get("QDRANT_COLLECTION_NAME_K8S"),
        dry_run=True
    )

def qa_k8s():
    load_dotenv(find_dotenv(raise_error_if_not_found=True, usecwd=True))
    bot = ConversationalRetrievalAgent(
        collection_name=os.environ["QDRANT_COLLECTION_NAME_K8S"]
    )
    bot.setup_bot()

    question = "How to provision pod network in kubernetes?"
    answer = bot.ask_question(question)
    print(question)
    print(answer)

# quip

def embedding_quip():
    load_dotenv(find_dotenv(raise_error_if_not_found=True, usecwd=True))
    persist_embeddings(
        HTMLDocumentManager(
            directory_path=os.environ.get("DATA_PATH_QUIP")
        ),
        collection_name=os.environ.get("QDRANT_COLLECTION_NAME_QUIP"),
        dry_run=True
    )

def qa_quip():
    load_dotenv(find_dotenv(raise_error_if_not_found=True, usecwd=True))
    bot = ConversationalRetrievalAgent(
        collection_name=os.environ["QDRANT_COLLECTION_NAME_QUIP"]
    )
    bot.setup_bot()

    question = "Influxdb Retention policy"
    answer = bot.ask_question(question)
    print(question)
    print(answer)

def run_telegram():
    run_telegram_bot()

def run_slack():
    run_slack_bot()

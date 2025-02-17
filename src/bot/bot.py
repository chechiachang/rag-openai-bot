from dotenv import find_dotenv
from dotenv import load_dotenv

from .document_manager import DocumentManager
from .embedding_manager import EmbeddingManager
from .conversational_retrieval_agent import ConversationalRetrievalAgent

def persist_embeddings():
    load_dotenv(find_dotenv(raise_error_if_not_found=True, usecwd=True))

    embed_manager = EmbeddingManager()

    data_path = "data/kubernetes-docs/"
    #data_path = "data/kubernetes-docs/docs/concepts/extend-kubernetes/"
    doc_manager = DocumentManager(data_path)
    doc_manager.load_documents()
    doc_manager.split_documents()
    embed_manager.create_and_persist_embeddings(doc_manager.all_sections)

    print(embed_manager.count())

def conversation():
    load_dotenv(find_dotenv(raise_error_if_not_found=True, usecwd=True))

    embed_manager = EmbeddingManager()
    bot = ConversationalRetrievalAgent(embed_manager.vectordb)
    bot.setup_bot()

    #question = "How to extend kubernetes?"
    question = "How to provision pod network?"
    print(question)
    print(bot.ask_question(question))

from .conversational_retrieval_agent import ConversationalRetrievalAgent
from .document_manager import DocumentManager
from .embedding_manager import EmbeddingManager


def persist_embeddings():
    embed_manager = EmbeddingManager('demo_collection')

    data_path = "data/kubernetes-docs/"
    doc_manager = DocumentManager(data_path)
    doc_manager.load_documents()
    doc_manager.split_documents()
    embed_manager.create_and_persist_embeddings(doc_manager.all_sections)

    print(embed_manager.count())

def k8s_qa():
    bot = ConversationalRetrievalAgent('demo_collection')
    bot.setup_bot()

    question = "How to provision pod network in kubernetes?"
    answer = bot.ask_question(question)
    print(question)
    print(answer)


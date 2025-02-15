from dotenv import find_dotenv
from dotenv import load_dotenv

from .document_manager import DocumentManager
from .embedding_manager import EmbeddingManager
from .conversational_retrieval_agent import ConversationalRetrievalAgent

def main():
    load_dotenv(find_dotenv(raise_error_if_not_found=True, usecwd=True))

    # Initialising and loading documents
    #data_path = "data/kubernetes-docs/"
    data_path = "data/kubernetes-docs/blog/_posts/2021-04-22-gateway-api/"
    doc_manager = DocumentManager(data_path)
    doc_manager.load_documents()
    doc_manager.split_documents()

    # Creation and persistence of embeddings
    embed_manager = EmbeddingManager()
    #embed_manager.create_and_persist_embeddings(doc_manager.all_sections)
    print(embed_manager.count())

    # Setup and use of conversation bots
    bot = ConversationalRetrievalAgent(embed_manager.vectordb)
    bot.setup_bot()
    print(bot.ask_question("What is a k8s hpa?"))

if __name__ == "__main__":
    main()

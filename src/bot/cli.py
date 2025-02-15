from dotenv import find_dotenv
from dotenv import load_dotenv

from .document_manager import DocumentManager
from .embedding_manager import EmbeddingManager
from .conversational_retrieval_agent import ConversationalRetrievalAgent

def main():
    load_dotenv(find_dotenv(raise_error_if_not_found=True, usecwd=True))

    # Creation and persistence of embeddings
    embed_manager = EmbeddingManager()

    ### Uncomment the following lines to create and persist embeddings to vector database
    #data_path = "data/kubernetes-docs/"
    #doc_manager = DocumentManager(data_path)
    #doc_manager.load_documents()
    #doc_manager.split_documents()

    #embed_manager.create_and_persist_embeddings(doc_manager.all_sections)
    ### end of embedding creation and persistence

    print(embed_manager.count())

    # Setup and use of conversation bots
    bot = ConversationalRetrievalAgent(embed_manager.vectordb)
    bot.setup_bot()
    print(bot.ask_question("What is hpa?"))
    print(bot.ask_question("What is controller?"))

if __name__ == "__main__":
    main()

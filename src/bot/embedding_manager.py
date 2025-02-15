import os

from langchain_openai import AzureOpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from uuid import uuid4

class EmbeddingManager:
    def __init__(self):
        self.openai_embeddings = AzureOpenAIEmbeddings(
            model='text-embedding-3-large',
            azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
            api_key=os.environ["AZURE_OPENAI_API_KEY"],
            openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"]
        )
        # intialize the vector store
        self.client=QdrantClient(host="localhost", port=6333)
        if not self.client.collection_exists('demo_collection'):
            self.client.create_collection(
               collection_name='demo_collection',
               vectors_config=VectorParams(
                   size=3072, 
                   distance=Distance.COSINE
                ),
            )
        # create the vector store
        self.vectordb = QdrantVectorStore(
            client=self.client,
            collection_name='demo_collection',
            embedding=self.openai_embeddings,
        )
        
    # Method to create and persist embeddings
    def create_and_persist_embeddings(self, all_sections):
        # add documents to the vector store
        uuids = [str(uuid4()) for _ in range(len(all_sections))]
        self.vectordb.add_documents(
            documents=all_sections,
            ids=uuids
        )

    def count(self):
        return self.client.count(
            collection_name='demo_collection',
            exact=True
        )

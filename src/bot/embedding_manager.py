import hashlib
import os

from langchain_openai import AzureOpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import Distance
from qdrant_client.models import VectorParams
from ratelimit import limits, sleep_and_retry


class EmbeddingManager:
    def __init__(self):
        self.openai_embeddings = AzureOpenAIEmbeddings(
            model='text-embedding-3-large',
            azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
            api_key=os.environ["AZURE_OPENAI_API_KEY"],
            openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
        )
        # initialize the qdrant client
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
        for section in all_sections:
            self.add_document(section)

    @sleep_and_retry
    @limits(calls=10, period=1)
    def add_document(self, document):
        # hash the source (url) to get a unique id
        print('Embedding progress:' + document.metadata['source'] + document.metadata['split'])
        hash = hashlib.sha256(
            str(document.metadata['source'] + document.metadata['split']).encode('utf-8')
        ).hexdigest()[::2]
        self.vectordb.add_documents(
            documents=[document],
            #ids=[str(uuid4())]
            ids=[hash]
        )

    def count(self):
        return self.client.count(
            collection_name='demo_collection',
            exact=True
        )

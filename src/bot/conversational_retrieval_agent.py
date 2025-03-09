import os

from langchain.chains import ConversationalRetrievalChain
from langchain_openai import AzureChatOpenAI
from ratelimit import limits
from ratelimit import sleep_and_retry

from .embedding_manager import EmbeddingManager


class ConversationalRetrievalAgent:
    # Initialize the ConversationalRetrievalAgent with a vector database and a temperature for the OpenAI model
    def __init__(self, collection_name, temperature=0.5):
        self.collection_name = collection_name
        self.llm = AzureChatOpenAI(
            temperature=temperature,
            azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
            azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
            openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
            #rate_limiter=InMemoryRateLimiter(
            #    requests_per_second=60,
            #    check_every_n_seconds=1,
            #)
        )
        self.chat_history = []

    # Method to get the chat history as a string
    def get_chat_history(self, inputs):
        res = []
        for human, ai in inputs:
            res.append(f"Human:{human}\nAI:{ai}")
        return "\n".join(res)

    # Method to set up the chain
    def setup_bot(self):
        embed_manager = EmbeddingManager(self.collection_name)
        self.vectordb = embed_manager.vectordb
        # Create a retriever from the vector database
        retriever = self.vectordb.as_retriever(
            #search_type="similarity",
            search_type="mmr",
            search_kwargs={
                "k": 4,
                #"score_threshold": 0.5,
            }
        )
        # Create a ConversationalRetrievalChain from the OpenAI model and the retriever
        self.chain = ConversationalRetrievalChain.from_llm(
            self.llm,
            retriever,
            return_source_documents=True,
            get_chat_history=self.get_chat_history,
        )

    def generate_prompt(self, question):
        if not self.chat_history:
            prompt = f"""你是一個問答任務的助手。根據 Retrival 的資料內容回答問題
            # 步驟
            1. 根據內容準確回答問題，確保答案清晰且準確，避免加入任何虛構或未經證實的資訊。
            2. 如果內容中沒有直接回答，請根據相關資訊進行合理推斷，但不要編造答案。
            3. 使用符合台灣用語習慣的表達方式，提高可讀性。
            4. 確保最終輸出內容為台灣繁體中文。如果是英文專有名詞，可以在字詞後加註原文。
               例如：「人工智慧（Artificial Intelligence）」。
            6. 如果內容有文章 title，顯示原文 title 不需要翻譯。
            7. 如果內容有url，請列出url。
            問題：{question}
            """
            #prompt = f"""You are an assistant for question-answering tasks.
            #Use the following pieces of retrieved context to answer the question.
            #If you don't know the answer, just say that you don't know.
            #Question: {question}
            #Context:
            #Answer:
            #"""
        else:
            # If it is the first question, use a specific template without previous conversation context
            print("Chat with previous history")
            context_entries = [f"Question: {q}\nAnswer: {a}" for q, a in self.chat_history[-3:]]
            context = "\n\n".join(context_entries)
            prompt = f"""Using the context provided by recent conversations,
            answer the new question in a concise and informative.
            Limit your answer to a maximum of three sentences.
            Context of recent conversations:
                {context}
            New question: {question}
            Answer:
            """

        return prompt

    @sleep_and_retry
    @limits(calls=600, period=60)
    def ask_question(self, query):
        prompt = self.generate_prompt(query)
        # Invoke the chain with the question and the chat history
        result = self.chain.invoke({"question": prompt, "chat_history": self.chat_history})
        # Append the question and the chain's answer to the chat history
        self.chat_history.append((query, result["answer"]))

        # Return the bot's answer
        return result["answer"]

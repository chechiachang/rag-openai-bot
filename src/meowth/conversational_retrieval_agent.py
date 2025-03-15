import os

from langchain.chains import create_history_aware_retriever
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
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

        condense_question_system_template = """
            給定一段對話歷史和最新的用戶問題，用戶問題可能參考對話歷史中的內容，
            重新構造一個獨立的問題，該問題可以在沒有對話歷史的情況下理解。
            不要直接回答問題，只有在需要時重新構造問題，否則原樣返回。
        """
        self.condense_question_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", condense_question_system_template),
                ("placeholder", "{chat_history}"),
                ("human", "{input}"),
            ]
        )

        system_prompt = """
            你是一個問答任務的助手。根據 Retrival 的資料內容回答問題。
            根據內容準確回答問題，確保答案清晰且準確，避免加入任何虛構或未經證實的資訊。
            保留內容重要資訊，如文章 title，顯示原文 title 不需要翻譯。
            保留內容重要資訊，如url，請列出不重複的url。
            有程式碼的部分，請列出程式碼。
            如果內容中沒有直接回答，請根據相關資訊進行合理推斷，但不要編造答案。
            使用符合台灣用語習慣的表達方式，提高可讀性。
            確保最終輸出內容為台灣繁體中文。如果是英文專有名詞，可以在字詞後加註原文。
            例如：「人工智慧（Artificial Intelligence）」。

            {context}
        """
        self.qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("placeholder", "{chat_history}"),
                ("human", "{input}"),
            ]
        )

    # Method to get the chat history as a string
    def get_chat_history(self, inputs):
        res = []
        for human, ai in inputs:
            res.append(f"Human:{human}\nAI:{ai}")
        return "\n".join(res)

    # Method to set up the chain
    def setup_bot(self):
        self.vectordb = EmbeddingManager(self.collection_name).vectordb
        # Create a retriever from the vector database
        vb_retriever = self.vectordb.as_retriever(
            #search_type="similarity",
            search_type="mmr",
            search_kwargs={
                "k": 4,
                #"score_threshold": 0.5,
            }
        )
        # Create a history-aware retriever from the OpenAI model and the retriever
        history_aware_retriever = create_history_aware_retriever(
            self.llm,
            vb_retriever,
            self.condense_question_prompt
        )
        self.qa_chain = create_stuff_documents_chain(
            self.llm,
            self.qa_prompt
        )
        self.convo_qa_chain = create_retrieval_chain(
            history_aware_retriever,
            self.qa_chain
        )

    def generate_prompt(self, question):
        if not self.chat_history:
            prompt = f"""
            問題：{question}
            """
        else:
            print("Chat with previous history")
            context_entries = [f"Question: {q}\nAnswer: {a}" for q, a in self.chat_history[-3:]]
            context = "\n\n".join(context_entries)
            prompt = f"""
                使用最近對話提供的內容，以簡潔且具信息性的方式回答新問題。
                最近對話的內容：{context}
                新問題：{question}
                答案：
            """

        return prompt

    @sleep_and_retry
    @limits(calls=600, period=60)
    def ask_question(self, question):
        prompt = self.generate_prompt(question)
        # Invoke the chain with the question and the chat history
        result = self.convo_qa_chain.invoke(
            {
                "input": prompt,
                "chat_history": self.chat_history
            }
        )
        # Append the question and the chain's answer to the chat history
        self.chat_history.append(
            (question, result["answer"])
        )

        # Return the bot's answer
        return result["answer"]

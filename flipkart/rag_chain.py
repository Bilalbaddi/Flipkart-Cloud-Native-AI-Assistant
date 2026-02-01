from operator import itemgetter
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableBranch
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from flipkart.config import Config

class RAGChainBuilder:
    def __init__(self,vector_store):
        self.vector_store=vector_store
        self.model = ChatGroq(model=Config.RAG_MODEL , temperature=0.5)
        self.history_store={}

    def _get_history(self, session_id: str) -> BaseChatMessageHistory:
        if session_id not in self.history_store:
            self.history_store[session_id] = ChatMessageHistory()
        return self.history_store[session_id]

    def build_chain(self):
        retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})

        # --- STEP 1: Contextualize Query (History Aware) ---
        # If there is chat history, rewrite the question. If not, use the raw question.
        
        context_system_prompt = (
            "Given a chat history and the latest user question "
            "which might reference context in the chat history, "
            "formulate a standalone question which can be understood "
            "without the chat history. Do NOT answer the question, "
            "just reformulate it if needed and otherwise return it as is."
        )
        
        context_prompt = ChatPromptTemplate.from_messages([
            ("system", context_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ])

        # This chain takes history + input -> outputs a search query
        history_aware_retriever = (
            context_prompt 
            | self.model 
            | StrOutputParser() 
            | retriever
        )

        # --- STEP 2: The QA Chain (Stuff Documents) ---
        
        qa_system_prompt = (
            "You are an e-commerce bot answering product-related queries.\n"
            "Use the following pieces of retrieved context to answer the question.\n"
            "If you don't know the answer, say that you don't know.\n\n"
            "{context}"
        )
        
        qa_prompt = ChatPromptTemplate.from_messages([
            ("system", qa_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ])

        # Helper to format documents into a single string
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        # The Final RAG Chain
        rag_chain = (
            RunnablePassthrough.assign(
                context=history_aware_retriever | format_docs 
            )
            | qa_prompt
            | self.model
            | StrOutputParser()
        )

        # --- STEP 3: Add Memory Management ---
        return RunnableWithMessageHistory(
            rag_chain,
            self._get_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer"
        )
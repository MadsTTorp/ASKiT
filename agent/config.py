import os
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceEndpoint
from langchain_chroma import Chroma

load_dotenv(find_dotenv())

def get_openai_models():
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    assert OPENAI_API_KEY, "Please set OPENAI_API_KEY environment variable"
    llm = ChatOpenAI(model="gpt-4o-mini")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    return llm, embeddings

def get_opensource_models():
    HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    assert HUGGINGFACEHUB_API_TOKEN, "Please set HUGGINGFACEHUB_API_TOKEN environment variable"
    endpoint_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    llm = HuggingFaceEndpoint(
        endpoint_url=endpoint_url,
        huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN
    )
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return llm, embeddings

def get_vectorstore(embeddings):
    provider = os.getenv("USE_PROVIDER", "huggingface").lower()
    if provider == "openai":
        return Chroma(
            persist_directory='./openai_chroma_langchain_db', 
            embedding_function=embeddings, 
            collection_name='openai_embeddings'
        )
    elif provider == "huggingface":
        return Chroma(
            persist_directory='./huggingface_chroma_langchain_db', 
            embedding_function=embeddings, 
            collection_name='huggingface_embeddings'
        )
    else:
        raise ValueError("Unknown provider specified. Use 'openai' or 'huggingface'.")

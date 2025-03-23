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
    base_dir = os.path.join(os.getcwd(), "data", "vectorstores")
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    
    if provider == "openai":
        persist_directory = os.path.join(base_dir, "openai_chroma_langchain_db")
        return Chroma(
            persist_directory=persist_directory,
            embedding_function=embeddings,
            collection_name='openai_embeddings'
        )
    elif provider == "huggingface":
        persist_directory = os.path.join(base_dir, "huggingface_chroma_langchain_db")
        return Chroma(
            persist_directory=persist_directory,
            embedding_function=embeddings,
            collection_name='huggingface_embeddings'
        )
    else:
        raise ValueError("Unknown provider specified. Use 'openai' or 'huggingface'.")

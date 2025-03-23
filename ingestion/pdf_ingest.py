import os
import PyPDF2
from langchain.docstore.document import Document
from agent.config import get_openai_models, get_opensource_models, get_vectorstore

def ingest_pdf_files(upload_dir: str):
    """
    Ingests all PDF files from the provided directory and adds them to the vectorstore.
    
    Args:
        upload_dir (str): Path to the directory containing the uploaded PDF files.
    """
    # Determine which provider to use based on the environment variable.
    # (The main.py script should have set this in .env or via session state.)
    provider = os.getenv("USE_PROVIDER", "huggingface").lower()
    
    if provider == "openai":
        llm, embeddings = get_openai_models()
    else:
        llm, embeddings = get_opensource_models()
    
    # Instantiate the vectorstore using the appropriate embeddings
    vectorstore = get_vectorstore(embeddings)
    
    documents = []
    # List PDF files in the upload directory
    for filename in os.listdir(upload_dir):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(upload_dir, filename)
            try:
                with open(pdf_path, "rb") as f:
                    pdf_reader = PyPDF2.PdfReader(f)
                    text = ""
                    # Extract text from each page in the PDF
                    for page in pdf_reader.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
                    if text.strip():
                        # Create a Document with the extracted text and PDF filename as title
                        doc = Document(page_content=text, metadata={"title": filename})
                        documents.append(doc)
                    else:
                        print(f"No text extracted from {filename}.")
            except Exception as e:
                print(f"Error processing {filename}: {e}")
    
    if documents:
        # Add all documents to the vectorstore in a single batch call
        vectorstore.add_documents(documents)
        print(f"Ingested {len(documents)} document(s) into the vectorstore.")
    else:
        print("No documents were ingested.")

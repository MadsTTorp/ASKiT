import os
import streamlit as st
from ingestion.pdf_ingest import ingest_pdf_files  # Your PDF ingestion function
import sys
import os

current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Configure the page
st.set_page_config(page_title="RAG Chat Application Setup", layout="wide")

# Initialize session state variables if they don't exist
if "provider" not in st.session_state:
    st.session_state.provider = None
if "token" not in st.session_state:
    st.session_state.token = None
if "uploaded" not in st.session_state:
    st.session_state.uploaded = False
if "rag_created" not in st.session_state:
    st.session_state.rag_created = False

st.title("RAG Chat Application Setup")

# -------------------------
# Step 1: Provider & API Token
# -------------------------
if st.session_state.provider is None or st.session_state.token is None:
    st.markdown("## Step 1: Select Model Provider and Enter API Token")
    provider = st.radio("Choose your provider:", ("OPENAI", "OPENSOURCE"))
    token = st.text_input("Please insert your API token", type="password")
    if st.button("Submit Credentials") and token:
        # Save values in session state (note: you can also validate the token here)
        st.session_state.provider = provider.lower()
        st.session_state.token = token
        st.success("Credentials saved! Proceed to upload documents.")

# -------------------------
# Step 2: Document Upload & Knowledge Base Creation
# -------------------------
if st.session_state.provider is not None and st.session_state.token is not None:
    st.markdown("## Step 2: Upload PDF Documents")
    uploaded_files = st.file_uploader("Upload PDF documents", type=["pdf"], accept_multiple_files=True)
    
    if uploaded_files:
        upload_dir = "uploaded_files"
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        # Save each uploaded file locally
        for uploaded_file in uploaded_files:
            file_path = os.path.join(upload_dir, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
        st.session_state.uploaded = True
        st.success("Files uploaded successfully!")
    
    if st.session_state.uploaded and not st.session_state.rag_created:
        if st.button("Create RAG"):
            with st.spinner("Ingesting documents and creating knowledge base..."):
                ingest_pdf_files("uploaded_files")
            st.session_state.rag_created = True
            st.success("Knowledge base created!")

# -------------------------
# Step 3: Navigate to Chat Interface
# -------------------------
if st.session_state.rag_created:
    st.markdown("## Step 3: Chat Interface")
    st.info("Your RAG knowledge base is ready. Click below to start chatting!")
    # Provide a clickable link to the chat page. In a multipage app this link would navigate to chat.py.
    st.markdown("[Go to Chat Interface](./chat.py)")

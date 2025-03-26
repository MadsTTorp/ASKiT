import sys
import os
import streamlit as st
from ingestion.pdf_ingest import ingest_pdf_files

# Ensure the project root is in sys.path (if needed)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

st.set_page_config(page_title="ASKiT - chat with your data", layout="wide")

# Updated CSS to center content for the login form
st.markdown(
    """
    <style>
    .centered-container {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        height: 20vh;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize session state variables if not present
if "provider" not in st.session_state:
    st.session_state.provider = None
if "token" not in st.session_state:
    st.session_state.token = None
if "uploaded" not in st.session_state:
    st.session_state.uploaded = False
if "rag_created" not in st.session_state:
    st.session_state.rag_created = False

# -------------------------
# Step 1: Login Screen (Credentials)
# -------------------------
if st.session_state.provider is None or st.session_state.token is None:
    with st.container():
        st.markdown("<div class='centered-container'>", unsafe_allow_html=True)
        st.title("ASKiT - chat with your data")
        st.markdown("### What LLM-provider do you want to use?")
        provider_choice = st.radio("Select Provider", ("OPENAI", "Open Source (Free)"), label_visibility="visible")
        token_input = st.text_input("Please provide your API token", type="password")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Submit Credentials") and token_input:
                st.session_state.provider = "openai" if provider_choice.upper() == "OPENAI" else "huggingface"
                st.session_state.token = token_input
                st.success("Credentials saved!")
                st.rerun()  # Force a re-run to show the next step
        with col2:
            if st.button("Use Key from Environment"):
                if provider_choice.upper() == "OPENAI":
                    env_token = os.getenv("OPENAI_API_KEY")
                else:
                    env_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
                if env_token:
                    st.session_state.provider = "openai" if provider_choice.upper() == "OPENAI" else "huggingface"
                    st.session_state.token = env_token
                    st.success("Credentials saved using environment variable!")
                    st.rerun()  # Force a re-run to show the next step
                else:
                    st.error("No token found in environment!")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# -------------------------
# Step 2: Document Upload & Knowledge Base Creation
# -------------------------
st.title("Upload PDF Documents")
st.markdown("Drag and drop your PDF files below:")

# Display the file uploader on the same page (allowing multiple interactions)
uploaded_files = st.file_uploader("Upload your PDFs", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    upload_dir = "uploaded_files"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    file_names = []
    for uploaded_file in uploaded_files:
        file_path = os.path.join(upload_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        file_names.append(uploaded_file.name)
    st.session_state.uploaded = True
    st.success(f"Uploaded files: {', '.join(file_names)}")

# Display the "Submit and Create RAG" button if files have been uploaded but vector store is not yet created
if st.session_state.uploaded and not st.session_state.rag_created:
    if st.button("Submit and Create RAG"):
        with st.spinner("Ingesting documents and creating knowledge base..."):
            ingest_pdf_files("uploaded_files")
        st.session_state.rag_created = True
        st.success("Your chatbot is ready!")
        st.rerun()  # Refresh to display the final step

# -------------------------
# Step 3: Setup Complete
# -------------------------
if st.session_state.rag_created:
    st.title("Setup Complete")
    st.info("Your RAG knowledge base is ready. Please use the sidebar to navigate to the Chat Interface.")

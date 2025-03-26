import streamlit as st
import os

st.set_page_config(page_title="Vector Store Content", layout="wide")

st.title("Vector Store Content")
st.markdown(
    """
    Explore the documents that power your AI agent. Each card represents a PDF you’ve uploaded.
    """,
    unsafe_allow_html=True,
)

# Check if the vector store has been created
if "rag_created" not in st.session_state or not st.session_state.rag_created:
    st.info("No vector store has been created yet. Please complete the document upload and vector store creation in the Setup page.")
    st.stop()

# Define the directory where uploaded PDFs are stored
upload_dir = "uploaded_files"

# Verify that the upload directory exists
if not os.path.exists(upload_dir):
    st.warning("The upload directory does not exist. No documents to display.")
else:
    files = os.listdir(upload_dir)
    if not files:
        st.warning("No documents found in the vector store.")
    else:
        st.markdown("### Uploaded Documents")
        # You can style the cards with CSS for a professional look.
        for file in files:
            st.markdown(
                f"""
                <div style="
                    background-color: #f8f9fa;
                    border: 1px solid #dee2e6;
                    border-radius: 10px;
                    padding: 15px;
                    margin-bottom: 10px;
                ">
                    <h4 style="margin: 0; color: #343a40;">{file}</h4>
                    <p style="margin: 0; color: #6c757d;">Uploaded Document</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
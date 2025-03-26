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

# Verify that the upload directory exists and list its files
if not os.path.exists(upload_dir):
    st.warning("The upload directory does not exist. No documents to display.")
else:
    pdf_files = os.listdir(upload_dir)
    if not pdf_files:
        st.warning("No documents found in the vector store.")
    else:
        # Inject custom CSS for a fun, card-style layout
        st.markdown(
            """
            <style>
            .pdf-card {
                background-color: #2e2e2e;  /* Dark grey background */
                border: 1px solid #444444;
                border-radius: 10px;
                padding: 15px;
                margin-bottom: 15px;
                text-align: center;
                box-shadow: 0px 4px 6px rgba(0,0,0,0.4);
                transition: transform 0.2s, box-shadow 0.2s;
            }
            .pdf-card:hover {
                transform: scale(1.03);
                box-shadow: 0px 6px 8px rgba(0,0,0,0.6);
            }
            .pdf-icon {
                width: 80px;
                margin-bottom: 10px;
            }
            .pdf-title {
                color: #ffffff;
                font-size: 1.2rem;
                font-weight: bold;
                margin-bottom: 5px;
            }
            .pdf-label {
                color: #cccccc;
                font-size: 0.9rem;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        
        st.markdown("### Uploaded Documents")
        # Create a grid layout with three columns
        cols = st.columns(3)
        for idx, file in enumerate(pdf_files):
            col = cols[idx % 3]
            # PDF icon URL; you can replace it with your preferred icon
            pdf_icon_url = "https://upload.wikimedia.org/wikipedia/commons/8/87/PDF_file_icon.svg"
            card_html = f"""
            <div class="pdf-card">
                <img src="{pdf_icon_url}" alt="PDF Icon" class="pdf-icon">
                <div class="pdf-title">{file}</div>
                <div class="pdf-label">PDF Document</div>
            </div>
            """
            col.markdown(card_html, unsafe_allow_html=True)
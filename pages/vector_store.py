import streamlit as st
import os

st.set_page_config(page_title="Vector Store Content", layout="wide")

st.title("Vector Store Content")
st.markdown("This page displays the documents that the AI agent has access to, based on your uploaded PDFs.")

# Check if the vector store has been created
if "rag_created" not in st.session_state or not st.session_state.rag_created:
    st.info("No vector store has been created yet. Please complete the document upload and vector store creation in the Setup page.")
    st.stop()
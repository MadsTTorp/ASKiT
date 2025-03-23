import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from agent.rag_agent import app  # Your compiled RAG agent

# Set page configuration (if desired)
st.set_page_config(page_title="RAG Chat Interface", layout="wide")

# Inject custom CSS for chat bubbles and layout
st.markdown(
    """
    <style>
    .chat-container {
        max-width: 800px;
        margin: auto;
    }
    .user-message {
        text-align: right;
        background-color: #dcf8c6;
        padding: 10px;
        border-radius: 10px;
        margin: 5px;
    }
    .assistant-message {
        text-align: left;
        background-color: #f1f0f0;
        padding: 10px;
        border-radius: 10px;
        margin: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("RAG Chat Interface")
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

# Verify that the knowledge base is ready; if not, inform the user
if "rag_created" not in st.session_state or not st.session_state.rag_created:
    st.error("Knowledge base not created. Please complete the setup in the main page.")
    st.stop()

# Initialize conversation history if not present
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the conversation history with custom alignment
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='user-message'>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='assistant-message'>{msg['content']}</div>", unsafe_allow_html=True)

# Accept new user input using st.chat_input
user_input = st.chat_input("Ask a question about your documents:")

if user_input:
    # Append the user's message and immediately refresh to show it
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.rerun()

    # Prepare the state for the agent
    state = {"messages": [HumanMessage(content=user_input)], "meta": {"provider": st.session_state.provider}}
    
    # Show a loading spinner while retrieving the answer
    with st.spinner("Retrieving answer..."):
        agent_response = app.invoke(state)
    
    # Append each agent response message to the conversation
    for msg in agent_response.get("messages", []):
        st.session_state.messages.append({"role": "assistant", "content": msg.content})
    
    st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

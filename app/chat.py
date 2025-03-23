import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from agent.rag_agent import app  # Import your compiled RAG agent

# Configure the page
st.set_page_config(page_title="RAG Chat Interface", layout="wide")

st.title("RAG Chat Interface")

# Initialize the conversation history if needed
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing conversation using chat message containers
st.markdown("## Conversation")
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Accept new user input via a chat input widget
user_input = st.chat_input("Ask a question about your documents:")

if user_input:
    # Append the user's message to the conversation
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Prepare a minimal agent state. You may extend this to include more context.
    state = {"messages": [HumanMessage(content=user_input)], "meta": {}}
    
    # Run the agent (using the .run method, as the compiled agent is not callable directly)
    agent_response = app.run(state)
    
    # Append each agent response message to the conversation
    for msg in agent_response.get("messages", []):
        st.session_state.messages.append({"role": "assistant", "content": msg.content})
    
    # Force a rerun to update the chat window with new messages.
    try:
        st.experimental_rerun()
    except Exception:
        pass

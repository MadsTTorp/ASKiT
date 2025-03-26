import streamlit as st
import time
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from agent.rag_agent import app  # Your compiled RAG agent

st.set_page_config(page_title="Chat Interface", layout="wide")

# Inject custom CSS for a professional, dark-themed chat UI
st.markdown(
    """
    <style>
    .chat-container {
        max-width: 1800px;
        margin: 100px;
        display: flex;
        flex-direction: column;
        padding: 20px;
    }
    .user-message {
        align-self: flex-end;
        background-color: #274690;
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 8px;
        max-width: 70%;
        font-size: 1.1rem;
    }
    .assistant-message {
        align-self: flex-start;
        background-color: #333333;
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 1px;
        max-width: 70%;
        font-size: 1.0rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("ASKiT")

# Verify that the knowledge base is ready
if "rag_created" not in st.session_state or not st.session_state.rag_created:
    st.error("Knowledge base not created. Please complete the setup on the main page.")
    st.stop()

# Initialize conversation history if not present
if "messages" not in st.session_state:
    st.session_state.messages = []

# Use a flag to ensure the same query is not processed twice.
if "last_input" not in st.session_state:
    st.session_state.last_input = ""

# Create a placeholder for the conversation
conversation_placeholder = st.empty()

def render_conversation():
    """Render the entire conversation as a single HTML block."""
    conversation_html = "<div class='chat-container'>"
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            conversation_html += f"<div class='user-message'>{msg['content']}</div>"
        else:
            conversation_html += f"<div class='assistant-message'>{msg['content']}</div>"
    conversation_html += "</div>"
    conversation_placeholder.markdown(conversation_html, unsafe_allow_html=True)

# Render any existing conversation
render_conversation()

# Accept new user input using st.chat_input with a fixed key
user_input = st.chat_input("Ask a question about your documents:", key="chat_input")

if user_input and user_input != st.session_state.last_input:
    st.session_state.last_input = user_input  # Mark this input as processed
    st.session_state.messages.append({"role": "user", "content": user_input})
    render_conversation()  # Update conversation to show user message

    # Prepare the state for the agent call using the provider from session state
    state = {
        "messages": [HumanMessage(content=user_input)],
        "meta": {"provider": st.session_state.provider},
    }

    # Retrieve the agent's response with a spinner
    with st.spinner("Retrieving answer..."):
        agent_response = app.invoke(state)

    # Extract the AIMessage from the agent response if available
    if "messages" in agent_response and agent_response["messages"]:
        agent_response_msg = next(
            (msg for msg in reversed(agent_response["messages"]) if isinstance(msg, AIMessage)),
            None,
        )
        full_answer = agent_response_msg.content if agent_response_msg else "No response from agent."
    else:
        full_answer = "No response from agent."

    # Create a placeholder to stream the answer letter by letter
    answer_placeholder = st.empty()
    streaming_text = ""
    for letter in full_answer:
        streaming_text += letter
        answer_placeholder.markdown(
            f"<div class='assistant-message'>{streaming_text}</div>",
            unsafe_allow_html=True,
        )
        time.sleep(0.005)  # Adjust delay for streaming effect
    answer_placeholder.empty()  # Clear the temporary placeholder

    # Append the full assistant answer to the conversation history and re-render
    st.session_state.messages.append({"role": "assistant", "content": streaming_text})
    render_conversation()

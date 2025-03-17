import sys
import os

# Add the project root directory to sys.path
current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from agent.rag_agent import app  

# Set the title of the app
st.title("Simple RAG Chat Interface")

# Initialize the conversation state in Streamlit session_state
if "conversation" not in st.session_state:
    st.session_state.conversation = []

def run_agent(user_input):
    """
    Append the user's message to the conversation, run the agent, 
    and update the conversation with the agent's responses.
    """
    # Create a HumanMessage with the user input
    human_msg = HumanMessage(content=user_input)
    st.session_state.conversation.append(human_msg)

    # Prepare the state for the agent (you may include extra metadata if needed)
    state = {"messages": st.session_state.conversation, "meta": {}}
    
    # Run the agent which is expected to process the state and return new messages
    new_state = app.invoke(state)
    
    # Append any new messages from the agent to the conversation
    for msg in new_state.get("messages", []):
        st.session_state.conversation.append(msg)

# Create a text input for the user to enter their query.
user_input = st.text_input("Your query:")

# When the user submits input, run the agent
if user_input:
    run_agent(user_input)
    # Clear the text input for the next message (if desired)
    st.experimental_rerun()

# Display the conversation history
for msg in st.session_state.conversation:
    if isinstance(msg, HumanMessage):
        st.markdown(f"**You:** {msg.content}")
    elif isinstance(msg, AIMessage):
        st.markdown(f"**Assistant:** {msg.content}")
    elif isinstance(msg, ToolMessage):
        st.markdown(f"**Retrieved Context:** {msg.content}")

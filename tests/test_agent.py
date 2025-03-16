import pytest
from langchain_core.messages import HumanMessage
from agent import app

def test_agent_retrieval():
    # Initialize a simple state with a dummy human message
    state = {"messages": [HumanMessage(content="Test query")], "meta": {}}
    new_state = app(state)
    # Check that new messages were added to the conversation
    assert "messages" in new_state
    assert len(new_state["messages"]) > 0
import os
import uuid
from typing import Sequence, Annotated
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage, HumanMessage, ToolMessage, AIMessage
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END

from agent.config import get_openai_models, get_opensource_models, get_vectorstore

# Set up models and vectorstore based on configuration
provider = os.getenv("USE_PROVIDER", "huggingface").lower()
if provider == "openai":
    llm, embeddings = get_openai_models()
else:
    llm, embeddings = get_opensource_models()

vectorstore = get_vectorstore(embeddings)
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    meta: dict

def retrieval_node(state: AgentState):
    query = state["messages"][-1].content
    docs = retriever.invoke(query)
    tool_call_id = str(uuid.uuid4())
    detailed_content = "\n\n".join(
        f"Title: {doc.metadata.get('title', 'test_document')}\nContent: {doc.page_content}"
        for doc in docs
    )
    tool_message = ToolMessage(
        content=detailed_content,
        name="stored_documents_retrieved",
        tool_call_id=tool_call_id
    )
    return {"messages": [tool_message]}

def retrieve_latest_message_typ(state: AgentState, message_type):
    latest_message = next(
        (msg for msg in reversed(state["messages"]) if isinstance(msg, message_type)),
        None
    )
    if latest_message is None:
        raise ValueError(f"No message found of type {message_type}")
    return latest_message

def generate_answer_node(state: AgentState):
    context = retrieve_latest_message_typ(state, ToolMessage).content
    query = retrieve_latest_message_typ(state, HumanMessage).content
    prompt = f"""
    You are a helpful assistant answering queries based strictly on the context provided.

    Context:
    {context}

    Query: {query}
    """
    response = llm.invoke(prompt)
    return {"messages": [response]}

def agent_router(state: AgentState):
    needs_retrieval = True  # This can be enhanced later with dynamic logic
    next_step = "retrieve" if needs_retrieval else END
    routing_message = AIMessage(content=next_step)
    return {"messages": [routing_message]}

# Build the state graph.
graph = StateGraph(AgentState)
graph.add_node("agent_router", agent_router)
graph.add_node("retrieve", retrieval_node)
graph.add_node("generate", generate_answer_node)
graph.set_entry_point("agent_router")
graph.add_conditional_edges(
    "agent_router",
    lambda state: retrieve_latest_message_typ(state, AIMessage).content,
    path_map={"retrieve": "retrieve", END: END}
)
graph.add_edge("retrieve", "generate")
graph.set_finish_point("generate")

# Compile the graph to create the agent callable.
app = graph.compile()

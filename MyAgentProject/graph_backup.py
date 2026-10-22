from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from langchain_ollama import ChatOllama


# ==================================================
# 1. State
# ==================================================

class ChatState(TypedDict):
    user_message: str
    response: str


# ==================================================
# 2. Ollama / Local LLM
# ==================================================

llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0.7
)


# ==================================================
# 3. Chat Node
# ==================================================

def chat_node(state: ChatState):

    user_message = state["user_message"]

    response = llm.invoke(user_message)

    return {
        "response": response.content
    }


# ==================================================
# 4. Build LangGraph
# ==================================================

builder = StateGraph(ChatState)

builder.add_node("chat", chat_node)

builder.add_edge(START, "chat")
builder.add_edge("chat", END)


# ==================================================
# 5. Compile
# ==================================================

graph = builder.compile()


# ==================================================
# 6. Function used by HEXBot
# ==================================================

def ask_graph(message: str):

    result = graph.invoke({
        "user_message": message,
        "response": ""
    })

    return result["response"]


# ==================================================
# 7. Test
# ==================================================

if __name__ == "__main__":

    print("Testing LangGraph + Ollama...")

    answer = ask_graph(
        "Hello! You are HEXBot. Introduce yourself in two sentences."
    )

    print("\nHEXBot:")
    print(answer)
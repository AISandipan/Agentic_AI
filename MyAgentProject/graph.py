from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from rag.rag_prompt import ask_rag


class ChatState(TypedDict):
    question: str
    answer: str


def rag_node(state: ChatState):
    question = state["question"]

    answer = ask_rag(question)

    return {
        "answer": answer
    }


# Create graph
builder = StateGraph(ChatState)

builder.add_node("rag", rag_node)

builder.add_edge(START, "rag")
builder.add_edge("rag", END)

graph = builder.compile()


# Function used by the GUI
def ask_graph(question: str) -> str:
    result = graph.invoke({
        "question": question,
        "answer": ""
    })

    return result["answer"]


if __name__ == "__main__":
    print("Testing LangGraph + RAG + Ollama...\n")

    question = "What technologies does HEXBot use?"

    result = graph.invoke({
        "question": question,
        "answer": ""
    })

    print("Question:")
    print(question)

    print("\nHEXBot:")
    print(result["answer"])
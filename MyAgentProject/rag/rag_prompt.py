

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

from rag.retriever import get_retriever


# Local LLM
llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0.2,
)


prompt = ChatPromptTemplate.from_template(
    """
You are HEXBot, a helpful AI assistant.

Answer the user's question using the provided context.

If the answer cannot be found in the context, say:
"I don't have enough information in my documents to answer that."

Do not invent information.

Context:
{context}

User question:
{question}

Answer:
"""
)


def ask_rag(question: str):
    retriever = get_retriever()

    documents = retriever.invoke(question)

    context = "\n\n".join(
        document.page_content
        for document in documents
    )

    messages = prompt.format_messages(
        context=context,
        question=question,
    )

    response = llm.invoke(messages)

    return response.content


if __name__ == "__main__":
    print("Testing RAG + Ollama...\n")

    question = "What is HEXBot?"

    answer = ask_rag(question)

    print("Question:")
    print(question)

    print("\nHEXBot:")
    print(answer)
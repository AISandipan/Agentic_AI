

from pathlib import Path

from langchain_ollama import OllamaEmbeddings
#from langchain_community.vectorstores import Chroma
from langchain_chroma import Chroma


BASE_DIR = Path(__file__).resolve().parent.parent
CHROMA_DIR = BASE_DIR / "data" / "chroma"


def get_retriever():
    embeddings = OllamaEmbeddings(
        model="nomic-embed-text"
    )

    vectorstore = Chroma(
        persist_directory=str(CHROMA_DIR),
        embedding_function=embeddings,
    )

    return vectorstore.as_retriever(
        search_kwargs={"k": 3}
    )


if __name__ == "__main__":
    print("Testing RAG retriever...")

    retriever = get_retriever()

    results = retriever.invoke(
        "What is HEXBot?"
    )

    print(f"\nRetrieved documents: {len(results)}\n")

    for i, doc in enumerate(results, 1):
        print(f"--- Result {i} ---")
        print(doc.page_content)
        print()
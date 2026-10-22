


from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma


# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DOCUMENTS_DIR = BASE_DIR / "data" / "documents"
CHROMA_DIR = BASE_DIR / "data" / "chroma"


def ingest_documents():
    documents = []

    # Find all .txt files
    for file_path in DOCUMENTS_DIR.glob("*.txt"):
        print(f"Loading: {file_path.name}")

        loader = TextLoader(
            str(file_path),
            encoding="utf-8"
        )

        documents.extend(loader.load())

    if not documents:
        print("No documents found.")
        return

    print(f"Documents loaded: {len(documents)}")

    # Local Ollama embedding model
    embeddings = OllamaEmbeddings(
        model="nomic-embed-text"
    )

    print("Creating vector database...")

    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=str(CHROMA_DIR),
    )

    print("RAG ingestion completed!")
    print(f"Vector database: {CHROMA_DIR}")


if __name__ == "__main__":
    ingest_documents()
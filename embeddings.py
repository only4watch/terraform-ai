import uuid
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from config import CHROMA_COLLECTION

# Persistent DB
chroma_client = chromadb.Client(
    Settings(
        persist_directory="./chroma_db",
        is_persistent=True
    )
)

# Local embedding (FREE + stable)
default_embedding = embedding_functions.DefaultEmbeddingFunction()

collection = chroma_client.get_or_create_collection(
    name=CHROMA_COLLECTION,
    embedding_function=default_embedding
)

print("Chroma document count:", collection.count())


def add_chunks_to_db(chunks):
    if not chunks:
        return

    ids = [str(uuid.uuid4()) for _ in chunks]

    collection.add(
        documents=chunks,
        ids=ids
    )

    print("Added chunks:", len(chunks))
    print("Updated Chroma count:", collection.count())


def search_similar(query: str, n_results: int = 3):
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    if results and results.get("documents"):
        return results["documents"][0]

    return []

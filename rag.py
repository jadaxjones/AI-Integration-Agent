# rag.py
import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection("api_schema")


def index_endpoints(endpoints: list):
    docs = []
    ids = []
    for i, e in enumerate(endpoints):
        text = f"{e['method']} {e['path']} - {e['summary']} {e['description']}"
        docs.append(text)
        ids.append(str(i))

    embeddings = model.encode(docs).tolist()
    collection.add(documents=docs, embeddings=embeddings, ids=ids)
    print(f"Indexed {len(docs)} endpoints into ChromaDB")


def retrieve_relevant(query: str, n=3) -> list:
    query_embedding = model.encode([query]).tolist()[0]
    results = collection.query(query_embeddings=[query_embedding], n_results=n)
    return results["documents"][0]

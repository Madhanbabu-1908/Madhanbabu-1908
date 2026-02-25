import chromadb
from embeddings import get_embedding

client = chromadb.Client()
collection = client.get_or_create_collection(name="knowledge_base")

def add_documents(docs):
    for i, doc in enumerate(docs):
        collection.add(
            ids=[str(i)],
            documents=[doc],
            embeddings=[get_embedding(doc)]
        )

def query_db(query, n_results=3):
    results = collection.query(
        query_embeddings=[get_embedding(query)],
        n_results=n_results
    )
    return results['documents'][0]

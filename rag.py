from vector_db import query_db
from llm import generate_response

def rag_pipeline(query):
    context_docs = query_db(query)
    context = "\n".join(context_docs)

    prompt = f"""
    You are an enterprise AI assistant.

    Context:
    {context}

    Question:
    {query}

    Answer clearly and professionally.
    """

    return generate_response(prompt)

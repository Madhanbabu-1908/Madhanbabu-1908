import os

def load_documents(path="data/documents"):
    docs = []
    for file in os.listdir(path):
        with open(os.path.join(path, file), "r", encoding="utf-8") as f:
            docs.append(f.read())
    return docs

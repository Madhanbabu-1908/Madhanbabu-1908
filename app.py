from dotenv import load_dotenv
load_dotenv()
import streamlit as st
from rag import rag_pipeline
from ingestion import load_documents
from vector_db import add_documents
import os
print("API KEY:", os.getenv("LITELLM_API_KEY"))

st.set_page_config(page_title="Enterprise AI Agent", layout="wide")

# Sidebar
st.sidebar.title("⚙️ Settings")
if st.sidebar.button("Load Training Data"):
    docs = load_documents()
    add_documents(docs)
    st.sidebar.success("Data Loaded into Vector DB")

# Chat UI
st.title("🤖 Enterprise AI Agent")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.chat_input("Ask something...")

if user_input:
    response = rag_pipeline(user_input)

    st.session_state.chat_history.append(("user", user_input))
    st.session_state.chat_history.append(("bot", response))

# Display chat
for role, msg in st.session_state.chat_history:
    if role == "user":
        st.chat_message("user").write(msg)
    else:
        st.chat_message("assistant").write(msg)

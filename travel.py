import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

# ---------------- LangChain Imports ----------------
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.chat_models import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_community.text_splitter import CharacterTextSplitter
from langchain_community.schema import Document
from langchain_community.tools import Tool
from langchain_community.agents import initialize_agent, AgentType
from langchain_community.memory import ConversationBufferMemory

# ---------------- Load Environment Variables ----------------
load_dotenv()
GENAI_API_KEY = os.getenv("GENAI_API_KEY")

# ---------------- Flask App ----------------
app = Flask(__name__)
CORS(app)

# ---------------- LLM Configuration ----------------
llm = ChatOpenAI(
    model_name="azure/genailab-maas-gpt-4.1",  # GPT reasoning model
    openai_api_key=GENAI_API_KEY,
    openai_api_base="https://genailab.tcs.in",
    temperature=0.2
)

# ---------------- Embeddings ----------------
embeddings = OpenAIEmbeddings(
    model="azure/genailab-maas-text-embedding-3-large",
    openai_api_key=GENAI_API_KEY,
    openai_api_base="https://genailab.tcs.in"
)

# ---------------- Load Policy Documents ----------------
POLICY_DIR = "policies"

def load_policies():
    docs = []
    if not os.path.exists(POLICY_DIR):
        os.makedirs(POLICY_DIR)
    for file in os.listdir(POLICY_DIR):
        if file.endswith(".txt"):
            with open(os.path.join(POLICY_DIR, file), "r", encoding="utf-8") as f:
                docs.append(f.read())
    return docs

policy_texts = load_policies()

# ---------------- Text Splitter ----------------
splitter = CharacterTextSplitter(chunk_size=800, chunk_overlap=100)
documents = []

for text in policy_texts:
    chunks = splitter.split_text(text)
    for chunk in chunks:
        documents.append(Document(page_content=chunk))

# ---------------- Vector Store (Chroma) ----------------
vectorstore = Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
    persist_directory="./vectorstore"
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# ---------------- Tools for Agent ----------------
def retrieve_policy(query: str) -> str:
    docs = retriever.get_relevant_documents(query)
    return "\n\n".join([d.page_content for d in docs])

def compare_policies(query: str) -> str:
    docs = retriever.get_relevant_documents(query)
    prompt = f"""
Compare these travel insurance policies clearly:

{chr(10).join([d.page_content for d in docs])}

Highlight:
- Coverage differences
- Claim process
- Premium differences
- Best for whom
"""
    return llm(prompt)

def recommend_coverage(query: str) -> str:
    docs = retriever.get_relevant_documents(query)
    prompt = f"""
User profile and preferences: {query}

Policies:
{chr(10).join([d.page_content for d in docs])}

Provide:
1. Personalized recommendation
2. Why it is suitable
3. What to avoid
4. Simplified explanation
"""
    return llm(prompt)

tools = [
    Tool(name="PolicyRetriever", func=retrieve_policy, description="Retrieve policy details"),
    Tool(name="PolicyComparison", func=compare_policies, description="Compare travel insurance policies"),
    Tool(name="CoverageRecommendation", func=recommend_coverage, description="Recommend best coverage")
]

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    memory=memory,
    verbose=False
)

# ---------------- Flask Routes ----------------
@app.route("/")
def home():
    return "<h2>✅ AI Travel Insurance Advisor Running</h2>"

@app.route("/ui")
def serve_ui():
    return send_from_directory(".", "index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "").strip()

    if not user_input:
        return jsonify({"reply": "Please provide a valid input."})

    try:
        response = agent.run(user_input)
    except Exception as e:
        response = f"Error: {str(e)}"

    return jsonify({"reply": response})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
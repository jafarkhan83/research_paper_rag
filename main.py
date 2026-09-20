from parser import initializer
from chunking import parent_child_chunking
from utilities import serialize_object, find_neighbors, deserialize_object, query_rewriting
from ingest import create_embeddings
from retriever import retriever_interface
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
q_groq = ChatGroq(
    model="openai/gpt-oss-safeguard-20b",
    temperature=0,
    reasoning_effort="low"
)

a_groq = ChatGroq(
    model="openai/gpt-oss-safeguard-20b",
    temperature=0,
    reasoning_effort="medium"
)

def initialize(file_path):
    sections = initializer(file_path)
    parent, children = parent_child_chunking(sections)

    if os.path.exists("pkl/children.pkl"):
        os.remove("pkl/children.pkl")

    serialize_object(children, "pkl/children.pkl")
    create_embeddings(children, model)

    print("Embeddings created, saved to pkl/children.pkl")

def retrieve(query, k, r, s):
    children = deserialize_object("pkl/children.pkl")
    r_query = query_rewriting(query, model=q_groq)
    try:
        chunks = retriever_interface(model, r_query.content, k=k, r=r, children=children)
        top_chunk = chunks[0]
        return find_neighbors(top_chunk, s, children)
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# initialize("papers/test_01.pdf")
query = "tell me about conclusion of this research paper."
chunks = retrieve(query=query, k=2, r=2, s=3)

for c in chunks:
    print(c, end='\n\n')
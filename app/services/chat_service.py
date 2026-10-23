from .parser import initializer
from .chunking import parent_child_chunking
from .utilities import (
    serialize_object,
    find_neighbors,
    deserialize_object,
    query_rewriting,
    final_response,
)
from .ingest import create_embeddings
from .retriever import retriever_interface
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
PAPERS_DIR = BASE_DIR / "papers"
PKL_DIR = BASE_DIR / "pkl"

class ChatService:

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
    
    def __init__(self):
        self.model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    def initialize(self, file_path):
        sections = initializer(file_path)
        parent, children = parent_child_chunking(sections)

        children_path = PKL_DIR / "children.pkl"
        parent_path = PKL_DIR / "parent.pkl"

        if children_path.exists():
            children_path.unlink()

        if parent_path.exists():
            parent_path.unlink()

        serialize_object(children, children_path)
        serialize_object(parent, parent_path)
        create_embeddings(children, self.model)

        print("Embeddings created")

    def retrieve(self, query, k, r, s):
        children = deserialize_object(PKL_DIR / "children.pkl")
        try:
            chunks = retriever_interface(self.model, query, k=k, r=r, children=children)
            top_chunk = chunks[0]
            return find_neighbors(top_chunk, s, children)
        except Exception as e:
            raise e

    def answer(self, query, k, s, r):
        new_query = query_rewriting(query, model=self.q_groq).content
        chunks = self.retrieve(new_query, k=k, r=r, s=s)
        response = final_response(query, chunks, self.a_groq)
        return "Response: " + response.content

    def initializer(self):
        self.initialize(PAPERS_DIR / "test_01.pdf")
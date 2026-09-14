from parser import initializer
from chunking import parent_child_chunking
from utilities import serialize_object
from ingest import create_embeddings
from retriever import retriever_interface
from langchain_huggingface import HuggingFaceEmbeddings
import os

model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def initialize(file_path):
    sections = initializer(file_path)
    parent, children = parent_child_chunking(sections)

    if os.path.exists("pkl/children.pkl"):
        os.remove("pkl/children.pkl")

    serialize_object(children, "pkl/children.pkl")
    create_embeddings(children, model)

    print("Embeddings created, saved to pkl/children.pkl")

def retrieve(query, k):
    return retriever_interface(model, query, k=k)

chunks = retrieve("semantic parent sections", k=3)

for c in chunks:
    print(c, end='\n\n')
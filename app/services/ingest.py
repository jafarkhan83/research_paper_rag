from langchain_chroma import Chroma

def create_embeddings(chunks, model):
    print("embedding chunks...")

    Chroma.from_documents(
        documents=chunks,
        embedding=model,
        persist_directory="./chroma_db"
    )

    print("Embeddings created and persisted.")
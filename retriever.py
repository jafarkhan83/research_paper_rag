from langchain_chroma import Chroma
from langchain_community.retrievers import BM25Retriever
from utilities import deserialize_object

def dense_retriever(model, query, k):
    vector_store = Chroma (
        persist_directory="./chroma_db",
        embedding_function=model
    )

    return vector_store.similarity_search(query, k=k)

def sparse_retriever(query, k):
    docs = deserialize_object("pkl/children.pkl")
    retriever = BM25Retriever.from_documents(docs)
    retriever.k = k
    return retriever.invoke(query)

def rrf_fusion(dense_results, sparse_results, k=60):
    resultant_list = [dense_results, sparse_results]
    scores = {}
    documents = {}

    for results in resultant_list:
        for i, doc in enumerate(results, start=1):

            doc_id = doc.metadata['id']

            score = 1 / (i + k)
            scores[doc_id] = scores.get(doc_id, 0) + score

            documents[doc_id] = doc

    ranked_ids = sorted(
        scores,
        key=scores.get,
        reverse=True
    )

    return [documents[doc_id] for doc_id in ranked_ids]

def retriever_interface(model, query, k):
    dense_results = dense_retriever(model, query, k)
    sparse_results = sparse_retriever(query, k)
    return rrf_fusion(dense_results, sparse_results)
from langchain_chroma import Chroma
from langchain_community.retrievers import BM25Retriever
import cohere
import os

def dense_retriever(model, query, k):
    vector_store = Chroma (
        persist_directory="./chroma_db",
        embedding_function=model
    )

    return vector_store.similarity_search(query, k=k)

def sparse_retriever(query, k, docs):
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

def reranker(query, results, r):
    docs = [doc.page_content for doc in results]
    api_key = os.getenv("COHERE_API_KEY")
    co = cohere.ClientV2(api_key=api_key)
    response = co.rerank(
        model='rerank-v4.0-pro',
        query=query,
        documents=docs,
        top_n=r
    )
    return [results[result.index] for result in response.results]

def retriever_interface(model, query, k, r, children):
    if k < 2 or r < 2 or r > k:
        raise ValueError("k must be at least 2, and r must be at least 2 and at most k")
    dense_results = dense_retriever(model, query, k)
    sparse_results = sparse_retriever(query, k, children)
    fused_results = rrf_fusion(dense_results, sparse_results)
    return reranker(query, fused_results, r)
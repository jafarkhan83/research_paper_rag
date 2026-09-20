from langchain_core.prompts import ChatPromptTemplate
import pickle

def get_siblings(section, parent_id, children):
    siblings = []
    for c in children:
        if c.metadata['parent'] == parent_id and c.metadata['section'] == section:
            siblings.append(c)
    return siblings

def find_neighbors(child, s, children):
    if s not in [1, 2, 3]:
        raise ValueError("s must be 1, 2, or 3")
    neighbor_siblings = []

    if s == 1:
        neighbor_siblings.append(child)
        for c in children:
            if c.metadata['parent'] == child.metadata['parent']:
                if (c.metadata['position'] == child.metadata['position'] - 1 or c.metadata['position'] == child.metadata['position'] + 1):
                    neighbor_siblings.append(c)
    elif s == 2:
        neighbor_siblings.append(child)
        neighbor_siblings += get_siblings(child.metadata['section'], child.metadata['parent'], children)
    else:
        neighbor_siblings += get_siblings(child.metadata['section'], child.metadata['parent'], children)
        neighbor_siblings += get_siblings(child.metadata['section'], child.metadata['parent']-1, children)
        neighbor_siblings += get_siblings(child.metadata['section'], child.metadata['parent']+1, children)

    return neighbor_siblings

def serialize_object(obj, file_path):
    with open(file_path, 'wb') as f:
        pickle.dump(obj, f)

def deserialize_object(file_path):
    with open(file_path, 'rb') as f:
        return pickle.load(f)

def query_rewriting(query, model):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are query rewriting component in RAG system.\nRewrite the user question into a concise search query optimized retrieving relevant documents.\nRules:\n - Preserve the user's intent.\n - Keep important entities, dates, products, and terminology.\n - Remove conversational filler.\n - Do not answer question.\n - Return ONLY the rewritten query."),
        ("human", "{query}")
    ])
    rewriter = prompt | model
    try:
        response = rewriter.invoke({"query": query})
    except Exception as e:
        raise e
    return response
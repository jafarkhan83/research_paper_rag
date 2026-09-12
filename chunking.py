from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

def parent_child_chunking(paragraphs):
	child_splitter = RecursiveCharacterTextSplitter(
		chunk_size=800,
		chunk_overlap=120,
		separators=["\n\n", "\n", ". ", " ", ""]
	)

	parents = {}
	children = []
	for i, t in enumerate(paragraphs):
		parents[i] = t

		child_chunks = child_splitter.split_text(t)
		for j, text in enumerate(child_chunks):
			child_doc = Document(page_content=text, metadata={"parent": str(i), "position": str(j)})
			children.append(child_doc)

	return parents, children
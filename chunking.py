from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

def parent_child_chunking(sections):
	child_splitter = RecursiveCharacterTextSplitter(
		chunk_size=800,
		chunk_overlap=120,
		separators=["\n\n", "\n", ". ", " ", ""]
	)

	parents = {}
	children = []
	counter = 0
	for i, section in enumerate(sections):
		text = section['text']
		parents[i] = text

		child_chunks = child_splitter.split_text(text)
		for j, text in enumerate(child_chunks):
			child_doc = Document(page_content=text, metadata={"parent": i, "position": j, "page": section['page'], "id": counter})
			counter += 1
			children.append(child_doc)

	return parents, children
import pymupdf

# Table extraction

def extract_table_caption_position(page):
	tabs = page.find_tables()
	tables = []

	for tab in tabs.tables:
		x0, y0, x1, y1 = tab.bbox

		area = pymupdf.Rect(
			x0,
			max(0, y0-20),
			x1,
			y0
		)
		caption = tab.page.get_text("text", clip=area).strip()
		md = tab.to_markdown()

		tables.append({
			"caption": caption,
			"table": md,
			"rect": pymupdf.Rect(tab.bbox)
		})
	return tables

def text_table_extraction(pdf_path, header_pct=0.10, footer_pct=0.10):
	doc = pymupdf.open(pdf_path)
	results = []

	for page_num, page in enumerate(doc):
		h = page.rect.height
		header_zone = h * header_pct
		footer_zone = h * (1 - footer_pct)

		d = page.get_text("dict")
		blocks = d["blocks"]
        
		removed = []
		body = ""

		tables = extract_table_caption_position(page)
		is_added = [False] *len(tables)

		for b in blocks:
			if b.get("type") == 1:
				continue # image, non readable text

			for line in b["lines"]:
				text = "".join(span["text"] for span in line["spans"]).strip()
				if not text:
					continue

				# exclude table content
				line_rect = pymupdf.Rect(line["bbox"])
				is_table = False

				for i, table in enumerate(tables):
					if table["rect"].intersects(line_rect):
						if not is_added[i]:
							table = table["table"]
							body += "\n" + "Detected\n\n" + table + "\n"
							is_added[i] = True
						is_table = True

				if is_table: continue

				y0, y1 = line["bbox"][1], line["bbox"][3]

				if y1 <= header_zone or y0 >= footer_zone:
					removed.append(text)
				else:
					body += f"\n{text}"


		results.append({
            		"page": page_num + 1,
			"text": body,
            		"removed": "\n".join(removed)
        		})
	return results

# divide the paper into sections
headings = ["abstract", "introduction", "problem statement", "objectives", "methodology", "results and discussion", "conclusion", "references"]
paragraphs = []

# heading extraction recursive
def extract_name(t, c, paragraph):

	name = headings[c]

	for index in range(len(t)-len(name)):
		buffer = t[index: len(name)+index]
		if name == buffer.lower():
			paragraphs.append(paragraph)
			t = t[index+len(name):]

			if c+1 < len(headings):
				extract_name(t, c+1, name)
			else:
				paragraphs.append(name + t)
			break
		else:
			paragraph += t[index]
	return

def extract_sections(pages):
	sections = []
	c = 0
	name = headings[c]
	p = {}
	
	for page in pages:
		p = {
			"page": page["page"],
			"text": "",
			"section": ""
		}
		if c != 0: p['section'] = sections[-1]['section']
		text = page['text']
		index = 0

		while index < len(text):
			buffer = text[index: index + len(name)]
			if name == buffer.lower():
				index += len(name)
				if p["text"]:
					sections.append(p)
				p = {
					"page": page["page"],
					"text": name + " ",
					"section": name
				}
				c += 1
				if c < len(headings):
					name = headings[c]
			else:
				p["text"] += text[index]
				index += 1

		if p["text"]:
			sections.append(p)

	return sections

def initializer(file_path):
	# load the data
    data = text_table_extraction(file_path)
    return extract_sections(data)
class TextChunker:

    """Splits cleaned text into overlapping paragraph-aware chunks."""
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def create_chunks(self, page_texts):

        chunks = []
        chunk_id = 1

        for page in page_texts:

            page_number = page["page"]
            text = page["text"]

            paragraphs = text.split("\n\n")

            current_chunk = ""
            start = 0

            for paragraph in paragraphs:

                paragraph = paragraph.strip()

                if not paragraph:
                    continue

                if len(current_chunk) + len(paragraph) <= self.chunk_size:

                    current_chunk += paragraph + "\n\n"

                else:

                    end = start + len(current_chunk)

                    chunks.append({
                        "chunk_id": chunk_id,
                        "page": page_number,
                        "text": current_chunk.strip(),
                        "start": start,
                        "end": end
                    })

                    overlap_text = current_chunk[-self.chunk_overlap:]

                    current_chunk = overlap_text + paragraph + "\n\n"

                    start = max(0, end - self.chunk_overlap)
                    chunk_id += 1

            if current_chunk:

                chunks.append({
                    "chunk_id": chunk_id,
                    "page": page_number,
                    "text": current_chunk.strip(),
                    "start": start,
                    "end": start + len(current_chunk)
                })

                chunk_id += 1

        return chunks
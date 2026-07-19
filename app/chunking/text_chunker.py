class TextChunker:
    """
    Splits cleaned text into overlapping chunks.
    """

    def __init__(self, chunk_size=1000, chunk_overlap=200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk(self, text: str):
        chunks = []

        start = 0
        chunk_id = 1

        while start < len(text):

            end = min(start + self.chunk_size, len(text))

            chunk_text = text[start:end]

            chunks.append({
                "chunk_id": chunk_id,
                "text": chunk_text,
                "start": start,
                "end": end
            })

            start += self.chunk_size - self.chunk_overlap
            chunk_id += 1

        return chunks
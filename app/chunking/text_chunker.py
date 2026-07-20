class TextChunker:

    """Splits cleaned text into overlapping paragraph-aware chunks."""
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk(self, text: str):

        paragraphs = text.split("\n\n")

        chunks = []
        current_chunk = ""
        chunk_id = 1
        start = 0

        for paragraph in paragraphs:

            paragraph = paragraph.strip()

            if not paragraph:
                continue

            # If adding this paragraph stays within the limit
            if len(current_chunk) + len(paragraph) <= self.chunk_size:

                current_chunk += paragraph + "\n\n"

            else:

                end = start + len(current_chunk)

                chunks.append({
                    "chunk_id": chunk_id,
                    "text": current_chunk.strip(),
                    "start": start,
                    "end": end
                })

                overlap = current_chunk[-self.chunk_overlap:]

                current_chunk = overlap + paragraph + "\n\n"

                start = end - self.chunk_overlap

                chunk_id += 1

        # Save last chunk
        if current_chunk:

            chunks.append({
                "chunk_id": chunk_id,
                "text": current_chunk.strip(),
                "start": start,
                "end": start + len(current_chunk)
            })

        return chunks
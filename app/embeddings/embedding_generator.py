from sentence_transformers import SentenceTransformer


class EmbeddingGenerator:
    """
    Generates semantic embeddings for text chunks.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Load the embedding model.

        Args:
            model_name (str): Hugging Face sentence transformer model.
        """
        print(f"Loading embedding model: {model_name}...")

        self.model = SentenceTransformer(model_name)

        print("Embedding model loaded successfully.\n")

    def generate(self, chunks):
        """
        Generate embeddings for all chunks.

        Args:
            chunks (list): List of chunk dictionaries.

        Returns:
            list: Chunk dictionaries with embeddings.
        """

        embedded_chunks = []

        for chunk in chunks:

            embedding = self.model.encode(
                chunk["text"],
                convert_to_numpy=True
            )

            embedded_chunks.append({
                "chunk_id": chunk["chunk_id"],
                "page": chunk["page"], 
                "text": chunk["text"],
                "start": chunk["start"],
                "end": chunk["end"],
                "embedding": embedding
            })

        return embedded_chunks
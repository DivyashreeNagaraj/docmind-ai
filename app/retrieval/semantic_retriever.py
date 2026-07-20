from sentence_transformers import SentenceTransformer


class SemanticRetriever:
    """
    Retrieves the most relevant document chunks
    based on semantic similarity.
    """

    def __init__(self, collection):

        self.collection = collection
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def search(self, query, top_k=3):

        query_embedding = self.model.encode(query).tolist()

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        return results
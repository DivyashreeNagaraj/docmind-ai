from sentence_transformers import SentenceTransformer

class SemanticRetriever:
    """
    Retrieves the most relevant document chunks
    based on semantic similarity.
    """

    def __init__(self, vector_store):

        self.collection = vector_store.collection
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def retrieve(self, query, top_k=3):

        query_embedding = self.model.encode(query).tolist()

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        retrieved_chunks = []

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]

        for document, metadata in zip(documents, metadatas):

            retrieved_chunks.append(
                {
                    "text": document,
                    "metadata": metadata
                }
            )

        return retrieved_chunks
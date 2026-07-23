import chromadb


class VectorStore:
    """
    Stores and retrieves document embeddings using ChromaDB.
    """

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path="data/vector_db"
        )

        self.collection = self.client.get_or_create_collection(
            name="documents"
        )

    def clear_collection(self):
        """
        Deletes all documents from the collection.
        """

        try:
            self.client.delete_collection("documents")
        except Exception:
            # Collection may not exist yet
            pass

        self.collection = self.client.get_or_create_collection(
            name="documents"
        )

    def add_documents(self, embedded_chunks):
        """
        Store embedded document chunks in ChromaDB.

        Args:
            embedded_chunks (list): List of chunk dictionaries containing
            text, metadata, and embeddings.
        """
        ids = []
        documents = []
        embeddings = []
        metadatas = []

        for chunk in embedded_chunks:

            ids.append(str(chunk["chunk_id"]))

            documents.append(chunk["text"])

            embeddings.append(chunk["embedding"].tolist())

            metadatas.append(
                {
                    "start": int(chunk["start"]),
                    "end": int(chunk["end"]),
                    "page": int(chunk["page"])
                }
            )

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )

        return len(ids)
    def count(self):

        return self.collection.count()    
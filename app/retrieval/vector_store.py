import chromadb
from chromadb.config import Settings


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

    def add_documents(self, embedded_chunks):

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

        print(embedded_chunks[0])
        print(metadatas[0])
        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )

        print(f"{len(ids)} chunks stored successfully.")

    def count(self):

        return self.collection.count()
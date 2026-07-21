from email import generator

from app.embeddings import embedding_generator
from app.ingestion.document_loader import DocumentLoader
from app.preprocessing.text_preprocessor import TextPreprocessor
from app.chunking.text_chunker import TextChunker
from app.embeddings.embedding_generator import EmbeddingGenerator
from app.retrieval import vector_store
from app.retrieval.vector_store import VectorStore
from app.retrieval.semantic_retriever import SemanticRetriever
from app.generation.answer_generator import AnswerGenerator

def main():
    # Step 1: Load the PDF
    loader = DocumentLoader()
    document = loader.load_pdf("data/raw/sample.pdf")

    # Step 2: Clean the extracted text
    preprocessor = TextPreprocessor()
    clean_text = preprocessor.clean(document["text"])
    clean_text = preprocessor.remove_front_matter(clean_text)

    # Step 3: Split text into chunks
    chunker = TextChunker(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = chunker.chunk(document["page_texts"])

    # generate embeddings for the chunks
    embedding_generator = EmbeddingGenerator()
    embedded_chunks = embedding_generator.generate(chunks)

    # Store embeddings in vector database
    vector_store = VectorStore()
    vector_store.add_documents(embedded_chunks)

    #create a semantic retriever and search for relevant chunks based on a query
    retrieve = SemanticRetriever(vector_store.collection)

    #user input for query
    query = input("\nEnter your question: ")

    #retrieve relevant chunks based on the query
    results = retrieve.search(query)

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    # Display document information
    print("\nDocument Information")
    print("=" * 60)
    print(f"Filename : {document['filename']}")
    print(f"Pages    : {document['pages']}")
    print(f"Characters: {len(document['text'])}")

    # Display chunk information
    print("\nChunk Information")
    print("=" * 60)
    print(f"\nTotal Chunks: {len(embedded_chunks)}")

    # Display embedding information
    print("\nEmbedding Information")
    print("=" * 60)
    print(f"Embedding Dimension : {len(embedded_chunks[0]['embedding'])}")

    print("\nFirst 10 Values of First Embedding:\n")
    print(embedded_chunks[0]["embedding"][:10])
   
     # Database statistics
    print("\nDatabase Statistics")
    print("=" * 60)
    print(f"Stored Chunks : {vector_store.count()}")

    # Retrieval results
    print("\nTop Relevant Chunks")
    print("=" * 60)


    # for chunk in embedded_chunks[:3]:      # Display first 3 chunks only
    #     print("\n" + "=" * 60)
    #     print(f"Chunk {chunk['chunk_id']}")
    #     print("=" * 60)
    #     print(chunk["text"][:300])   # Preview first 300 characters


    for i, (doc, meta, distance) in enumerate(
        zip(documents, metadatas, distances), start=1):

        print(f"\nResult {i}")
        print("-" * 40)
        print(f"Distance: {distance:.4f}")
        print(f"Start: {meta['start']}")
        print(f"End: {meta['end']}")
        print(doc[:400])

    # Build context for LLM
    context = "\n\n".join(documents)

    # Generate answer
    generator = AnswerGenerator()
    answer = generator.generate(query, context)

    print("\nGenerated Answer")
    print("=" * 60)
    print(answer)

    print("\nSources")
    print("=" * 60)

    for i, meta in enumerate(metadatas, start=1):
        print(
            f"Source {i}: "
            f"Page {meta.get('page', 'Unknown')} "
            f"(Characters {meta['start']} - {meta['end']})"
        )


if __name__ == "__main__":
    main()
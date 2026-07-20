from app.embeddings import embedding_generator
from app.ingestion.document_loader import DocumentLoader
from app.preprocessing.text_preprocessor import TextPreprocessor
from app.chunking.text_chunker import TextChunker
from app.embeddings.embedding_generator import EmbeddingGenerator

def main():
    # Step 1: Load the PDF
    loader = DocumentLoader()
    document = loader.load_pdf("data/raw/sample.pdf")

    # Step 2: Clean the extracted text
    preprocessor = TextPreprocessor()
    clean_text = preprocessor.clean(document["text"])

    # Step 3: Split text into chunks
    chunker = TextChunker(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = chunker.chunk(clean_text)
    embedding_generator = EmbeddingGenerator()

    embedded_chunks = embedding_generator.generate(chunks)

    # Display document information
    print(f"Filename : {document['filename']}")
    print(f"Pages    : {document['pages']}")
    print(f"Characters: {len(document['text'])}")

    # Display chunk information
    print(f"\nTotal Chunks: {len(embedded_chunks)}")

    print("\nEmbedding Information")
    print("=" * 60)

    print(f"Embedding Dimension : {len(embedded_chunks[0]['embedding'])}")

    print("\nFirst 10 Values of First Embedding:\n")

    print(embedded_chunks[0]["embedding"][:10])


    for chunk in embedded_chunks[:3]:      # Display first 3 chunks only
        print("\n" + "=" * 60)
        print(f"Chunk {chunk['chunk_id']}")
        print("=" * 60)
        print(chunk["text"][:300])   # Preview first 300 characters

if __name__ == "__main__":
    main()
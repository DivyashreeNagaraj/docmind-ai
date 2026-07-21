import streamlit as st
from pathlib import Path

from app.ingestion.document_loader import DocumentLoader
from app.preprocessing.text_preprocessor import TextPreprocessor
from app.chunking.text_chunker import TextChunker
from app.embeddings.embedding_generator import EmbeddingGenerator
from app.retrieval.vector_store import VectorStore
from app.retrieval.semantic_retriever import SemanticRetriever
from app.generation.answer_generator import AnswerGenerator

st.set_page_config(
    page_title="DocMind AI",
    page_icon="📄",
    layout="wide"
)

st.title("📄 DocMind AI")
st.subheader("AI Research Assistant with RAG")

st.write(
    """
Upload a PDF, ask questions, and receive AI-generated answers
grounded in the uploaded document.
"""
)

uploaded_file = st.file_uploader(
    "Upload a PDF",
    type=["pdf"]
)

question = st.text_input("Ask a question")

if st.button("Generate Answer"):

    if uploaded_file is None:
        st.warning("Please upload a PDF first.")

    elif question == "":
        st.warning("Please enter a question.")

    else:

        save_path = Path("data/raw") / uploaded_file.name

        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        with st.spinner("Processing document..."):
            
            # Step 1: Load the PDF
            loader = DocumentLoader()
            document = loader.load_pdf(str(save_path))

            # Step 2: Clean the extracted text
            preprocessor = TextPreprocessor()
            for page in document["page_texts"]:
                page["text"] = preprocessor.clean(page["text"])
                page["text"] = preprocessor.remove_front_matter(page["text"])


            # Step 3: Split text into chunks
            chunker = TextChunker()
            chunks = chunker.chunk(document["page_texts"])

            st.write(f"Total Chunks: {len(chunks)}")


            # Step 4: Generate embeddings for the chunks
            embedding_generator = EmbeddingGenerator()
            embedded_chunks = embedding_generator.generate(chunks)

            # Step 5: Store embeddings in vector database
            vector_store = VectorStore()
            vector_store.add_documents(embedded_chunks)

            # Step 6: Create a semantic retriever and search for relevant chunks based on the query
            retriever = SemanticRetriever(vector_store.collection)
            results = retriever.search(question)

            documents = results["documents"][0]
            metadatas = results["metadatas"][0]
            
            context = "\n\n".join(documents)

            # Answer Generation
            generator = AnswerGenerator()
            answer = generator.generate(question, context)

            # Display document information
            st.success("Answer generated successfully!")
            st.write(answer)
            st.subheader("Generated Answer")
            st.subheader("Sources")

            for i, meta in enumerate(metadatas, start=1):
                st.write(
                    f"Source {i}: Page {meta.get('page', 'Unknown')} "
                    f"(Characters {meta['start']} - {meta['end']})"
                )
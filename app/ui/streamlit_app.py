import streamlit as st
from pathlib import Path

from app.ingestion.document_loader import DocumentLoader
from app.preprocessing.text_preprocessor import TextPreprocessor
from app.chunking.text_chunker import TextChunker
from app.embeddings.embedding_generator import EmbeddingGenerator
from app.retrieval.vector_store import VectorStore
from app.retrieval.semantic_retriever import SemanticRetriever
from app.generation.answer_generator import AnswerGenerator



# ---------------------------------------------------------
# Initialize Variables
# ---------------------------------------------------------

retrieved_chunks = []
answer = ""
filename = ""
pages = 0
chunks = []

BASE_DIR = Path(__file__).resolve().parent.parent
LOGO = BASE_DIR / "assets" / "docmind_logo.png"

# Page Configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="DocMind AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)
# Sidebar
with st.sidebar:
    st.image(LOGO, width= 170)

    st.markdown("---")

    st.markdown("### ✨ AI Research Assistant")

    st.write(
        """
Upload research papers and ask questions using
Retrieval-Augmented Generation (RAG).

### Features

- 📄 PDF Upload
- 🧠 Semantic Search
- ⚙️ AI Answer Generation
- 📚 Source Citations
- 🗄️ ChromaDB Vector Search
"""
    )

    # Header

header_col1, header_col2 = st.columns([1, 5])

with header_col1:
    st.image(LOGO, width=190)

with header_col2:

    st.title("DocMind AI")

    st.caption(
        "AI Research Assistant with Retrieval-Augmented Generation"
    )

    st.write(
        "Upload a PDF, ask questions, and receive AI-powered answers grounded in your document."
    )

st.divider()


# Layout

st.markdown("## 📂 Upload & Query")
with st.container(border=True):
    left, right = st.columns([1, 2], gap="large")

    with left:

        st.markdown("### 📂 Upload Document")

        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type=["pdf"],
            help="Upload a research paper or PDF document."
            )

    with right:

        st.markdown("### 💬 Ask a Question")

        question = st.text_input(
             "",
            placeholder="Example: What is the main objective of this paper?"
        )

        st.write("")
        generate = st.button(
            "🚀 Generate Answer",
            use_container_width=True,
            type="primary"

        )

st.write("")

#RAG Pipeline
if generate:

    if uploaded_file is None:
        st.warning(" ⚠️ Please upload a PDF first.")
        st.stop()


    if not question.strip():
        st.warning(" ⚠️ Please enter a question.")
        st.stop()

    with st.spinner("🧠 Processing document..."):

            
            # Step 1: Load the PDF
            loader = DocumentLoader()
            document = loader.load_document(uploaded_file)

            filename = document["filename"]
            pages = document["pages"]
            page_texts = document["page_texts"]

            # Step 2: Clean the extracted text
            preprocessor = TextPreprocessor()
            cleaned_pages = [
                {
                    "page": page["page"],
                    "text": preprocessor.clean(page["text"])
                }
                for page in page_texts
            ]

            # Step 3: Split text into chunks
            chunker = TextChunker(
                chunk_size=500,
                chunk_overlap=100
            )
        
            # Step 4: Generate embeddings for the chunks
            embedding_generator = EmbeddingGenerator()
            chunks = chunker.create_chunks(cleaned_pages)
            embedded_chunks = embedding_generator.generate_embeddings(chunks)

            # Step 5: Store embeddings in vector database
                    # Store in ChromaDB
            vector_store = VectorStore()
            vector_store.clear_collection()
            vector_store.add_documents(embedded_chunks)

            # Step 6: Create a semantic retriever and search for relevant chunks based on the query
            retriever = SemanticRetriever(vector_store)
            retrieved_chunks = retriever.retrieve(
            question,
            top_k=3)

            # Answer Generation
            generator = AnswerGenerator()
            answer = generator.generate_answer(question, retrieved_chunks)

# ---------------------------------------------------------
# Document Information
# ---------------------------------------------------------

            st.divider()

            st.subheader("📄 Document Information")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("📄 Document", filename)

            with col2:
                st.metric("📑 Pages", pages)

            with col3:
                st.metric("🧩 Chunks", len(chunks))


        # Question

            st.subheader("❓ Question")

            with st.container(border=True):
                st.write(question)


        # Answer

            st.subheader(" 🤖 AI Generated Answer")

            with st.chat_message("assistant"):
            
        # Sources

                st.subheader("📚 Sources")

            if retrieved_chunks:

                for index, chunk in enumerate(retrieved_chunks, start=1):

                    page = chunk["metadata"].get("page", "Unknown")

                    with st.expander(
                        f"📄 Source {index} • Page {page}"
                    ):

                        st.caption(f"Retrieved Context • Page {page}")

                        st.markdown(chunk["text"])

            else:

                st.info("No supporting context found.")

    # ---------------------------------------------------------
# Footer
# ---------------------------------------------------------

st.markdown(
    """
<div style="text-align:center; padding:10px; color:#9ca3af;">

<b style="font-size:22px;">🤖 DocMind AI</b><br><br>

AI Research Assistant powered by Retrieval-Augmented Generation (RAG)<br><br>

<b>Tech Stack:</b> Streamlit • ChromaDB • Sentence Transformers • Ollama • Python<br><br>

© 2026 DocMind AI • All Rights Reserved

</div>
""",
    unsafe_allow_html=True
)
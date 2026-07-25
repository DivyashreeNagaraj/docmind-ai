import streamlit as st
from pathlib import Path
import time

from sympy import false

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
    st.image(LOGO,use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("### ✨ AI Research Assistant")

    st.write(
        """
Upload research papers and ask questions using
Retrieval-Augmented Generation (RAG).

### Features

- 📄 PDF Upload
- 🔍 Semantic Search
- ⚙️ AI Answer Generation
- 📚 Source Citations
- 🗄️ ChromaDB Vector Search
"""
    )
    st.markdown("---")

    st.markdown("### ⚙️ Technology")

    st.write("""
- 🖥️ Framework: Streamlit
- 🧬 Embeddings: all-MiniLM-L6-v2
- 🗄️ Vector DB: ChromaDB
- 🌀 LLM: Ollama
- 🐍 Language: Python
""")

    # Header

# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

st.markdown(
    """
    <h1 style="text-align:center; margin-bottom:0;">
        🧠 DocMind AI
    </h1>

    <p style="text-align:center; color:#9ca3af; font-size:18px;">
        AI Research Assistant with Retrieval-Augmented Generation
    </p>

    <p style="text-align:center; font-size:20px;">
        Upload a PDF, ask intelligent questions, and receive AI-powered answers grounded in your document.
    </p>
    """,
    unsafe_allow_html=True,
)

# Technology badges

st.markdown(
    """
    <div style="text-align:center; font-size:18px; margin-top:20px;">
        🚀 <b>Streamlit</b>
        &nbsp;&nbsp;&nbsp;&nbsp;
        🧬 <b>Embeddings</b>
        &nbsp;&nbsp;&nbsp;&nbsp;
        🗄️ <b>ChromaDB</b>
        &nbsp;&nbsp;&nbsp;&nbsp;
        🌀 <b>Ollama</b>
        &nbsp;&nbsp;&nbsp;&nbsp;
        🐍 <b>Python</b>
    </div>
    """,
    unsafe_allow_html=True,
)


# Layout

st.markdown("## 🚀 Document Analysis")
with st.container(border=True):
    left, right = st.columns([1, 2], gap="large")

    with left:

        st.markdown("###  📤 Upload Document")

        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type=["pdf"],
            help="Upload a research paper or PDF document."
            )

    with right:

        st.markdown("### 💬 Ask a Question")
        with st.form("question_form"):

            question = st.text_input(
                "",
                placeholder="Example: What is the main objective of this paper?"
            )

            generate = st.form_submit_button(
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


    if len(question.strip()) < 3:
        st.warning(" ⚠️ Please enter a question.")
        st.stop()

    try:
        start_time = time.time()
        # Progress Bar
        progress = st.progress(0)
        status = st.empty()

        status.info("📄 Reading PDF...")
        progress.progress(10)

            
        # Step 1: Load the PDF
        loader = DocumentLoader()
        document = loader.load_document(uploaded_file)

        if not document["text"].strip():
            st.error("❌ No readable text found in the uploaded PDF.")
            st.stop()

        filename = document["filename"]
        pages = document["pages"]
        page_texts = document["page_texts"]

        status.info("🧹 Cleaning extracted text...")
        progress.progress(25)

        # Step 2: Clean the extracted text
        preprocessor = TextPreprocessor()
        cleaned_pages = [
            {
                "page": page["page"],
                "text": preprocessor.clean(page["text"])
            }
            for page in page_texts
        ]

        status.info("✂️ Creating text chunks...")
        progress.progress(45)

        # Step 3: Split text into chunks
        chunker = TextChunker(
            chunk_size=500,
            chunk_overlap=100
        )
        chunks = chunker.create_chunks(cleaned_pages)

        status.info("🧬 Generating embeddings...")
        progress.progress(65)
        
        # Step 4: Generate embeddings for the chunks
        embedding_generator = EmbeddingGenerator()
        embedded_chunks = embedding_generator.generate_embeddings(chunks)

        status.info("🗄️ Building vector database...")
        progress.progress(80)

        # Step 5: Store embeddings in vector database
                # Store in ChromaDB
        vector_store = VectorStore()
        vector_store.clear_collection()
        vector_store.add_documents(embedded_chunks)

        status.info("🔍 Searching relevant information...")
        progress.progress(90)

        # Step 6: Create a semantic retriever and search for relevant chunks based on the query
        retriever = SemanticRetriever(vector_store)
        retrieved_chunks = retriever.retrieve(
        question,
        top_k=3)

        # Answer Generation
        generator = AnswerGenerator()
        answer = generator.generate_answer(question, retrieved_chunks)
        end_time = time.time()
        processing_time = end_time - start_time

        progress.progress(100)
        status.success("✅ Analysis completed successfully!")
        st.toast("🎉 Answer generated successfully!")

        progress.empty()
        status.empty()


        # Document Information


        st.divider()

        st.subheader("📊 Document Information")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.write("**📄 Document**")
            st.caption(filename)

        with col2:
            st.write("**📑 Pages**")
            st.caption(pages)

        with col3:
            st.write("**🧩 Chunks**")
            st.caption(len(chunks))

    
        # Document Preview

        st.subheader("📄 Document Preview")

        preview = document["text"][:800]

        st.text_area(
            "",
            value=preview,
            height=220,
            disabled=True
        )


        # Question

        st.subheader("💬User Question")

        with st.container(border=True):
                st.write(question)


        # Answer

        st.subheader(" 💡 AI Generated Answer")

        with st.container(border=True):
                st.markdown(answer)

        download_content = f"""
        DocMind AI

        Question:
        {question}

        ----------------------------------------

        Answer:
        {answer}
        """
        st.download_button(
            label="📥 Download Answer",
            data=download_content,
            file_name="DocMind_AI_Answer.txt",
            mime="text/plain",
            use_container_width=True
        )

        st.subheader("📊 Processing Statistics")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("🧩 Chunks Created", len(chunks))

        with col2:
            st.metric("📚 Chunks Retrieved", len(retrieved_chunks))

        with col3:
            st.metric("⏱ Processing Time", f"{processing_time:.2f}s")

        with st.container(border=True):

            st.write("**🧬 Embedding Model:** all-MiniLM-L6-v2")

            st.write("**🗄️ Vector Database:** ChromaDB")  

        # Sources

        st.subheader("📚 Sources")

        if retrieved_chunks:

                for index, chunk in enumerate(retrieved_chunks, start=1):

                    page = chunk["metadata"].get("page", "Unknown")

                    with st.expander(
                        f"📄 Source {index} • Page {page}"
                    ):
                        st.caption(f"Retrieved Context • Page {page}")

                        preview = chunk["text"]

                        if len(preview) > 700:
                            preview = preview[:700] + "..."

                        st.markdown(preview)

        else:

                st.info("No supporting context found.")

    except Exception as e:

        st.error("❌ Something went wrong while processing the document.")

        st.exception(e)

    # ---------------------------------------------------------
# Footer
# ---------------------------------------------------------

st.markdown(
    """
<div style="text-align:center; padding:10px; color:#9ca3af;">

<b style="
font-size:28px;
font-weight:700;
color:#FFFFFF;
">
🧠 DocMind <span style="color:#4DA3FF;">AI</span>
</b>

AI Research Assistant powered by Retrieval-Augmented Generation (RAG)<br><br>

<b>Tech Stack:</b> Streamlit • ChromaDB • Sentence Transformers • Ollama • Python<br><br>

© 2026 DocMind AI • All Rights Reserved

</div>
""",
    unsafe_allow_html=True
)
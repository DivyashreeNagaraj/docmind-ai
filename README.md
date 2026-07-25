# 🤖 DocMind AI

<p align="center">
  <img src="app/assets/docmind_logo.png" width="220">
</p>

<h2 align="center">AI Research Assistant with Retrieval-Augmented Generation (RAG)</h2>

<p align="center">
Upload PDF documents, perform semantic search, and receive AI-generated answers grounded in your documents.
</p>

---

## 🚀 Overview

DocMind AI is an AI-powered research assistant that enables users to upload PDF documents and ask natural language questions. It uses a Retrieval-Augmented Generation (RAG) pipeline to retrieve the most relevant document passages before generating accurate, context-aware responses with source citations.

---

## ✨ Features

- 📄 Upload and analyze PDF documents
- 🧹 Automatic text preprocessing
- ✂️ Intelligent text chunking
- 🧬 Sentence Transformer embeddings
- 🗄️ ChromaDB vector database
- 🔍 Semantic similarity search
- 🤖 AI-powered answer generation using Ollama
- 📚 Source citations with page numbers
- 📊 Processing statistics
- 📥 Download generated answers
- 🌙 Modern Streamlit interface

---

## 💬 Example Questions

- What is the main objective of this paper?
- Summarize the introduction.
- Explain the proposed methodology.
- What datasets were used?
- What are the key findings?
- What limitations are discussed?
- Compare the proposed approach with existing methods.
- What future work is suggested?

---

## 🏗️ Architecture

```text
PDF
 │
 ▼
Document Loader
 │
 ▼
Text Preprocessing
 │
 ▼
Chunking
 │
 ▼
Embeddings
 │
 ▼
ChromaDB
 │
 ▼
Semantic Retrieval
 │
 ▼
Ollama (Llama 3.2)
 │
 ▼
Answer + Citations
```

---

## 🛠️ Tech Stack

- Python
- Streamlit
- ChromaDB
- Sentence Transformers (all-MiniLM-L6-v2)
- Ollama
- PyPDF

---

## ▶️ Run Locally

```bash
git clone https://github.com/DivyashreeNagaraj/docmind-ai.git

cd docmind-ai

pip install -r requirements.txt

streamlit run app/ui/streamlit_app.py
```

---

## 👩‍💻 Author

**Divyashree Nagaraj**

Master's Student in Artificial Intelligence

---

## 📄 License

This project is licensed under the MIT License.
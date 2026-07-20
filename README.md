# DocMind AI

An AI-powered document intelligence platform that enables semantic search, Retrieval-Augmented Generation (RAG), and grounded question answering over enterprise documents.

---

## 🚀 Features

### ✅ Implemented
- PDF document loading
- Multi-page text extraction
- Document metadata extraction
- Modular project architecture

### 🔄 In Progress
- Text preprocessing
- Intelligent document chunking
- Embedding generation
- Vector database integration
- Semantic retrieval
- RAG pipeline
- Evaluation framework
- Streamlit interface
- Deployment

---

## 🏗️ System Architecture

```text
PDF
   │
   ▼
Document Loader
   │
   ▼
Text Preprocessor
   │
   ▼
Chunking
   │
   ▼
Embeddings
   │
   ▼
Vector Database
   │
   ▼
Retriever
   │
   ▼
LLM
   │
   ▼
Response with Citations
```

---

## 📂 Project Structure

```text
docmind-ai/
│
├── app/
│   ├── ingestion/
│   ├── preprocessing/
│   ├── chunking/
│   ├── embeddings/
│   ├── retrieval/
│   ├── generation/
│   ├── evaluation/
│   ├── ui/
│   └── utils/
│
├── data/
├── docs/
├── notebooks/
├── tests/
│
├── main.py
├── requirements.txt
└── README.md
```

---

## 🛠️ Tech Stack

- Python
- PyPDF
- ChromaDB *(planned)*
- Sentence Transformers *(planned)*
- OpenAI / Anthropic APIs *(planned)*
- Streamlit *(planned)*

---

## 📅 Development Status

- [x] Project initialization
- [x] Project structure
- [x] PDF document loader
- [x] Text preprocessing
- [x] Intelligent chunking
- [x] Embedding generation
- [ ] Vector database
- [ ] Semantic retrieval
- [ ] RAG pipeline
- [ ] Evaluation framework
- [ ] Streamlit UI
- [ ] Deployment
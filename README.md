# Sehat-Fahm: AI-Powered Medical Lab Report Analysis System
Inside HealthAgent File

## Overview

**Sehat-Fahm** (سہت فہم) is an intelligent multi-agent system designed to automate medical lab report analysis and provide accessible health insights. The system leverages advanced AI technologies including LangGraph multi-agent orchestration, RAG (Retrieval-Augmented Generation) pipelines, and natural language processing to make medical information understandable for non-medical users, with special emphasis on Urdu language accessibility.

## Key Features

### 🤖 Multi-Agent Architecture
- **LangGraph-based Agent System**: Engineered a sophisticated multi-agent workflow using LangGraph to orchestrate specialized AI agents
- **Two Specialized Agents**:
  - **Extractor Agent**: Extracts comprehensive textual content from medical PDF reports without summarization or interpretation
  - **Doctor Agent**: Analyzes extracted reports and provides detailed, easy-to-understand medical insights

### 🧠 RAG Pipeline with Research-Backed Knowledge
- **ChromaDB Vector Store**: Persistent vector database storing medical knowledge from MedlinePlus
- **HuggingFace Embeddings**: Uses `all-MiniLM-L6-v2` model for semantic search and document retrieval
- **MedlinePlus Integration**: Automated web crawler that ingests medical lab test information from MedlinePlus.gov
- **PubMed Integration**: Access to up-to-date medical research through PubMed query tool

### 🌐 Urdu Language Accessibility
- **Google Translator Integration**: Automatic translation of medical insights from English to Urdu
- **Text-to-Speech (gTTS)**: Converts Urdu text to natural speech for audio playback
- **Bilingual Interface**: Streamlit UI supports both English and Urdu display

### 🎨 Real-Time Streamlit Interface
- **Interactive Web Application**: Modern, user-friendly interface for uploading and analyzing medical reports
- **Real-Time Processing**: Live analysis with progress indicators
- **Audio Playback**: Integrated audio player for Urdu voice output

## Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit UI (app.py)                     │
│  - PDF Upload Interface                                      │
│  - Urdu Translation & Voice Generation                      │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              LangGraph Workflow (main.py)                    │
│  ┌──────────────────┐         ┌──────────────────┐          │
│  │  PDF Extractor   │ ──────▶ │  Doctor Agent    │          │
│  │     Agent        │         │                  │          │
│  └──────────────────┘         └──────────────────┘          │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   ChromaDB   │ │    PubMed    │ │     Groq      │
│  Vector Store│ │     Tool     │ │      LLM      │
└──────────────┘ └──────────────┘ └──────────────┘
```

### Technology Stack

- **LLM**: Groq (Meta Llama 4 Maverick 17B 128E Instruct)
- **Agent Framework**: LangGraph, LangChain
- **Vector Database**: ChromaDB
- **Embeddings**: HuggingFace Transformers (all-MiniLM-L6-v2)
- **Web Framework**: Streamlit
- **Translation**: Google Translator (deep-translator)
- **Text-to-Speech**: Google Text-to-Speech (gTTS)
- **PDF Processing**: PyPDFLoader (LangChain)
- **Web Scraping**: BeautifulSoup, Requests

## Project Structure

```
Sehat-Fahm/
├── agents.py                      # Agent definitions and executors
├── app.py                         # Streamlit web application
├── CrawlerAndChromaDBIngestor.py  # MedlinePlus crawler and vector store builder
├── main.py                        # LangGraph workflow definition
├── memory.py                      # Conversation memory management
├── prompts.py                     # Agent prompt templates
├── tools.py                       # Custom tools (PDF extractor, retriever)
├── testAudio.py                   # Audio generation testing
├── testVectorStore.py             # Vector store testing
└── README.md                      # This file
```

## Installation

### Prerequisites

- Python 3.8 or higher
- Groq API key
- Internet connection (for MedlinePlus crawling and translation services)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Sehat-Fahm
   ```

2. **Install dependencies**
   ```bash
   pip install langchain langchain-groq langchain-community langchain-chroma langchain-huggingface
   pip install streamlit gtts deep-translator
   pip install beautifulsoup4 requests python-dotenv
   pip install langgraph
   ```

3. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

4. **Build the knowledge base**
   Run the crawler to populate ChromaDB with MedlinePlus data:
   ```bash
   python CrawlerAndChromaDBIngestor.py
   ```
   This will:
   - Crawl up to 1000 pages from MedlinePlus lab-tests section
   - Extract and process medical content
   - Generate embeddings and store in ChromaDB
   - Create `chroma_medlineplus` directory with vector store

5. **Run the Streamlit application**
   ```bash
   streamlit run app.py
   ```

## Usage

### Web Interface

1. **Start the application**: Run `streamlit run app.py`
2. **Upload PDF**: Click "Upload PDF report" and select a medical lab report PDF
3. **Analyze**: Click "🔍 Analyze Report" button
4. **View Results**: 
   - English insights will be displayed first
   - Urdu translation will appear below
   - Click the audio player to hear the Urdu explanation

### Programmatic Usage

You can also use the system programmatically:

```python
from main import app

input_state = {
    "file_path": "path/to/medical_report.pdf",
    "messages": []
}

result = app.invoke(input_state)
print(result["insights"])
```

## How It Works

### 1. PDF Extraction Phase

The **Extractor Agent** receives a PDF file path and:
- Uses the `extract_report_text` tool to load and parse the PDF
- Extracts all textual content without summarization
- Preserves structure, headings, and values
- Returns complete report text to the workflow state

### 2. Medical Analysis Phase

The **Doctor Agent** receives the extracted report text and:
- Analyzes the lab values and medical information
- Uses the ChromaDB retriever tool to find relevant medical context from MedlinePlus
- Optionally queries PubMed for research-backed information
- Generates comprehensive, easy-to-understand explanations
- Returns detailed insights suitable for non-medical users

### 3. Translation & Voice Generation

The Streamlit interface:
- Receives English insights from the workflow
- Translates to Urdu using Google Translator
- Generates Urdu speech audio using gTTS
- Displays both text and audio to the user

## Agent Details

### Extractor Agent

**Purpose**: Extract complete textual content from medical PDF reports

**Tools**:
- `extract_report_text`: PDF loader and text extractor

**Behavior**: 
- Extracts all content without interpretation
- Preserves original structure and formatting
- No summarization or filtering

### Doctor Agent

**Purpose**: Analyze medical reports and provide understandable insights

**Tools**:
- `medlineplus_health_retriever`: Semantic search in ChromaDB knowledge base
- `PubmedQueryRun`: Query PubMed for research articles

**Behavior**:
- Prefers using retriever tool for lab test values and medical conditions
- Uses PubMed only when additional research context is needed
- Avoids unnecessary tool calls when knowledge is sufficient
- Provides detailed, educational explanations for non-medical users

## RAG Pipeline

### Knowledge Base Construction

1. **Web Crawling**: `CrawlerAndChromaDBIngestor.py` crawls MedlinePlus.gov/lab-tests
2. **Content Extraction**: BeautifulSoup extracts text from HTML pages
3. **Document Processing**: 
   - Creates LangChain Document objects with metadata
   - Splits into chunks (1000 chars, 100 char overlap)
4. **Embedding Generation**: HuggingFace embeddings create vector representations
5. **Vector Storage**: ChromaDB stores and persists vectors for retrieval

### Retrieval Process

- Semantic search using similarity matching
- Returns top 3 most relevant documents
- Provides context-aware medical information to the Doctor Agent

## Configuration

### Crawler Settings

In `CrawlerAndChromaDBIngestor.py`:
- `BASE_URL`: MedlinePlus lab-tests base URL
- `MAX_PAGES`: Maximum pages to crawl (default: 1000)
- `CHROMA_DIR`: ChromaDB persistence directory

### Agent Settings

In `agents.py`:
- `model`: Groq model name (default: "meta-llama/llama-4-maverick-17b-128e-instruct")
- `verbose`: Enable verbose logging
- `handle_parsing_errors`: Error handling for agent responses

### Retrieval Settings

In `tools.py`:
- `search_kwargs={"k": 3}`: Number of documents to retrieve
- `model_name`: Embedding model (default: "all-MiniLM-L6-v2")

## Testing

### Test Audio Generation

```bash
python testAudio.py
```

Tests Urdu text-to-speech functionality.

### Test Vector Store

```bash
python testVectorStore.py
```

Tests ChromaDB retrieval functionality with sample queries.

## Limitations & Considerations

1. **API Dependencies**: Requires Groq API key and internet connection for translation
2. **Knowledge Base**: Limited to MedlinePlus content; may not cover all medical conditions
3. **Language Support**: Urdu translation quality depends on Google Translator
4. **PDF Quality**: Extraction quality depends on PDF structure and text encoding
5. **Medical Disclaimer**: This system provides informational insights only and should not replace professional medical advice

## Future Enhancements

- Support for additional languages
- Enhanced PDF parsing for structured reports
- Integration with more medical databases
- User session management and history
- Export functionality for reports
- Mobile-responsive interface
- Offline mode support

## Contributing

Contributions are welcome! Please ensure:
- Code follows existing style conventions
- Comments are removed (as per project standards)
- Tests are added for new features
- Documentation is updated

## License

See LICENSE file for details.

## Acknowledgments

- MedlinePlus for providing comprehensive medical information
- Groq for high-performance LLM inference
- LangChain and LangGraph communities
- HuggingFace for embedding models

---

**Note**: Sehat-Fahm is designed to assist users in understanding medical reports but should never replace professional medical consultation. Always consult with qualified healthcare providers for medical decisions.

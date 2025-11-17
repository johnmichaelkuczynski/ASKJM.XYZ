# Ask a Philosopher - J.-M. Kuczynski AI Assistant

## Overview
This project is an intelligent philosophical conversation application that uses semantic search over J.-M. Kuczynski's works to synthesize thoughtful, streaming responses via Claude AI. Its core purpose is to provide an AI assistant capable of engaging in philosophical dialogue, accurately reflecting Kuczynski's rigorous arguments and writing style, based on a comprehensive database of his philosophical positions. The project aims to make his extensive body of work more accessible and interactive for users interested in in-depth philosophical inquiry.

## User Preferences
- **API Integration**: Prefers direct Anthropic API integration over Replit AI Integrations
- **Response Style**: AI responses must faithfully represent Kuczynski's actual arguments, examples, and rigorous writing style, not glib paraphrases. This means quoting or very closely paraphrasing the actual text from positions, using his exact examples and rhetorical questions, preserving his step-by-step argumentative structure, and matching his rigorous, technical, methodical, and detailed tone. The AI should not summarize, simplify, or "make accessible" his work.
- **Argumentation**: The AI prompt is configured to not argue against user input when they present a position; it defaults to SUPPORT/EXPAND mode, but acknowledges mismatches if retrieved positions conflict.
- **Relevance Assessment**: The AI should check if retrieved positions actually address the user's question before using them, providing an intelligent fallback response consistent with Kuczynski's broader philosophy if no relevant positions exist.

## System Architecture

### Core Functionality
- **Semantic Search**: Indexes 894 philosophical positions using sentence-transformers (all-MiniLM-L6-v2 model) for efficient retrieval.
- **Streaming AI Responses**: Delivers token-by-token responses from various AI providers, ensuring a smooth user experience.
- **Multi-AI Provider Support**: Integrates Anthropic Claude, OpenAI, DeepSeek, and Perplexity, allowing model selection.
- **Content Ingestion**: Supports file uploads (PDF, Word, TXT) with automatic text extraction.
- **User Interface**: Features a clean conversation UI with auto-expanding input, distinct user/AI dialogue, and responsive design.
- **Source Citations**: Automatically includes relevant position IDs (e.g., EP-111, META-033) with each AI response.
- **Conversation Management**: Allows downloading individual exchanges in Markdown or TXT format.
- **Optional Login**: Implements a username-only login system for future chat history features.

### Technical Implementation
- **Backend**: Flask 3.1+ handles the main application logic, SSE streaming, and integration with the semantic search module (`search.py`).
- **Frontend**: A minimal HTML interface (`index.html`) is styled with professional gradients (`style.css`) and powered by vanilla JavaScript (`app.js`) for dynamic interactions and SSE streaming.
- **Data Management**: Philosophical positions are stored in `data/KUCZYNSKI_PHILOSOPHICAL_DATABASE_v28_BLOG_COMPLETE.json` (894 positions). Pre-computed embeddings for these positions are cached in `data/position_embeddings.pkl`. Source texts from Kuczynski's works are stored in the `texts/` directory.
- **ML/NLP**: Utilizes `sentence-transformers`, `scikit-learn`, and CPU-optimized PyTorch for embedding generation and semantic similarity calculations.
- **File Processing**: Employs `PyPDF2` and `python-docx` for extracting text from uploaded documents.

### Key Design Decisions
- **Faithful Representation**: A critical design principle ensures AI responses strictly adhere to Kuczynski's original text, examples, and argumentative style, avoiding summarization or simplification.
- **Token-by-Token Streaming**: Provides immediate and real-time display of AI responses for enhanced user experience.
- **Simplified Data Model**: Focuses on philosophical positions as the primary data points, with potential future integration of full text excerpts.
- **CPU-Only PyTorch**: Optimizes for Replit environment constraints by using CPU-based PyTorch.

## External Dependencies
- **AI Providers**:
    - Anthropic Claude (via direct Anthropic SDK)
    - OpenAI
    - DeepSeek
    - Perplexity
- **Python Libraries**:
    - Flask
    - sentence-transformers
    - scikit-learn
    - PyTorch (CPU)
    - PyPDF2
    - python-docx
    - Gunicorn (for production deployment)
    - gevent (for production deployment)
- **Deployment Platform**: Render.com (configured via `render.yaml`, `runtime.txt`)
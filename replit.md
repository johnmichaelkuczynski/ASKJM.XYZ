# Ask a Philosopher - J.-M. Kuczynski AI Assistant

## Overview
This project is an intelligent philosophical conversation application that uses semantic search over J.-M. Kuczynski's works to synthesize thoughtful, streaming responses via Claude AI. Its core purpose is to provide an AI assistant capable of engaging in philosophical dialogue, accurately reflecting Kuczynski's rigorous arguments and writing style, based on a comprehensive database of his philosophical positions. The project aims to make his extensive body of work more accessible and interactive for users interested in in-depth philosophical inquiry.

## User Preferences
- **API Integration**: Prefers direct Anthropic API integration over Replit AI Integrations
- **Response Style**: AI responses must faithfully represent Kuczynski's actual arguments, examples, and rigorous writing style, not glib paraphrases. This means quoting or very closely paraphrasing the actual text from positions, using his exact examples and rhetorical questions, preserving his step-by-step argumentative structure, and matching his rigorous, technical, methodical, and detailed tone. The AI should not summarize, simplify, or "make accessible" his work.
- **Examples Required**: Kuczynski's writing is replete with concrete examples. AI responses MUST include examples when explaining abstract concepts (propositions, properties, mental states, etc.). This is mandatory, not optional. Without examples, responses become difficult to understand.
- **Argumentation**: The AI prompt is configured to not argue against user input when they present a position; it defaults to SUPPORT/EXPAND mode, but acknowledges mismatches if retrieved positions conflict.
- **Relevance Assessment**: The AI should check if retrieved positions actually address the user's question before using them, providing an intelligent fallback response consistent with Kuczynski's broader philosophy if no relevant positions exist.

## System Architecture

### Core Functionality
- **Semantic Search**: Indexes philosophical positions using OpenAI embeddings (text-embedding-3-small model) for efficient retrieval.
- **Streaming AI Responses**: Delivers token-by-token responses from various AI providers.
- **Multi-AI Provider Support**: Integrates Grok (xAI - default), Anthropic Claude, OpenAI, DeepSeek, and Perplexity, allowing model selection.
- **Dual Response Modes**:
  - **Basic Mode**: Faithfully quotes or very closely paraphrases retrieved positions, preserving exact arguments and examples.
  - **Enhanced Mode**: Synthesizes and extends ideas using positions as foundation, adding new inferences, structure, and clarification while maintaining Kuczynski's voice and philosophical system.
- **Content Ingestion**: Supports file uploads (PDF, Word, TXT) with automatic text extraction.
- **User Interface**: Features a clean conversation UI with auto-expanding input, distinct user/AI dialogue, responsive design, and mode toggle.
- **Source Citations**: Automatically includes relevant position IDs (e.g., EP-111, META-033) with each AI response.
- **Conversation Management**: Allows downloading individual exchanges in Markdown or TXT format.
- **Optional Login**: Implements a username-only login system for future chat history features.

### Technical Implementation
- **Backend**: Flask 3.1+ handles application logic, SSE streaming, and integration with the semantic search module (`search.py`).
- **Frontend**: A minimal HTML interface (`index.html`) is styled with professional gradients (`style.css`) and powered by vanilla JavaScript (`app.js`) for dynamic interactions and SSE streaming.
- **Data Management**: Philosophical positions are stored in `data/KUCZYNSKI_PHILOSOPHICAL_DATABASE_v32_CONCEPTUAL_ATOMISM.json`. Pre-computed embeddings are cached in `data/position_embeddings.pkl`. Source texts are in the `texts/` directory.
- **ML/NLP**: Utilizes `sentence-transformers`, `scikit-learn`, and CPU-optimized PyTorch for embedding generation and semantic similarity calculations.
- **File Processing**: Employs `PyPDF2` and `python-docx` for extracting text from uploaded documents.

### Key Design Decisions
- **Dual Mode Architecture**: Provides both strict adherence to Kuczynski's text (Basic Mode) and creative extension within his philosophical framework (Enhanced Mode).
- **Token-by-Token Streaming**: Ensures immediate and real-time display of AI responses.
- **Simplified Data Model**: Focuses on philosophical positions as primary data points.
- **CPU-Only PyTorch**: Optimizes for Replit environment constraints.

## External Dependencies
- **AI Providers**:
    - **Grok (xAI)** - Default provider
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
- **Deployment Platform**: Render.com
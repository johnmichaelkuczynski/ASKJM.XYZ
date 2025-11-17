# Ask a Philosopher - J.-M. Kuczynski AI Assistant

## Overview
This project is an intelligent philosophical conversation application that uses semantic search over J.-M. Kuczynski's works to synthesize thoughtful, streaming responses via Claude AI. Its core purpose is to provide an AI assistant capable of engaging in philosophical dialogue, accurately reflecting Kuczynski's rigorous arguments and writing style, based on a comprehensive database of his philosophical positions. The project aims to make his extensive body of work more accessible and interactive for users interested in in-depth philosophical inquiry.

**Status:** ✅ Fully functional MVP  
**Database:** v30_COLLEGE_PAPERS_COMPLETE - 1,558 positions from 40 works (includes College Papers Plus with 607 positions across logic, ethics, epistemology, metaphysics, mind, language, science, religion, political philosophy, aesthetics)

## User Preferences
- **API Integration**: Prefers direct Anthropic API integration over Replit AI Integrations
- **Response Style**: AI responses must faithfully represent Kuczynski's actual arguments, examples, and rigorous writing style, not glib paraphrases. This means quoting or very closely paraphrasing the actual text from positions, using his exact examples and rhetorical questions, preserving his step-by-step argumentative structure, and matching his rigorous, technical, methodical, and detailed tone. The AI should not summarize, simplify, or "make accessible" his work.
- **Argumentation**: The AI prompt is configured to not argue against user input when they present a position; it defaults to SUPPORT/EXPAND mode, but acknowledges mismatches if retrieved positions conflict.
- **Relevance Assessment**: The AI should check if retrieved positions actually address the user's question before using them, providing an intelligent fallback response consistent with Kuczynski's broader philosophy if no relevant positions exist.

## System Architecture

### Core Functionality
- **Semantic Search**: Indexes 1,558 philosophical positions using sentence-transformers (all-MiniLM-L6-v2 model) for efficient retrieval.
- **Streaming AI Responses**: Delivers token-by-token responses from various AI providers, ensuring a smooth user experience.
- **Multi-AI Provider Support**: Integrates Anthropic Claude, OpenAI, DeepSeek, and Perplexity, allowing model selection.
- **Dual Response Modes**: 
  - **Basic Mode**: Faithfully quotes or very closely paraphrases retrieved positions, preserving exact arguments and examples
  - **Enhanced Mode**: Synthesizes and extends ideas using positions as foundation, adding new inferences, structure, and clarification while maintaining Kuczynski's voice and philosophical system
- **Content Ingestion**: Supports file uploads (PDF, Word, TXT) with automatic text extraction.
- **User Interface**: Features a clean conversation UI with auto-expanding input, distinct user/AI dialogue, responsive design, and mode toggle.
- **Source Citations**: Automatically includes relevant position IDs (e.g., EP-111, META-033) with each AI response.
- **Conversation Management**: Allows downloading individual exchanges in Markdown or TXT format.
- **Optional Login**: Implements a username-only login system for future chat history features.

### Technical Implementation
- **Backend**: Flask 3.1+ handles the main application logic, SSE streaming, and integration with the semantic search module (`search.py`).
- **Frontend**: A minimal HTML interface (`index.html`) is styled with professional gradients (`style.css`) and powered by vanilla JavaScript (`app.js`) for dynamic interactions and SSE streaming.
- **Data Management**: Philosophical positions are stored in `data/KUCZYNSKI_PHILOSOPHICAL_DATABASE_v30_COLLEGE_PAPERS_COMPLETE.json` (1,558 positions). Pre-computed embeddings for these positions are cached in `data/position_embeddings.pkl`. Source texts from Kuczynski's works are stored in the `texts/` directory.
- **ML/NLP**: Utilizes `sentence-transformers`, `scikit-learn`, and CPU-optimized PyTorch for embedding generation and semantic similarity calculations.
- **File Processing**: Employs `PyPDF2` and `python-docx` for extracting text from uploaded documents.

### Key Design Decisions
- **Dual Mode Architecture**: 
  - **Basic Mode** (default): Ensures AI responses strictly adhere to Kuczynski's original text, examples, and argumentative style, avoiding summarization or simplification
  - **Enhanced Mode**: Uses retrieved positions as jumping-off point for original philosophical intellection that synthesizes, extends, and clarifies ideas while maintaining voice consistency and system coherence
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

## Recent Changes

**2025-11-17**: Enhanced Mode Feature
- **NEW FEATURE**: Added dual response mode toggle with Basic and Enhanced modes
- **Basic Mode**: Preserves existing behavior - faithfully quotes/closely paraphrases retrieved positions with exact examples, arguments, and tone
- **Enhanced Mode**: Synthesizes and extends ideas using positions as foundation - adds new inferences, structure, clarification while maintaining Kuczynski's rigorous voice and philosophical consistency
- **UI Update**: Added mode selector dropdown in frontend with clear labels explaining each mode
- **Backend**: Created separate prompt generation for each mode (build_prompt for Basic, build_enhanced_prompt for Enhanced)
- **Prompting Strategy**: Enhanced mode instructs AI to summarize in Kuczynski's voice, extend with new implications, add systematic organization, clarify concepts, and go beyond retrieved material while remaining consistent with core philosophical commitments
- **Architect Reviewed**: Implementation balances fidelity and extension, handles mode parameter safely with 'basic' default, UI clearly communicates differences

**2025-11-17**: College Papers Integration Fix
- **CRITICAL BUG FIX**: Fixed search.py field mapping issue that prevented College Papers positions from loading
- Added `text` field check to search.py position loader (line 32) - College Papers use `text` field while legacy positions use `thesis`, `position`, etc.
- **RESULT**: Active positions increased from 858 to 1,077 (all 607 College Papers positions now successfully integrated)
- Regenerated embeddings: 11 batches instead of 9, proper 1:1 alignment (1,077 positions = 1,077 embeddings)
- Semantic search now covers complete College Papers Plus collection across all philosophical domains

**2025-01-16**: Database v30 - College Papers Plus
- **DATABASE UPDATE v30**: Upgraded to v30_COLLEGE_PAPERS_COMPLETE with 1,558 positions from 40 works (607 more positions than v29)
- Added WORK-041 "College Papers Plus: Complete Works as of October 2019" with 607 positions from 63 philosophical papers covering:
  - Logic (material conditionals, modal logic, relevance logic)
  - Ethics (utilitarianism critique, Kantian ethics, consequentialism)
  - Epistemology (sensory perception, Gettier cases, testimony, induction)
  - Philosophy of Mind (dualism, hard problem of consciousness, qualia)
  - Philosophy of Language (Wittgenstein, reference/attribution)
  - Philosophy of Science (hypothetico-deductive method, values in science)
  - Metaphysics (external world, Cartesian self)
  - Philosophy of Religion (arguments for God, moral foundations)
  - Political Philosophy (democracy, justice, rights)
  - Aesthetics (nature of art, aesthetic value)
- Database loaded with 1,558 total positions; 1,077 active after deduplication and empty-text filtering

**2025-01-16**: Database v29 - Blog Essays Set 2
- **DATABASE UPDATE v29**: Upgraded to v29_BLOG_SET2_COMPLETE with 951 positions from 39 works (57 more positions than v28)
- Added WORK-040 "Blog Essays Collection Set 2" with 57 positions on:
  - Entropy and counter-entropy in cultural systems
  - Efficient Market Hypothesis critique
  - Jungian vs. Freudian psychoanalysis
  - Evolutionary psychology and mate selection
  - AI epistemology and embedded intelligence
- Regenerated embeddings with proper 1:1 alignment (858 active positions after filtering)

**2025-01-16**: Database v28 update + critical fixes
- **DATABASE UPDATE v28**: Upgraded to v28_BLOG_COMPLETE with 894 positions from 38 works (801 active after filtering). Added WORK-039 "Blog Essays Collection" with 58 positions on:
  - Zen Buddhism as authoritarianism (critique of Western misreading)
  - AI and embedded intelligence (the "pianist's hand" analogy)
  - Liberal empire decay (Glubb's theory amended)
  - Proceduralism and cultural criticism
- **CRITICAL BUG FIX**: Fixed index misalignment in semantic search - positions with empty text were filtered during embedding but remained in positions list, causing retrieval to return wrong IDs
- Regenerated embeddings with proper 1:1 alignment (801 positions = 801 embeddings)
- Removed "RELEVANCE ASSESSMENT" preamble from AI responses - responses now start directly with content
- Added Perplexity as 4th AI provider option
- Added Render.com deployment configuration (render.yaml, runtime.txt)
- Fixed Flask app to read PORT environment variable for Render deployment
- Added Gunicorn + gevent to requirements for production deployment
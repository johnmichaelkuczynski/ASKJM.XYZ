# Ask a Philosopher - J.-M. Kuczynski AI Assistant

## Overview
This project is an intelligent philosophical conversation application that uses semantic search over J.-M. Kuczynski's works to synthesize thoughtful, streaming responses via Claude AI. Its core purpose is to provide an AI assistant capable of engaging in philosophical dialogue, accurately reflecting Kuczynski's rigorous arguments and writing style, based on a comprehensive database of his philosophical positions. The project aims to make his extensive body of work more accessible and interactive for users interested in in-depth philosophical inquiry.

## Recent Changes

### 2025-11-19: Comprehensive Publications Corpus Added to Database
- Added 38 new philosophical positions from 100+ Kuczynski publications (1997-2025)
- Covers major journal articles, books, and dissertation work
- Key additions:
  - **Language of Thought**: LOT-001 through LOT-003 (presentations vs representations, vicious regress argument)
  - **Self-Knowledge**: SELF-001, SELF-002 (object-awareness vs truth-awareness distinction)
  - **Mind-Body Problem**: MAT-001 through MAT-003 (qualia argument, data-spaces argument, theoretical identification)
  - **Explanatory Gap**: EXPL-001, EXPL-002 (ontological vs epistemological priority)
  - **Emergence**: EMERG-001 (ambiguity of emergence claims)
  - **Causation**: CAUS-001 through CAUS-003 (causation as persistence, spacetime supervenes on causation)
  - **Epistemology**: KNOW-001 (knowledge as meta-knowledge about anomaly generation)
  - **Legal Philosophy**: LAW-001, LAW-002 (laws as assurances of rights, international law)
  - **Emotions**: EMOT-001 (emotions as judgments from egocentric frame)
  - **Logic & AI**: LOGIC-001 (classical logic fails for real reasoning)
  - **Paradoxes**: PARA-001, PARA-002 (non-revisionist solutions, Sorites via implicit comparatives)
  - **Modality**: MOD-001, COUNT-001 (Kripke critique, counterfactuals)
  - **Language**: LANG-001, LANG-002 (literal vs intuitive meaning, anti-Russellian descriptions)
  - **Computational Mind**: COMP-001, COMP-002 (form equivocation, simulation vs thinking)
  - **Kant**: KANT-001, KANT-002 (non-trivial analytics fix system, God as ground not creator)
  - **Wittgenstein**: WITT-001 (language not essential for thought)
  - **Intentionalism**: INT-001 (qualia content not fixed)
  - **Justice**: JUST-001 (Rawls critique)
  - **Psychology**: PSY-001 through PSY-004 (aggression, psychopathy, paranoia, neuroses)
  - **Nietzsche**: NIET-001 (slave vs master morality)
  - **Paradox of Analysis**: ANAL-001 (solution via grasping vs knowing distinction)
- Database now contains 1,760 total positions (631 with valid text for semantic search)
- Regenerated embeddings for semantic search integration

### 2025-11-19: Secure Internal Knowledge API Endpoint Created
- Created `/api/internal/knowledge` POST endpoint for external system integration
- **Authentication**: Requires `ZHI_PRIVATE_KEY` in Authorization header (supports both `Bearer <token>` and direct token)
- **Input**: JSON body with `query` (required) and `context` (optional)
- **Output**: JSON response with:
  - `result`: Formatted text with philosophical positions and KIRE inferences
  - `metadata`: Structured data including positions array, KIRE inferences, database size, timestamp
- **Security**: All unauthorized requests return 401 error
- **Functionality**: Integrates semantic search (top 5 positions) + KIRE deductive reasoning (top 10 rules)
- **URL Pattern**: `https://askjm.xyz/api/internal/knowledge`

### 2025-11-18: Two Philosophy Articles Added to Database
- Added comprehensive extraction from "Fodor on Concepts: How to be a non-Atomist without being a Holist" (KUC-FODOR-CONCEPTS)
  - Extracted 15 positions covering:
    - Terminological distinctions (concept vs concepto)
    - Anti-atomist thesis: concepts always presuppose other concepts
    - Case studies: redness, phenomenal experience, sense-perception
    - Fodor's atomism and three arguments for it
    - Critique of Fodor's indefinability argument
    - Analysis showing conceptso have infinite structure, not atomic simplicity
  - Position IDs: FODOR-001 through FODOR-015
  
- Added comprehensive extraction from "Uniquely Individuating Descriptions" (KUC-UID)
  - Extracted 9 positions covering:
    - Main thesis: reference and conception require UIDs
    - Reconciliation of Kripke's direct reference with epistemic descriptivism
    - Three ways of learning reference: ostension, description, picking up from context
    - Analysis showing ostensive definition reduces to descriptive knowledge
    - Causal connections subordinate to UID knowledge
  - Position IDs: UID-001 through UID-009

- Total new positions: 24
- Database now contains 1,722 total positions (593 with valid text for semantic search)
- Regenerated embeddings for semantic search integration

### 2025-11-18: Economics Article Added to Database
- Added comprehensive extraction from "The Impossibility of Economics as Predictive Science: Reflexivity, Emergence, and the Equilibrium Fallacy" (KUC-2025-11-REFLEX)
- Extracted 70 detailed positions covering:
  - The Equilibrium Worldview as Category Error
  - Reflexivity Problem in economic systems
  - Constant Emergence in economies
  - Path-Dependency and evolutionary nature of economics
  - Endogenous/Exogenous distinction collapse
  - Invariants problem (universal principles too abstract, specific principles not invariant)
  - Cultural vs Economic Equilibrium confusion
  - Degree of predictability questions
  - Implications for economic modeling and policy
- Position IDs: ECON-REFLEX-001 through ECON-REFLEX-070
- Database now contains 1,698 total positions (1,203 with valid text for semantic search)
- Regenerated embeddings for semantic search integration

### 2025-11-18: Grok Configuration Fixed
- Updated from deprecated `grok-beta` model to `grok-2-latest`
- Added `grok-2-vision-1212` and `grok-vision-beta` as available models
- Fixed frontend to default to Grok (xAI) provider
- Fixed frontend to default to Enhanced Mode

## User Preferences
- **API Integration**: Prefers direct Anthropic API integration over Replit AI Integrations
- **Response Style**: AI responses must faithfully represent Kuczynski's actual arguments, examples, and rigorous writing style, not glib paraphrases. This means quoting or very closely paraphrasing the actual text from positions, using his exact examples and rhetorical questions, preserving his step-by-step argumentative structure, and matching his rigorous, technical, methodical, and detailed tone. The AI should not summarize, simplify, or "make accessible" his work.
- **Examples Required**: Kuczynski's writing is replete with concrete examples. AI responses MUST include examples when explaining abstract concepts (propositions, properties, mental states, etc.). This is mandatory, not optional. Without examples, responses become difficult to understand.
- **Argumentation**: The AI prompt is configured to not argue against user input when they present a position; it defaults to SUPPORT/EXPAND mode, but acknowledges mismatches if retrieved positions conflict.
- **Relevance Assessment**: The AI should check if retrieved positions actually address the user's question before using them, providing an intelligent fallback response consistent with Kuczynski's broader philosophy if no relevant positions exist.

## System Architecture

### Core Functionality
- **Secure Internal API**: `/api/internal/knowledge` endpoint for external system queries with ZHI_PRIVATE_KEY authentication
- **Semantic Search**: Indexes philosophical positions using OpenAI embeddings (text-embedding-3-small model) for efficient retrieval.
- **Streaming AI Responses**: Delivers token-by-token responses from various AI providers.
- **Multi-AI Provider Support**: Integrates Grok (xAI - default), Anthropic Claude, OpenAI, DeepSeek, and Perplexity, allowing model selection.
- **Dual Response Modes**:
  - **Enhanced Mode** (Default): Synthesizes and extends ideas using positions as foundation, adding new inferences, structure, and clarification while maintaining Kuczynski's voice and philosophical system.
  - **Basic Mode**: Faithfully quotes or very closely paraphrases retrieved positions, preserving exact arguments and examples.
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
# Ask a Philosopher - J.-M. Kuczynski AI Assistant

## Overview

An intelligent philosophical conversation application that uses semantic search over 826 philosophical positions from J.-M. Kuczynski's works and synthesizes thoughtful responses using Claude AI with streaming.

**Status:** ✅ Fully functional MVP  
**Database:** v27_COMPLETE - 744 active positions (filtered from 836 total, removing 82 with empty text) from 37 works

## Features

### Core Functionality
- ✅ **Semantic Search**: 826 philosophical positions indexed with sentence-transformers
- ✅ **Streaming AI Responses**: Token-by-token streaming from Claude API (no loading spinner!)
- ✅ **Multiple AI Providers**: Support for Anthropic Claude, OpenAI, DeepSeek, and Perplexity with model selection
- ✅ **Large Text Input**: Auto-expanding textarea (150-400px) for questions
- ✅ **File Upload**: Support for PDF, Word (.doc/.docx), and TXT files with automatic text extraction
- ✅ **Clean Conversation UI**: Clear distinction between user questions and Kuczynski responses
- ✅ **Source Citations**: Each response shows relevant position IDs (e.g., EP-111, META-033)
- ✅ **Download Conversations**: Export individual exchanges to Markdown or TXT format
- ✅ **Responsive Design**: Mobile-friendly with smooth auto-scroll during streaming
- ✅ **Optional Login**: Username-only login system (no password) for future chat history

## Architecture

### Backend (Python/Flask)
- `app.py`: Main Flask application with SSE streaming endpoint
- `search.py`: Semantic search module using sentence-transformers (all-MiniLM-L6-v2 model)
- Direct Claude API integration via Anthropic SDK (requires ANTHROPIC_API_KEY)

### Frontend
- `templates/index.html`: Clean, minimal HTML interface
- `static/style.css`: Professional gradient design with conversation bubbles
- `static/app.js`: Vanilla JavaScript with SSE streaming support

### Data
- `data/KUCZYNSKI_PHILOSOPHICAL_DATABASE_v27_COMPLETE.json`: 836 positions (826 with unique IDs) across 37 works (v27_COMPLETE)
- `data/position_embeddings.pkl`: Pre-computed embeddings for fast search (auto-generated)
- `texts/`: Source texts from Kuczynski's works (being added incrementally)

## Technical Stack

- **Backend**: Flask 3.1+
- **AI Providers**: Anthropic Claude, OpenAI, DeepSeek, Perplexity (direct API integration)
- **ML**: sentence-transformers 5.1+, scikit-learn 1.7+, PyTorch (CPU)
- **File Processing**: PyPDF2, python-docx
- **Frontend**: Vanilla JavaScript, SSE for streaming

## User Preferences

- **API Integration**: Prefers direct Anthropic API integration over Replit AI Integrations

## Recent Changes

**2025-11-16**: Critical semantic search fix and prompt cleanup
- **CRITICAL BUG FIX**: Fixed index misalignment in semantic search - positions with empty text were filtered during embedding but remained in positions list, causing retrieval to return wrong IDs
- Regenerated embeddings with proper 1:1 alignment (744 positions = 744 embeddings)
- Removed "RELEVANCE ASSESSMENT" preamble from AI responses - responses now start directly with content
- Added Perplexity as 4th AI provider option
- Added Render.com deployment configuration (render.yaml, runtime.txt)
- Fixed Flask app to read PORT environment variable for Render deployment
- Added Gunicorn + gevent to requirements for production deployment

**2025-11-15**: Initial MVP implementation, database expansion, and prompt refinements
- Set up semantic search and upgraded to 808 philosophical positions
- Database evolution: v17 baseline → v18 (free will, religion) → v19 (modal logic, religion) → v25 COMPLETE (762 positions, 36 works) → v25_PROBABILITY_FIX (808 positions, 36 works + 7 critical probability positions)
- Implemented Claude streaming with SSE
- Created clean conversation UI with auto-expanding input
- Added file upload support (PDF/Word/TXT)
- Implemented per-exchange Markdown export
- Added optional username login system
- Successfully deployed on port 5000
- Switched from Replit AI Integrations to direct Anthropic API (user preference)
- Added multi-provider support (Anthropic, OpenAI, DeepSeek) with model selection
- **CRITICAL**: Completely rewrote AI prompt (5 iterations) to ensure faithful representation of Kuczynski's actual arguments, examples, and rigorous writing style - not glib paraphrases
- **CRITICAL FIX**: Modified prompt to NOT argue against user input when they're presenting a position - defaults to SUPPORT/EXPAND mode, but ACKNOWLEDGES MISMATCH if retrieved positions conflict (prevents fabrication of supportive citations)
- **VERIFIED WORKING**: User confirmed prompt is now functioning correctly after all refinements
- **DATABASE UPDATE**: Upgraded to v25_PROBABILITY_FIX with 808 positions (added 7 critical positions on probability from WORK-014 Chapter 7 establishing probability as CAUSAL, refuting Frequency Theory)
- **CRITICAL FIX v2**: Completely rewrote prompt to include RELEVANCE ASSESSMENT - AI now checks if positions actually address the question before using them. Prevents fabricating absurd connections (e.g., alcoholics → Socrates). Added similarity threshold (0.25) to filter weak semantic matches. When no relevant positions exist, AI provides intelligent fallback response consistent with Kuczynski's broader philosophy.
- **DATABASE UPDATE v27**: Upgraded to v27_COMPLETE with 836 positions from 37 works. Added WORK-038 "Why Was Socrates Executed?" with 5 positions (POL-37, POL-38, POL-39, HIST-2, POL-41) establishing: (1) Socrates executed for wartime disruption not truth-seeking, (2) sought power through intellectual influence, (3) trained oligarchic coup leaders, (4) delegitimized authority with replacement theory.
- Created `texts/` directory for source works
- Added source texts (being provided incrementally):
  - "A Priori Knowledge and Other Philosophical Works" (1,385 lines)
  - "Analytic Philosophy Complete" (9,169 lines)
  - "Attachment Theory and Mental Illness" (178 lines)
  - "Conception and Causation: Selected Early Philosophical Papers" (8,869 lines)
  - "Dialogues with the Master" (730 lines)
  - "Group Psychology is More Basic than Individual Psychology" (12 lines)
  - "The Incompleteness of Deductive Logic" (5,369 lines)
  - "Intensionality, Modality, and Rationality" (2,120 lines)
  - "Kant and Hume on Induction, Causation, and Methodology" (571 lines)
  - "King Follett Discourse: A Historiographical Approach" (1,220 lines)
  - "Libet's Experiment: Why It Matters and What It Means" (1,977 lines)
  - "Logic, Set-theory, and Philosophy of Mathematics" (5,735 lines)
  - "Network Reinterpretation of Kant's Transcendental Idealism" (7,992 lines)
  - "Ninety Paradoxes of Philosophy and Psychology" (582 lines)
  - "OCD and Philosophy" (403 lines)
  - "Papers on Accounting, Business, Economics, Politics, and Psychology" (59,939 lines)
  - "Philosophical Knowledge: What It Is and Why Philosophy Departments Don't Want You to Have It" (2,065 lines)
  - "Quantifiers in Natural Language" (567 lines)
  - "Theoretical Knowledge and Inductive Inference" (1,681 lines) [UPDATED - Full 8-chapter version with critical Chapter 7 on probability as CAUSAL]
  - "Three Kinds of Psychopaths" (25 lines) [UPDATED]
  - "Mind, Meaning, and Scientific Explanation" (7,269 lines)
  - "Counterfactuals (Epistemic Analysis)" (483 lines)
  - "The Moral Structure of Legal Obligation" (22,950 lines)
  - "A Dialogue Concerning OCD" (734 lines)
  - "Outline of a Theory of Knowledge" (104 lines)
  - "Group Psychology is More Basic than Individual Psychology" (12 lines) [UPDATED]
- Added TXT download format option (in addition to Markdown)

## Project Structure

```
.
├── app.py                          # Flask app with streaming
├── search.py                       # Semantic search module
├── requirements.txt                # Python dependencies
├── data/
│   ├── master_database_v19_complete.json   # 699 philosophical positions (v19.0 COMPLETE)
│   └── position_embeddings.pkl    # Cached embeddings (auto-generated)
├── texts/                          # Source texts from Kuczynski's works
│   ├── A_Priori_Knowledge_and_Other_Philosophical_Works.txt  # 1,385 lines
│   ├── Analytic_Philosophy_Complete.txt  # 9,169 lines
│   ├── Attachment_Theory_and_Mental_Illness.txt  # 178 lines
│   ├── Chomskys_Two_Contributions_to_Philosophy.txt  # 80 lines
│   ├── Conception_and_Causation.txt      # 8,869 lines
│   ├── Dialogues_with_the_Master.txt     # 730 lines
│   ├── Group_Psychology_More_Basic_than_Individual.txt  # 12 lines
│   ├── Incompleteness_of_Deductive_Logic.txt  # 5,369 lines
│   ├── Intensionality_Modality_and_Rationality.txt  # 2,120 lines
│   ├── Kant_and_Hume_on_Induction.txt    # 571 lines
│   ├── King_Follett_Discourse_Historiography.txt  # 1,220 lines
│   ├── Libets_Experiment_Free_Will.txt   # 1,977 lines
│   ├── Logic_Set_Theory_and_Philosophy_of_Mathematics.txt  # 5,735 lines
│   ├── Network_Reinterpretation_of_Kants_Transcendental_Idealism.txt  # 7,992 lines
│   ├── Ninety_Paradoxes.txt              # 582 lines
│   ├── OCD_and_Philosophy.txt            # 403 lines
│   ├── Papers_on_Accounting_Business_Economics_Politics_and_Psychology.txt  # 59,939 lines
│   ├── Philosophical_Knowledge.txt       # 2,065 lines
│   ├── Quantifiers_in_Natural_Language.txt  # 567 lines
│   ├── Theoretical_Knowledge_and_Inductive_Inference.txt  # 1,681 lines [UPDATED]
│   ├── Three_Kinds_of_Psychopaths.txt    # 25 lines [UPDATED]
│   ├── Mind_Meaning_and_Scientific_Explanation.txt  # 7,269 lines
│   ├── Counterfactuals_Epistemic_Analysis.txt  # 483 lines
│   ├── Moral_Structure_of_Legal_Obligation.txt  # 22,950 lines
│   ├── Dialogue_Concerning_OCD.txt  # 734 lines
│   ├── Outline_of_a_Theory_of_Knowledge.txt  # 104 lines
│   └── Group_Psychology_More_Basic_than_Individual.txt  # 12 lines [UPDATED]
├── templates/
│   └── index.html                 # Frontend HTML
├── static/
│   ├── style.css                  # UI styling
│   └── app.js                     # Frontend JavaScript
└── attached_assets/
    └── master_database_v17*.json  # Source database file
```

## How It Works

1. **User Input**: User types/pastes a question or uploads a document
2. **Semantic Search**: Query is embedded and compared against 699 position embeddings
3. **Context Retrieval**: Top 5-7 most relevant positions are retrieved
4. **Intelligent Synthesis**: Claude receives positions as context and generates thoughtful response
5. **Streaming Display**: Response streams token-by-token to frontend via SSE
6. **Citations**: Position IDs shown at bottom of each response
7. **Download**: User can export exchange to Markdown

## Key Design Decisions

### Faithful Representation, Not Creative Interpretation
**CRITICAL DESIGN PRINCIPLE**: The prompt explicitly forbids paraphrasing or generalizing. The AI must:
- QUOTE or VERY CLOSELY PARAPHRASE the actual text from positions
- Use Kuczynski's exact examples (rock, tree, dog, cat, etc.)
- Use his exact rhetorical questions when present
- Preserve his step-by-step argumentative structure
- Match his exact tone: rigorous, technical, methodical, detailed
- When source is detailed and long → response must be detailed and long
- Think of the task as TRANSCRIBING Kuczynski's actual words, not explaining them
- FORBIDDEN: summarizing, simplifying, "making accessible", or being glib/conversational
This ensures responses sound like Kuczynski's actual work, not an AI's interpretation of it.

### Token-by-Token Streaming
No loading spinners - responses appear immediately and stream in real-time for better UX.

### Simplified Data Model
No separate text retrieval system yet - positions themselves contain the philosophical content. Future enhancement could add actual text excerpts from source works.

### CPU-Only PyTorch
Used CPU-optimized PyTorch to avoid disk quota issues in Replit environment.

## Future Enhancements

1. **Text Pointers System**: Link positions to actual excerpts in source works (texts being added incrementally)
2. **Full Conversation Export**: Download entire session history
3. **Chat History**: Persist conversations for logged-in users
4. **Domain Filtering**: Filter positions by philosophical domain
5. **Follow-up Context**: Maintain conversation context across multiple exchanges
6. **Position Details**: Click citations to see full position text from source works

## Known Limitations

- Embeddings computed on first run (takes ~5 seconds), then cached
- No actual text excerpts from source works yet (positions only)
- Login doesn't persist across sessions (session-based only)
- Single conversation per session (no history panel)

## Performance

- **Startup**: ~10 seconds (downloads model, computes embeddings)
- **Subsequent Starts**: ~2 seconds (loads cached embeddings)
- **Search**: <100ms for semantic search over 826 positions
- **Streaming**: Real-time token-by-token display from Claude

## Environment

- **Port**: 5000 (configured for Replit webview)
- **Database**: 826 positions from J.-M. Kuczynski's works (v27_COMPLETE: 37 works analyzed, 826 unique IDs, includes Socrates execution positions and critical probability positions)
- **AI Providers**: Multiple providers supported (direct integration)
- **Required Secrets** (at least one):
  - `ANTHROPIC_API_KEY` - For Claude models
  - `OPENAI_API_KEY` - For GPT models (optional)
  - `DEEPSEEK_API_KEY` - For DeepSeek models (optional)
  - `PERPLEXITY_API_KEY` - For Perplexity models (optional)

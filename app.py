from flask import Flask, render_template, request, Response, jsonify, session  # type: ignore
import json
import os
from search import SemanticSearch

try:
    import anthropic  # type: ignore
    from anthropic import Anthropic  # type: ignore
except ImportError:
    print("Anthropic library not found. Installing...")
    Anthropic = None

try:
    from openai import OpenAI  # type: ignore
except ImportError:
    print("OpenAI library not found. Installing...")
    OpenAI = None

try:
    import PyPDF2  # type: ignore
except ImportError:
    print("PyPDF2 not found")
    PyPDF2 = None

try:
    import docx  # type: ignore
except ImportError:
    print("python-docx not found")
    docx = None

app = Flask(__name__)
app.secret_key = os.environ.get('SESSION_SECRET', os.urandom(24))

print("Initializing semantic search...")
searcher = SemanticSearch('data/KUCZYNSKI_PHILOSOPHICAL_DATABASE_v32_CONCEPTUAL_ATOMISM.json', 'data/position_embeddings.pkl')

anthropic_client = None
openai_client = None
deepseek_client = None
perplexity_client = None

try:
    ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
    if ANTHROPIC_API_KEY and Anthropic:
        anthropic_client = Anthropic(api_key=ANTHROPIC_API_KEY)
        print("✓ Anthropic client initialized")
except Exception as e:
    print(f"✗ Could not initialize Anthropic: {e}")

try:
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    if OPENAI_API_KEY and OpenAI:
        openai_client = OpenAI(api_key=OPENAI_API_KEY)
        print("✓ OpenAI client initialized")
except Exception as e:
    print(f"✗ Could not initialize OpenAI: {e}")

try:
    DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")
    if DEEPSEEK_API_KEY and OpenAI:
        deepseek_client = OpenAI(
            api_key=DEEPSEEK_API_KEY,
            base_url="https://api.deepseek.com"
        )
        print("✓ DeepSeek client initialized")
except Exception as e:
    print(f"✗ Could not initialize DeepSeek: {e}")

try:
    PERPLEXITY_API_KEY = os.environ.get("PERPLEXITY_API_KEY")
    if PERPLEXITY_API_KEY and OpenAI:
        perplexity_client = OpenAI(
            api_key=PERPLEXITY_API_KEY,
            base_url="https://api.perplexity.ai"
        )
        print("✓ Perplexity client initialized")
except Exception as e:
    print(f"✗ Could not initialize Perplexity: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/providers', methods=['GET'])
def get_providers():
    """Return available AI providers"""
    providers = []
    if anthropic_client:
        providers.append({'id': 'anthropic', 'name': 'Anthropic Claude', 'models': ['claude-sonnet-4-20250514', 'claude-opus-4-20250514']})
    if openai_client:
        providers.append({'id': 'openai', 'name': 'OpenAI', 'models': ['gpt-4o', 'gpt-4o-mini', 'o1', 'o1-mini']})
    if deepseek_client:
        providers.append({'id': 'deepseek', 'name': 'DeepSeek', 'models': ['deepseek-chat', 'deepseek-reasoner']})
    if perplexity_client:
        providers.append({'id': 'perplexity', 'name': 'Perplexity', 'models': ['llama-3.1-sonar-large-128k-online', 'llama-3.1-sonar-small-128k-online']})
    return jsonify({'providers': providers})

@app.route('/api/ask', methods=['POST'])
def ask():
    """Handle user question with streaming response"""
    try:
        data = request.json
        question = data.get('question', '')
        provider = data.get('provider', 'anthropic')
        model = data.get('model', '')
        mode = data.get('mode', 'basic')
        
        print(f"Received question: {question}")
        print(f"Provider: {provider}, Model: {model}, Mode: {mode}")
        
        if not question:
            return jsonify({'error': 'No question provided'}), 400
        
        print("Searching for relevant positions...")
        try:
            relevant_positions = searcher.search(question, top_k=7)
            print(f"Found {len(relevant_positions)} relevant positions")
        except Exception as e:
            print(f"ERROR in search: {str(e)}")
            import traceback
            traceback.print_exc()
            return jsonify({'error': f'Search failed: {str(e)}'}), 500
        
        def generate():
            try:
                print("Starting SSE generator...")
                sources = [p['position_id'] for p in relevant_positions]
                yield f"data: {json.dumps({'type': 'sources', 'data': sources})}\n\n"
                
                if mode == 'enhanced':
                    prompt = build_enhanced_prompt(question, relevant_positions)
                else:
                    prompt = build_prompt(question, relevant_positions)
                print(f"Generated prompt, sending to {provider}...")
                
                if provider == 'anthropic':
                    if not anthropic_client:
                        yield f"data: {json.dumps({'type': 'error', 'data': 'Anthropic API key not configured'})}\n\n"
                        yield f"data: {json.dumps({'type': 'done'})}\n\n"
                        return
                    model_name = model or "claude-sonnet-4-20250514"
                    print(f"Using Anthropic model: {model_name}")
                    with anthropic_client.messages.stream(
                        model=model_name,
                        max_tokens=2500,
                        messages=[{"role": "user", "content": prompt}]
                    ) as stream:
                        token_count = 0
                        for text in stream.text_stream:
                            token_count += 1
                            if token_count % 10 == 0:
                                print(f"Streamed {token_count} tokens...")
                            yield f"data: {json.dumps({'type': 'token', 'data': text})}\n\n"
                        print(f"Completed streaming {token_count} total tokens")
                
                elif provider == 'openai':
                    if not openai_client:
                        yield f"data: {json.dumps({'type': 'error', 'data': 'OpenAI API key not configured'})}\n\n"
                        yield f"data: {json.dumps({'type': 'done'})}\n\n"
                        return
                    model_name = model or "gpt-4o"
                    stream = openai_client.chat.completions.create(
                        model=model_name,
                        messages=[{"role": "user", "content": prompt}],
                        stream=True,
                        max_tokens=2500
                    )
                    for chunk in stream:
                        if chunk.choices[0].delta.content:
                            yield f"data: {json.dumps({'type': 'token', 'data': chunk.choices[0].delta.content})}\n\n"
                
                elif provider == 'deepseek':
                    if not deepseek_client:
                        yield f"data: {json.dumps({'type': 'error', 'data': 'DeepSeek API key not configured'})}\n\n"
                        yield f"data: {json.dumps({'type': 'done'})}\n\n"
                        return
                    model_name = model or "deepseek-chat"
                    stream = deepseek_client.chat.completions.create(
                        model=model_name,
                        messages=[{"role": "user", "content": prompt}],
                        stream=True,
                        max_tokens=2500
                    )
                    for chunk in stream:
                        if chunk.choices[0].delta.content:
                            yield f"data: {json.dumps({'type': 'token', 'data': chunk.choices[0].delta.content})}\n\n"
                
                elif provider == 'perplexity':
                    if not perplexity_client:
                        yield f"data: {json.dumps({'type': 'error', 'data': 'Perplexity API key not configured'})}\n\n"
                        yield f"data: {json.dumps({'type': 'done'})}\n\n"
                        return
                    model_name = model or "llama-3.1-sonar-large-128k-online"
                    stream = perplexity_client.chat.completions.create(
                        model=model_name,
                        messages=[{"role": "user", "content": prompt}],
                        stream=True,
                        max_tokens=2500
                    )
                    for chunk in stream:
                        if chunk.choices[0].delta.content:
                            yield f"data: {json.dumps({'type': 'token', 'data': chunk.choices[0].delta.content})}\n\n"
                
                else:
                    yield f"data: {json.dumps({'type': 'error', 'data': f'Unknown provider: {provider}'})}\n\n"
                    yield f"data: {json.dumps({'type': 'done'})}\n\n"
                    return
                
                yield f"data: {json.dumps({'type': 'done'})}\n\n"
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                yield f"data: {json.dumps({'type': 'token', 'data': error_msg})}\n\n"
                yield f"data: {json.dumps({'type': 'done'})}\n\n"
        
        return Response(
            generate(), 
            mimetype='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'X-Accel-Buffering': 'no',
                'Connection': 'keep-alive'
            }
        )
    except Exception as e:
        print(f"ERROR in /api/ask: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

def build_prompt(question, positions):
    """Build intelligent prompt for Claude - BASIC MODE (faithful quoting)"""
    
    excerpts = "\n\n".join([
        f"POSITION {i+1} (ID: {p['position_id']}, Domain: {p['domain']}):\nTitle: {p['title']}\n{p['text']}"
        for i, p in enumerate(positions)
    ])
    
    prompt = f"""You are J.-M. Kuczynski answering a philosophical question.

CRITICAL: Kuczynski's writing is REPLETE with concrete examples. Philosophical explanations without examples are inadequate and hard to understand.

INSTRUCTIONS:
1. If the retrieved positions below address the question, QUOTE or VERY CLOSELY PARAPHRASE them
2. ALWAYS INCLUDE EXAMPLES when explaining concepts - this is mandatory, not optional
3. Use EXACT EXAMPLES from positions (if it says "rock, tree, dog" → you say "rock, tree, dog")
4. Use EXACT RHETORICAL QUESTIONS from positions
5. Follow EXACT ARGUMENT STRUCTURE from positions (step-by-step if present)
6. Match EXACT TONE: rigorous, technical, methodical, detailed
7. When positions are detailed → your response must be detailed
8. Think of yourself as transcribing actual words, not explaining them
9. If a position includes examples to illustrate a point, you MUST include those examples
10. If no example is present in the position but one is needed to illustrate an abstract concept, supply one consistent with the text and Kuczynski's style

When explaining abstract concepts like "proposition," "property," "abstraction," etc., ALWAYS provide concrete examples (e.g., the proposition that snow is white, the property of being red, the number 7, etc.).

If positions don't address the question, provide an intelligent philosophical response consistent with rigorous analysis, INCLUDING EXAMPLES.

NEVER fabricate connections between unrelated topics. NEVER output preambles, assessments, or meta-commentary.

RETRIEVED POSITIONS:
{excerpts}

USER QUESTION:
{question}

Respond directly with your answer (no preamble)."""

    return prompt

def build_enhanced_prompt(question, positions):
    """Build enhanced prompt - ENHANCED MODE (synthesis and extension)"""
    
    excerpts = "\n\n".join([
        f"POSITION {i+1} (ID: {p['position_id']}, Domain: {p['domain']}):\nTitle: {p['title']}\n{p['text']}"
        for i, p in enumerate(positions)
    ])
    
    prompt = f"""You are J.-M. Kuczynski in ENHANCED MODE. Your task is to synthesize, extend, and develop the ideas from your retrieved positions.

CRITICAL: Kuczynski's writing is REPLETE with concrete examples. ALWAYS illustrate abstract points with specific examples. This is non-negotiable.

ENHANCED MODE INSTRUCTIONS:
1. SUMMARIZE retrieved positions in your voice - capture the essence, not just transcribe
2. ALWAYS INCLUDE CONCRETE EXAMPLES when explaining concepts (mandatory, not optional)
3. Use examples from positions when available, create new ones in Kuczynski's style when needed
4. EXTEND the ideas with new inferences, implications, and connections not explicitly stated in positions
5. ADD new structure and organization that makes ideas more systematic and comprehensive  
6. CLARIFY difficult concepts with new explanations AND EXAMPLES in your rigorous style
7. REMAIN CONSISTENT with your philosophical system - never contradict core positions
8. USE YOUR CONCEPTS AND VOCABULARY - your distinctive terminology and analytical framework
9. GO BEYOND the retrieved material while staying true to the underlying philosophical commitments

Think of this as using the positions as a jumping-off point for original philosophical intellection that sounds unmistakably like you - rigorous, systematic, analytical, uncompromising - but develops ideas further than what's explicitly written.

When explaining abstract concepts (proposition, property, mental state, etc.), ALWAYS provide concrete examples like:
- "The proposition that snow is white" or "the proposition that 2+2=4"
- "The property of being red" or "the property of being triangular"
- "Believing that Paris is in France" or "desiring that the pain stop"

CRITICAL: Sound like Kuczynski. Match his:
- Rigorous, technical precision
- Step-by-step analytical method with concrete illustrations
- Uncompromising clarity and directness
- Systematic interconnection of ideas
- Distinctive philosophical vocabulary
- Extensive use of specific examples to illustrate abstract points

NEVER fabricate connections between unrelated topics. NEVER output preambles or meta-commentary.

RETRIEVED POSITIONS (use as foundation):
{excerpts}

USER QUESTION:
{question}

Synthesize, extend, and develop your answer (no preamble)."""

    return prompt

@app.route('/api/login', methods=['POST'])
def login():
    """Simple username-only login"""
    username = request.json.get('username', '').strip()
    if username:
        session['username'] = username
        return jsonify({'success': True, 'username': username})
    return jsonify({'success': False, 'error': 'Username required'}), 400

@app.route('/api/logout', methods=['POST'])
def logout():
    """Logout user"""
    session.pop('username', None)
    return jsonify({'success': True})

@app.route('/api/check-session', methods=['GET'])
def check_session():
    """Check if user is logged in"""
    username = session.get('username')
    return jsonify({'logged_in': username is not None, 'username': username})

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle file uploads and extract text"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        filename = file.filename.lower()
        
        if filename.endswith('.txt'):
            text = file.read().decode('utf-8', errors='ignore')
        elif filename.endswith('.pdf'):
            if not PyPDF2:
                return jsonify({'error': 'PDF support not available'}), 400
            try:
                pdf = PyPDF2.PdfReader(file)
                text = '\n\n'.join([page.extract_text() for page in pdf.pages if page.extract_text()])
            except Exception as e:
                return jsonify({'error': f'Error reading PDF: {str(e)}'}), 400
        elif filename.endswith(('.doc', '.docx')):
            if not docx:
                return jsonify({'error': 'Word document support not available'}), 400
            try:
                doc = docx.Document(file)
                text = '\n\n'.join([para.text for para in doc.paragraphs if para.text.strip()])
            except Exception as e:
                return jsonify({'error': f'Error reading Word document: {str(e)}'}), 400
        else:
            return jsonify({'error': 'Unsupported file type. Please upload .txt, .pdf, or .docx'}), 400
        
        return jsonify({'text': text[:10000]})
    except Exception as e:
        return jsonify({'error': f'Error processing file: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print("\n" + "="*60)
    print("  Ask a Philosopher - J.-M. Kuczynski AI Assistant")
    print("="*60)
    print(f"  Loaded {len(searcher.positions)} philosophical positions")
    print(f"  Server starting on http://0.0.0.0:{port}")
    print("="*60 + "\n")
    app.run(host='0.0.0.0', port=port, debug=False)

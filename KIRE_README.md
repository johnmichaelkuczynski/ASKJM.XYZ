# Kuczynski Inference Rule Engine (KIRE)

## Overview
KIRE transforms your Kuczynski app from "best Kuczynski impersonator" into "executable Kuczynski mind" by adding savage inference-rule chaining.

## Architecture

### New Files Created
1. **`kuczynski_rules_full.json`** (842 rules)
   - 5 immortal meta-rules (KMETA-001 to KMETA-005)
   - 837 inference rules from philosophical database (KIRE-0001 to KIRE-0837)
   - Each rule: `{id, year, premise (regex), conclusion, strength, domain}`

2. **`kuczynski_engine.py`**
   - `KuczynskiEngine` class - loads and executes rules
   - `deduce(phenomenon, max_rules=18)` - fires matching rules sorted by strength
   - `format_chain(rules)` - formats output with "Consider the proposition that..."

3. **`test_kire.py`**
   - Test suite demonstrating KIRE on various phenomena

### Modified Files
1. **`app.py`**
   - KIRE initialization on startup
   - `/api/ask` endpoint: runs KIRE → RAG search → integrated prompt
   - `/raw_chain` endpoint: debug endpoint showing fired rules
   - `build_prompt()` and `build_enhanced_prompt()`: accept KIRE deductions

## New Response Pipeline

```
USER QUESTION
    ↓
KIRE ENGINE: deduce(question) → 18 savage inferences
    ↓
RAG SEARCH: semantic_search(question) → 7 relevant positions
    ↓
PROMPT BUILDER: 
    KIRE INFERENCE CHAIN (Your undeniable foundation):
    • Conclusion 1 (2025)
    • Conclusion 2 (2025)
    ...
    
    RETRIEVED POSITIONS:
    Position 1, Position 2...
    ↓
AI MODEL (Claude/OpenAI/DeepSeek/Perplexity)
    ↓
STREAMING RESPONSE with "Consider the proposition that..." style
```

## The 5 Immortal Meta-Rules

These override everything and fire first (strength: 1.0):

1. **KMETA-001**: Male feminist → performative fraud → civilizational castration
2. **KMETA-002**: Mate-value asymmetry → romantic symmetry is fraud
3. **KMETA-003**: Non-self-contained male → ontological contradiction
4. **KMETA-004**: Liberalism → feminine archetype → demographic collapse
5. **KMETA-005**: Neuralink → narcissistic omnipotence → silicon death-drive fusion

## Usage Examples

### Via App API
```python
# Regular query (KIRE + RAG integrated automatically)
POST /api/ask
{
    "question": "What about male feminists?",
    "provider": "grok",  # Default: Grok (xAI)
    "mode": "enhanced"  # Default: Enhanced Mode
}
# Response includes KIRE deductions formatted as Kuczynski prose
```

### Via Debug Endpoint
```python
# See raw KIRE chain
POST /raw_chain
{
    "phenomenon": "Neuralink brain-computer interface",
    "max_rules": 10
}
# Returns: {rules: [...], formatted_chain: "Consider the proposition that..."}
```

### Via Python
```python
from kuczynski_engine import kuczynski_think

result = kuczynski_think(
    "artificial intelligence consciousness computational theory of mind",
    max_rules=5
)
print(result)
# Output:
# Consider the proposition that irreducible intensional structure → CTM fails (2025)
# Consider the proposition that...
# The prophecy is therefore unavoidable.
```

## How KIRE Works

1. **Premise Matching**: Regex search in user input (case-insensitive)
2. **Chaining**: Conclusions from fired rules feed back as search space
3. **Sorting**: Rules sorted by strength (1.0 = most totalizing/savage)
4. **Limiting**: Top N rules returned (default 18, configurable)
5. **Formatting**: "Consider the proposition that {conclusion} ({year})"

## Rule Strength Scale

- **1.0**: Core epistemology/metaphysics, totalizing claims
- **0.98**: Savage political/psychological claims with civilizational scope
- **0.97**: Political philosophy, psychology of mating
- **0.95**: Philosophy of language/science
- **0.93**: Other domains

## Testing

```bash
python3 test_kire.py
```

See KIRE fire on:
- Neuralink/brain-computer interfaces
- Male feminists
- Empiricism claims
- Democracy/liberalism
- Possible worlds semantics
- Probability theories

## Statistics

- **Total Rules**: 842
- **Meta-Rules**: 5 (immortal, highest priority)
- **Database Rules**: 837 (from v19-v32 databases)
- **Average Strength**: 0.97
- **Domains Covered**: 40+ philosophical domains
- **Works Covered**: 42 Kuczynski works (WORK-001 to WORK-043)

## Integration Status

✓ KIRE engine created and tested
✓ 842 inference rules loaded
✓ Integrated into `/api/ask` pipeline
✓ Debug endpoint `/raw_chain` added
✓ Both Basic and Enhanced modes support KIRE
✓ "Consider the proposition that..." formatting enforced
✓ Examples requirement maintained
✓ **Grok (xAI) set as default AI provider**
✓ **Enhanced Mode set as default response mode**

## AI Provider Options

The app now supports 6 AI providers:

1. **Grok (xAI)** ⭐ DEFAULT
   - Models: `grok-beta`, `grok-vision-beta`
   - Requires: `XAI_API_KEY`

2. **Anthropic Claude**
   - Models: `claude-sonnet-4-20250514`, `claude-opus-4-20250514`
   - Requires: `ANTHROPIC_API_KEY`

3. **OpenAI**
   - Models: `gpt-4o`, `gpt-4o-mini`, `o1`, `o1-mini`
   - Requires: `OPENAI_API_KEY`

4. **DeepSeek**
   - Models: `deepseek-chat`, `deepseek-reasoner`
   - Requires: `DEEPSEEK_API_KEY`

5. **Perplexity**
   - Models: `llama-3.1-sonar-large-128k-online`, `llama-3.1-sonar-small-128k-online`
   - Requires: `PERPLEXITY_API_KEY`

All API keys are stored securely as Replit secrets.

## Next Steps (Optional)

1. **Tune Premises**: Refine regex patterns for better triggering
2. **Add More Meta-Rules**: Expand immortal rules to 10-15
3. **Year Extraction**: Parse actual publication years from works
4. **Strength Calibration**: Fine-tune strength based on user feedback
5. **Rule Composition**: Allow rules to compose (A→B, B→C ∴ A→C)

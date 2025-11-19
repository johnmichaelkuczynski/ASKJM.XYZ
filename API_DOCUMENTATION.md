# Internal Knowledge API Documentation

## Endpoint: `/api/internal/knowledge`

### Overview
Secure internal API endpoint for querying J.-M. Kuczynski's philosophical knowledge base. Integrates semantic search over 1,227 philosophical positions with KIRE (Kuczynski Inference Rule Engine) deductive reasoning.

### Authentication
**Required**: `ZHI_PRIVATE_KEY` in `Authorization` header

Supports two authentication formats:
- `Authorization: Bearer YOUR_ZHI_PRIVATE_KEY`
- `Authorization: YOUR_ZHI_PRIVATE_KEY`

### Request

**Method**: `POST`

**Headers**:
```
Content-Type: application/json
Authorization: Bearer YOUR_ZHI_PRIVATE_KEY
```

**Body**:
```json
{
  "query": "string (required)",
  "context": "string (optional)"
}
```

**Example**:
```bash
curl -X POST https://askjm.xyz/api/internal/knowledge \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ZHI_PRIVATE_KEY" \
  -d '{"query": "What is knowledge?", "context": "Epistemology"}'
```

### Response

**Success (200)**:
```json
{
  "result": "Formatted text with positions and KIRE inferences",
  "metadata": {
    "query": "user query",
    "context": "optional context",
    "positions_found": 5,
    "kire_rules_fired": 10,
    "database_size": 1227,
    "timestamp": "2025-11-19T01:14:00.000000",
    "positions": [
      {
        "position_id": "EP-111",
        "title": "Position title",
        "thesis": "Full philosophical position text",
        "source": "Source citation",
        "domain": "Epistemology",
        "similarity_score": 0.842
      }
    ],
    "kire_inferences": [
      {
        "id": "KIRE-0219",
        "premise": "analytic|truth|defined",
        "conclusion": "Analytic truths hold entirely in virtue of own content...",
        "strength": 1.0,
        "domain": "logic"
      }
    ]
  }
}
```

**Unauthorized (401)**:
```json
{
  "error": "Unauthorized",
  "message": "Invalid or missing authentication key"
}
```

**Bad Request (400)**:
```json
{
  "error": "Invalid request",
  "message": "Query parameter required"
}
```

**Server Error (500)**:
```json
{
  "error": "Internal server error",
  "message": "Error details"
}
```

### Features

#### Semantic Search
- Uses OpenAI `text-embedding-3-small` model
- Returns top 5 most relevant positions
- Includes similarity scores (0-1 range)
- Searches across 593 positions with valid embeddings

#### KIRE Inference Engine
- Applies 842 deductive reasoning rules
- Returns top 10 fired rules
- Includes premise patterns, conclusions, and strength scores
- Covers domains: logic, epistemology, metaphysics, ethics, etc.

#### Response Format
The `result` field contains formatted text suitable for display:
```
Query: What is knowledge?

Context: Epistemology

=== RELEVANT PHILOSOPHICAL POSITIONS ===

1. [EP-111] Position Title
   Full thesis text explaining the position...
   (Similarity: 0.842)

2. [EP-115] Another Position
   ...

=== KIRE INFERENCES ===

1. [KIRE-0219] Strength: 1.0
   If: analytic|truth|defined
   Then: Analytic truths hold entirely in virtue of own content...
```

### Security Notes

1. **Never expose** the `ZHI_PRIVATE_KEY` in client-side code
2. All unauthorized requests are denied with 401 status
3. Key must be set in Render.com environment variables for production
4. Requests are logged but authentication keys are never logged

### Deployment

**Development**: `http://localhost:5000/api/internal/knowledge`

**Production**: `https://askjm.xyz/api/internal/knowledge`

To deploy to production:
1. Commit changes to GitHub repository
2. Push to `johnmichaelkuczynski/ASKJM.XYZ.git`
3. Render.com will automatically deploy
4. Ensure `ZHI_PRIVATE_KEY` is set in Render environment variables

### Database Coverage

**Total Positions**: 1,722
- Economics (ECON-REFLEX series): 70 positions
- Epistemology (EP series): ~400 positions
- Metaphysics (META series): ~200 positions
- Philosophy of Mind (FODOR series): 15 positions
- Philosophy of Language (UID series): 9 positions
- Logic, Ethics, and other domains: ~1,000 positions

**Searchable Positions**: 593 (positions with both text content and position IDs)

### Example Queries

**Epistemology**:
```json
{"query": "What is the relationship between knowledge and belief?"}
```

**Conceptual Atomism**:
```json
{"query": "Fodor on conceptual atomism", "context": "Philosophy of mind"}
```

**Reference Theory**:
```json
{"query": "uniquely individuating descriptions", "context": "Philosophy of language"}
```

**Economics**:
```json
{"query": "reflexivity in economic systems", "context": "Philosophy of economics"}
```

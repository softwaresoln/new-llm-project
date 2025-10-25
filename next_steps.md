## Step 1: Semantic Chunking

**Code Changes Required:**

- Low-Medium complexity: Replace ~30 lines of chunking logic

- Files to modify: app.py (lines 78-106)

- New dependencies: spacy or nltk for sentence segmentation

- New functions needed: 2-3 helper functions for semantic splitting

**Specific Changes example:**

```python
# REPLACE THIS (lines 88-96):
for j in range(0, len(full_text), chunk_size):
    chunk = full_text[j:j + chunk_size]

# WITH THIS:
chunks = semantic_chunking(full_text, max_chunk_size=500)
```

Time Estimate: 2-4 hours
1 hour: Research and choose chunking strategy
1-2 hours: Implement semantic chunking function
1 hour: Testing and refinement

## Step 2: Upgrade Embedding Model and check output

**Code Changes Required:**

- Very Low complexity: Change 1 line of code
- Files to modify: app.py (line 108)
- New dependencies: None (same package, different model)
- No new functions needed

**Specific Changes:**
Time Estimate: 30 minutes - 1 hour
15 minutes: Change model name
15-45 minutes: Test and verify performance

### Example Query Quality comparison

1. GST Input Tax Credit Query:

```json
   POST /query
   {
     "question": "What is input tax credit under GST?"
   }
```

2. Complex Tax calculation:

```json
   POST /query
   {
     "question": "How to calculate GST on reverse charge mechanism?"
   }
```

3. Specific Section Query:
   ```json
   POST /query
   {
     "question": "What are the conditions for claiming ITC under Section 16?"
   }
   ```

**Performance Metrics to Check**

Before vs After Comparison:

| Metric              | Old Model (384D) | New Model (768D)       | Expected Improvement |
| ------------------- | ---------------- | ---------------------- | -------------------- |
| **Relevance Score** | ~0.6-0.7         | ~0.8-0.9               | +20-30%              |
| **Chunk Quality**   | Basic matching   | Semantic understanding | Much better          |
| **Tax Terms**       | Limited          | Excellent              | Significant          |
| **Context Match**   | Good             | Excellent              | +25%                 |

**Web Interface Testing**

1. **Open:** `http://localhost:5000`
2. **Ask these questions:**
   - "What is input tax credit?"
   - "GST reverse charge conditions"
   - "Section 16 ITC requirements"
3. **Check:** Are the retrieved chunks more relevant and contextually appropriate?

## Step 3: Hybrid Retrieval System

### **What to Implement:**

Add hybrid retrieval that combines:

- **Semantic search** (current vector similarity)
- **Keyword search** (BM25 or TF-IDF)
- **Query expansion** (synonyms and related terms)

### **Expected Output:**

```json
{
  "question": "GST input tax credit conditions",
  "results": {
    "semantic_chunks": [...],  // Vector similarity results
    "keyword_chunks": [...],   // Keyword matching results
    "expanded_queries": ["GST ITC", "input tax credit", "tax credit conditions"],
    "combined_score": 0.85,
    "retrieval_method": "hybrid"
  }
}
```

### **Implementation Scope:**

- **Code changes:** ~50-80 lines
- **New dependencies:** `rank_bm25`, `nltk`
- **New functions:** 3-4 functions for keyword search and query expansion
- **Time estimate:** 4-6 hours

### **Success Criteria:**

- Retrieval relevance >85%
- Better handling of technical tax terms
- Improved recall for edge cases

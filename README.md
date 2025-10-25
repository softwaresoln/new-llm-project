# AI-Powered Tax & GST Assistant

Tax is an intelligent, domain-specific chatbot built using Flask, LangChain, ChromaDB, and OpenRouter API. It can answer tax and GST-related questions by retrieving relevant context from uploaded or sample knowledge bases.

## Features

- ✅ Flask-based REST API for chatbot and retrieval
- ✅ Retrieval-Augmented Generation (RAG) using LangChain + Chroma
- ✅ SentenceTransformer embeddings (all-MiniLM-L6-v2)
- ✅ OpenRouter model integration (e.g., qwen/qwen3-4b:free)
- ✅ Metadata for sections, source, and chunk indices
- ✅ Auto cleanup of Chroma DB on exit
- ✅ Configurable .env parameters
- ✅ Modern web interface with real-time chat

## Project Structure

```
TaxAJ-Chatbot/
├── app.py                  # Flask backend (main logic)
├── sample2.txt             # Example knowledge base
├── templates/
│   └── index.html          # Web interface
├── chroma_db/              # Auto-generated vector database
├── .env                    # Environment configuration
├── requirements.txt        # Dependencies
└── README.md               # Documentation
```

## Environment Setup

### 1. Create a .env file

Create a `.env` file in the project root with the following variables:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_MODEL=qwen/qwen3-4b:free
OPENROUTER_PROVIDER=
SAMPLE_FILE=sample2.txt
CHROMA_DB_PATH=./chroma_db
REQUEST_TIMEOUT=30
PORT=5000
```

> Get your OpenRouter API key from [https://openrouter.ai/keys](https://openrouter.ai/keys)

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Server

```bash
python3 app.py
```

Then open: 👉 [http://localhost:5000](http://localhost:5000)

## Quick Start

1. **Clone and setup:**

   ```bash
   git clone <your-repo>
   cd new-llm-project
   cp .env.example .env
   # Edit .env and add your OpenRouter API key
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**

   ```bash
   python3 app.py
   ```

4. **Access the web interface:**
   - Open your browser to `http://localhost:5000`
   - Use the chat interface to ask tax-related questions
   - The app will automatically process your `sample2.txt` file

**That's it!** Your Tax AI Assistant is now running.

## API Endpoints

### POST /query

Retrieves relevant chunks from the knowledge base.

**Request:**

```json
{
  "question": "What is input tax credit under GST?"
}
```

**Response:**

```json
{
  "question": "What is input tax credit under GST?",
  "top_chunks": [
    {
      "content": "Section 16: Eligibility and conditions for taking input tax credit...",
      "source": "sample2.txt",
      "section": "Section 16",
      "chunk_index": 0,
      "score": 0.89
    }
  ]
}
```

### POST /chat

Generates a contextual answer using retrieved chunks.

**Request:**

```json
{
  "question": "Explain GST composition scheme."
}
```

**Response:**

```json
{
  "question": "Explain GST composition scheme.",
  "reply": "Under GST, the composition scheme allows small taxpayers...",
  "sources": [
    {
      "source": "sample2.txt",
      "section": "Section 10",
      "chunk_index": 1
    }
  ]
}
```

### GET /health

Checks the service status.

**Response:**

```json
{
  "status": "healthy",
  "message": "Service is running"
}
```

## Workflow Diagram

```
┌───────────────────────────┐
│ Sample File (sample2.txt) │
└─────────┬─────────────────┘
          │
          ▼
┌───────────────────────────┐
│ Split Text into 500-char  │
│        Chunks             │
└─────────┬─────────────────┘
          │
          ▼
┌─────────────────────────┐
│ Generate Embeddings     │
│   (SentenceTransformer) │
└─────────┬───────────────┘
          │
          ▼
┌─────────────────────────┐
│ Store in ChromaDB with  │
│       Metadata          │
└─────────┬───────────────┘
          │
          ▼
┌─────────────────────────┐
│ Retriever: Find Top 3   │
│    Relevant Chunks      │
└─────────┬───────────────┘
          │
          ▼
┌─────────────────────────┐
│ Create Context with     │
│     PromptTemplate      │
└─────────┬───────────────┘
          │
          ▼
┌─────────────────────────┐
│ OpenRouter API          │
│   (Qwen/Qwen3-4B)       │
└─────────┬───────────────┘
          │
          ▼
┌─────────────────────────┐
│    AI Reply Returned    │
└─────────────────────────┘
```

This diagram shows how text is embedded, stored, retrieved, and used to generate contextual AI responses.

## Automatic Cleanup

When the app stops, it deletes the ChromaDB directory to prevent stale data:

```python
atexit.register(cleanup_chroma_db)
```

---

## Future Development

### **Option 1: Custom LLM Development**

- **Timeline**: 6-8 months | **Cost**: High
- **Approach**: Build a completely custom LLM trained on tax domain data
- **Benefits**: Complete control, no API costs, domain expertise
- **Challenges**: High cost, long development time, complex maintenance

### **Option 2: Enhanced RAG System (Recommended for now)**

- **Timeline**: 2-3 months | **Cost**: Low
- **Approach**: Improve current RAG system with advanced techniques
- **Benefits**: Quick wins, low risk, immediate improvements
- **Improvements**: Better retrieval, optimized prompts, performance monitoring

### **Option 3: Hybrid Approach**

- **Timeline**: 4-6 months | **Cost**: Medium
- **Approach**: Combine enhanced RAG with selective custom models
- **Benefits**: Balanced approach, gradual migration, best of both worlds

## Development Options Comparison

| Factor            | Option 1   | **Option 2 **  | Option 3 (Hybrid) |
| ----------------- | ---------- | -------------- | ----------------- |
| **Timeline**      | 6-8 months | **2-3 months** | 4-6 months        |
| **Cost**          | High       | Low            | Medium            |
| **Complexity**    | High       | **Medium**     | High-Medium       |
| **Control**       | Complete   | **Limited**    | Partial           |
| **Customization** | Full       | **Limited**    | Selective         |
| **Risk**          | High       | **Low**        | Medium            |
| **ROI Timeline**  | 12+ months | **3-6 months** | 6-12 months       |

**Recommended: Option 2 (Enhanced RAG System)**

## Recommended Development Path

### **Immediate Action (Next 3 months):**

1. **Implement Option 2** for quick wins and immediate improvements
2. **Collect data** for future custom model development
3. **Engage tax experts** for validation and feedback
4. **Build pilot** for specific tax area (e.g., GST)

### **Medium-term (6-12 months):**

1. **Evaluate Option 2 results** and measure improvements
2. **Start Option 3 implementation** if needed
3. **Gradual custom model integration** for specific areas
4. **Scale based on success** and user feedback

### **Long-term (12+ months):**

1. **Consider Option 1** only if complete control is needed
2. **Complete domain expertise** through specialized models
3. **Advanced tax calculations** and automation
4. **Enterprise features** and multi-tenancy

## Option 2: Enhanced RAG System - Detailed Plan

### **Phase 1: Enhanced Retrieval System (Weeks 1-4)**

#### **Current Issues:**

- Fixed 500-character chunks (too rigid)
- Basic embedding model (all-MiniLM-L6-v2)
- Simple similarity search only
- No query expansion or reranking

#### **Improvements:**

- **Semantic Chunking**: Intelligent document splitting
- **Better Embeddings**: Upgrade to all-mpnet-base-v2 (768 dimensions)
- **Hybrid Retrieval**: Combine semantic + keyword search
- **Query Expansion**: Expand user queries for better matching
- **Reranking**: Use cross-encoder models for better relevance

#### **Implementation Tasks:**

- [ ] **Week 1**: Implement semantic chunking
- [ ] **Week 2**: Upgrade embedding models
- [ ] **Week 3**: Add hybrid retrieval system
- [ ] **Week 4**: Test and optimize retrieval quality

### **Phase 2: Advanced Prompt Engineering (Weeks 5-8)**

#### **Current Prompt:**

```
You are a helpful assistant named TaxAJ. Use the following GST context to answer the question.
If the context does not contain the answer, answer based on your general tax knowledge.

Context: {context}
Question: {question}
Answer:
```

#### **Enhanced Prompts:**

- **Specialized Templates**: Different prompts for GST, Income Tax, calculations
- **Few-Shot Learning**: Include examples in prompts
- **Chain-of-Thought**: Step-by-step reasoning
- **Domain-Specific Instructions**: Tax expert persona and guidelines

#### **Implementation Tasks:**

- [ ] **Week 5**: Create specialized prompt templates
- [ ] **Week 6**: Implement few-shot learning
- [ ] **Week 7**: Add chain-of-thought reasoning
- [ ] **Week 8**: Test and optimize prompts

### **Phase 3: System Integration & Optimization (Weeks 9-12)**

#### **Performance Monitoring:**

- Response time tracking
- Accuracy metrics
- User satisfaction scores
- Retrieval quality assessment

#### **Caching System:**

- Redis-based response caching
- Query deduplication
- Smart cache invalidation
- Performance optimization

#### **A/B Testing Framework:**

- Experiment management
- Variant testing
- Results tracking
- Statistical significance

#### **Implementation Tasks:**

- [ ] **Week 9**: Implement performance monitoring
- [ ] **Week 10**: Add caching system
- [ ] **Week 11**: Create A/B testing framework
- [ ] **Week 12**: Deploy and test integrated system

## Expected Improvements

### **Performance Metrics:**

- **Response Accuracy**: +15-25% improvement
- **Response Time**: <2 seconds (vs current 3-5 seconds)
- **Retrieval Quality**: +30% relevance score
- **User Satisfaction**: +20% satisfaction rating

### **Technical Improvements:**

- **Better Chunking**: Semantic vs fixed-size
- **Smarter Retrieval**: Hybrid semantic + keyword
- **Optimized Prompts**: Domain-specific templates
- **Performance Monitoring**: Real-time metrics

### **Cost Benefits:**

- **Reduced API Calls**: 30-40% reduction through caching
- **Better Efficiency**: Faster responses, less compute
- **Improved ROI**: Better user experience

## Success Criteria

### **Technical Success:**

- [ ] Response time <2 seconds
- [ ] Accuracy improvement >15%
- [ ] Retrieval relevance >80%
- [ ] System uptime >99%

### **Business Success:**

- [ ] User satisfaction >4.5/5
- [ ] Query resolution rate >90%
- [ ] Cost reduction >30%
- [ ] User engagement +25%

## Summary of Next Steps

### **Week 1-2: Enhanced Retrieval**

- Implement semantic chunking
- Upgrade embedding models
- Add hybrid retrieval (semantic + keyword)

### **Week 3-4: Prompt Engineering**

- Create specialized prompt templates
- Add few-shot learning examples
- Implement chain-of-thought reasoning

### **Week 5-6: System Integration**

- Add performance monitoring
- Implement caching system
- Create A/B testing framework

### **Week 7-8: Testing & Optimization**

- Deploy and test integrated system
- Measure improvements
- Optimize based on results

**Expected Results:**

- **15-25% accuracy improvement**
- **<2 second response time**
- **30% reduction in API costs**
- **20% improvement in user satisfaction**

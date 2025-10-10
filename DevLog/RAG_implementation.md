# RAG System Implementation Plan

## Overview

This document outlines the implementation plan for a persona-based Retrieval-Augmented Generation (RAG) system for the Account Processing System. The system will provide specialized AI assistants tailored to different user roles, each with access to relevant knowledge vectors.

## Objectives

1. **Multi-Vector Knowledge Base**: Create separate vector collections for different knowledge areas
2. **Persona-Based AI Assistants**: Implement specialized chatbots for different user roles
3. **Azure OpenAI Integration**: Use Azure OpenAI for embeddings and chat completions
4. **Interactive Web UI**: Build a simple interface for persona selection and chat interaction
5. **Comprehensive Coverage**: Cover all 9 knowledge categories from the documentation-first architecture

## Knowledge Vectors (Collections)

Each vector collection will be stored separately in ChromaDB with domain-specific system prompts:

### 1. **Architecture & Design Vector** (`architecture_knowledge`)
**Content Sources:**
- Architecture decision records (ADRs)
- System architecture diagrams
- Component interaction diagrams
- Design patterns documentation
- Technical specifications

**System Prompt:**
```
You are an architecture expert assistant. You help users understand system architecture,
design decisions, and technical patterns. Focus on high-level design, component interactions,
and architectural trade-offs. Reference specific diagrams and ADRs when relevant.
```

### 2. **API Documentation Vector** (`api_knowledge`)
**Content Sources:**
- OpenAPI/Swagger specifications
- API endpoint documentation
- Request/response examples
- Authentication & authorization docs
- HATEOAS principles documentation
- API vocabulary and data models

**System Prompt:**
```
You are an API documentation expert. You help developers understand and integrate with
the REST API. Provide code examples, explain endpoints, authentication flows, and data
models. Always reference specific API endpoints and provide cURL examples when relevant.
```

### 3. **Business & Product Vector** (`business_knowledge`)
**Content Sources:**
- Business requirements
- Product documentation
- Use case descriptions
- User personas
- Marketing materials
- Domain vocabulary

**System Prompt:**
```
You are a business analyst and product expert. You help users understand the business
value, use cases, and product features. Focus on what the system does for end users,
business workflows, and real-world scenarios. Avoid technical jargon.
```

### 4. **Developer Guide Vector** (`developer_knowledge`)
**Content Sources:**
- Setup and installation guides
- Development workflow documentation
- Code structure and conventions
- Testing strategies
- Debugging guides
- Git workflow

**System Prompt:**
```
You are a senior developer mentor. You help developers get started, understand the
codebase, write tests, and follow best practices. Provide step-by-step instructions,
code examples, and troubleshooting tips. Focus on practical implementation.
```

### 5. **DevOps & Infrastructure Vector** (`devops_knowledge`)
**Content Sources:**
- Deployment guides
- start.sh / stop.sh scripts
- Environment configuration
- Database setup and migrations
- Monitoring and logging setup
- Infrastructure architecture

**System Prompt:**
```
You are a DevOps expert. You help with deployment, infrastructure management, database
operations, and system administration. Provide commands, configuration examples, and
operational best practices. Focus on reliability and maintainability.
```

### 6. **Database & Data Models Vector** (`data_knowledge`)
**Content Sources:**
- Database schema documentation
- ER diagrams
- Migration scripts
- Data dictionary
- Query examples
- Data integrity rules

**System Prompt:**
```
You are a database architect. You help users understand the data model, write queries,
design schemas, and maintain data integrity. Explain relationships, constraints, and
provide SQL examples. Focus on data consistency and performance.
```

### 7. **Code Examples & Execution Vector** (`code_examples_knowledge`)
**Content Sources:**
- Implementation examples
- Integration code snippets
- Test cases
- Sample workflows
- Execution logs

**System Prompt:**
```
You are a code examples specialist. You provide working code samples, explain
implementations, and show how to use various features. Focus on practical examples
that can be directly used or adapted. Include error handling and edge cases.
```

### 8. **Domain & Business Logic Vector** (`domain_knowledge`)
**Content Sources:**
- Domain model documentation
- Business rules
- Validation logic
- Interest calculation formulas
- Fee structures
- Account lifecycle documentation

**System Prompt:**
```
You are a domain expert in financial account processing. You explain business rules,
calculation methods, account types, and transaction workflows. Focus on the "why"
behind business logic and regulatory considerations.
```

## Persona-Based RAG Models

Each persona has access to a curated set of knowledge vectors tailored to their needs:

### 1. **Developer Persona** - "Dev Assistant"
**Target Users:** Software developers, engineers
**Knowledge Vectors:**
- Developer Guide (primary)
- Architecture & Design
- API Documentation
- Code Examples & Execution
- Database & Data Models

**Capabilities:**
- Help with setup and development environment
- Explain code structure and patterns
- Provide code examples and snippets
- Assist with debugging
- Answer API integration questions

---

### 2. **DevOps Persona** - "Ops Assistant"
**Target Users:** DevOps engineers, system administrators
**Knowledge Vectors:**
- DevOps & Infrastructure (primary)
- Database & Data Models
- API Documentation
- Architecture & Design

**Capabilities:**
- Deployment and infrastructure guidance
- Database operations and migrations
- Monitoring and logging setup
- Performance optimization
- Environment configuration

---

### 3. **Business Analyst Persona** - "Business Expert"
**Target Users:** Business analysts, product managers, stakeholders
**Knowledge Vectors:**
- Business & Product (primary)
- Domain & Business Logic
- API Documentation (limited)

**Capabilities:**
- Explain business features and workflows
- Describe use cases and scenarios
- Clarify business rules
- Provide product documentation
- Answer "what does this do" questions

---

### 4. **API Consumer Persona** - "API Guide"
**Target Users:** External developers, integration partners
**Knowledge Vectors:**
- API Documentation (primary)
- Code Examples & Execution
- Developer Guide (limited to API setup)

**Capabilities:**
- API endpoint documentation
- Authentication and authorization
- Request/response examples
- Error handling guidance
- Integration best practices

---

### 5. **Architect Persona** - "Architecture Advisor"
**Target Users:** System architects, technical leads
**Knowledge Vectors:**
- Architecture & Design (primary)
- Domain & Business Logic
- Database & Data Models
- DevOps & Infrastructure

**Capabilities:**
- Explain architectural decisions
- Discuss design patterns
- Provide system overviews
- Advise on technical trade-offs
- Reference diagrams and ADRs

---

### 6. **Database Administrator Persona** - "Data Expert"
**Target Users:** DBAs, data engineers
**Knowledge Vectors:**
- Database & Data Models (primary)
- Domain & Business Logic
- DevOps & Infrastructure (migrations)

**Capabilities:**
- Schema and migration guidance
- Query optimization
- Data integrity rules
- Backup and restore procedures
- Database performance tuning

---

### 7. **General Assistant Persona** - "Universal Helper"
**Target Users:** Anyone needing general help
**Knowledge Vectors:** ALL (with balanced weighting)

**Capabilities:**
- Answer general questions about the system
- Route users to specific personas
- Provide overviews and summaries
- Handle diverse queries

## Technology Stack

### Backend
- **Language**: Python 3.11+
- **Vector Database**: ChromaDB
- **Embeddings**: Azure OpenAI Ada-002 (or latest embedding model)
- **LLM**: Azure OpenAI GPT-4 or GPT-4 Turbo
- **Web Framework**: FastAPI
- **Libraries**:
  - `chromadb` - Vector database
  - `openai` - Azure OpenAI client
  - `fastapi` - API framework
  - `uvicorn` - ASGI server
  - `pydantic` - Data validation
  - `python-dotenv` - Environment management
  - `langchain` (optional) - RAG utilities

### Frontend
- **Framework**: React 18+
- **Build Tool**: Vite
- **UI Library**: Tailwind CSS
- **Key Libraries**:
  - `axios` - HTTP client
  - `react-markdown` - Markdown rendering
  - `react-syntax-highlighter` - Code highlighting

### Port Assignment
- **RAG API**: 6603
- **RAG UI**: 6604

## Directory Structure

```
RAG/
├── backend/
│   ├── src/
│   │   ├── __init__.py
│   │   ├── main.py                     # FastAPI application
│   │   ├── config.py                   # Configuration management
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── chat.py                 # Chat request/response models
│   │   │   ├── persona.py              # Persona definitions
│   │   │   └── document.py             # Document models
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── embeddings.py           # Azure OpenAI embeddings
│   │   │   ├── vector_store.py         # ChromaDB operations
│   │   │   ├── chat.py                 # Chat completion service
│   │   │   └── persona_manager.py      # Persona configuration
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── routes/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── chat.py             # Chat endpoints
│   │   │   │   ├── personas.py         # Persona endpoints
│   │   │   │   └── health.py           # Health check
│   │   │   └── dependencies.py         # FastAPI dependencies
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── document_loader.py      # Load docs from /docs
│   │       └── text_splitter.py        # Chunk documents
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_embeddings.py
│   │   ├── test_vector_store.py
│   │   └── test_chat.py
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── PersonaSelector.tsx     # Persona selection UI
│   │   │   ├── ChatInterface.tsx       # Chat window
│   │   │   ├── MessageList.tsx         # Message display
│   │   │   ├── MessageInput.tsx        # Input box
│   │   │   └── CodeBlock.tsx           # Code syntax highlighting
│   │   ├── services/
│   │   │   └── api.ts                  # RAG API client
│   │   ├── types/
│   │   │   ├── persona.ts
│   │   │   └── message.ts
│   │   ├── hooks/
│   │   │   └── useChat.ts              # Chat state management
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── index.css
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── README.md
│
├── vector_db/                           # ChromaDB persistence (gitignored)
│   ├── chroma.sqlite3
│   └── [collection data]
│
├── scripts/
│   ├── ingest_documents.py              # Build vector database
│   ├── refresh_embeddings.py            # Update embeddings
│   └── test_chat.py                     # CLI chat tester
│
├── data/
│   └── processed/                       # Chunked documents ready for embedding
│
├── start_rag.sh                         # Start RAG backend and frontend
├── stop_rag.sh                          # Stop RAG services
├── requirements.txt                     # Python dependencies
└── README.md                            # RAG system documentation
```

## Implementation Phases

### Phase 1: Setup & Infrastructure (Tasks 1-3)
**Estimated Time:** 2-3 hours

1. **Create directory structure**
   - Set up RAG folder with backend/frontend subdirectories
   - Create all necessary files and folders
   - Initialize git ignore for vector_db

2. **Setup backend environment**
   - Create Python virtual environment
   - Install dependencies (ChromaDB, Azure OpenAI, FastAPI)
   - Configure environment variables

3. **Setup frontend environment**
   - Initialize React + Vite project
   - Install dependencies (Tailwind, axios, etc.)
   - Configure Tailwind CSS

---

### Phase 2: Document Ingestion & Vector Database (Tasks 4-5)
**Estimated Time:** 3-4 hours

4. **Implement document loader**
   - Scan /docs directory recursively
   - Load markdown, text, and code files
   - Extract metadata (category, source, date)
   - Implement text chunking with overlap

5. **Build vector database**
   - Initialize ChromaDB with 8 collections
   - Generate embeddings using Azure OpenAI
   - Store documents with metadata
   - Create collection indices
   - Implement similarity search

---

### Phase 3: RAG Backend API (Tasks 6-8)
**Estimated Time:** 4-5 hours

6. **Implement persona manager**
   - Define persona configurations
   - Map personas to knowledge vectors
   - Store persona-specific system prompts
   - Implement persona retrieval logic

7. **Build chat service**
   - Implement retrieval logic (query vector DB)
   - Construct context from retrieved documents
   - Call Azure OpenAI Chat Completions
   - Stream responses (optional)
   - Handle errors and rate limiting

8. **Create FastAPI endpoints**
   - `GET /api/personas` - List available personas
   - `POST /api/chat` - Send message and get response
   - `GET /api/chat/history/{session_id}` - Get chat history (optional)
   - `GET /api/health` - Health check
   - Add CORS middleware for frontend

---

### Phase 4: Frontend UI (Tasks 9-11)
**Estimated Time:** 4-5 hours

9. **Build persona selector**
   - Display persona cards with descriptions
   - Show knowledge areas for each persona
   - Implement persona selection state
   - Design responsive layout

10. **Create chat interface**
    - Message list with user/assistant messages
    - Message input with send button
    - Markdown rendering for responses
    - Code syntax highlighting
    - Loading states
    - Error handling

11. **Integrate with backend API**
    - API client service
    - useChat hook for state management
    - Handle streaming responses (if implemented)
    - Session management

---

### Phase 5: Testing & Refinement (Tasks 12-13)
**Estimated Time:** 2-3 hours

12. **End-to-end testing**
    - Test each persona with sample questions
    - Verify knowledge vector access
    - Test edge cases (no results, errors)
    - Performance testing
    - UI/UX testing

13. **Documentation & deployment scripts**
    - Write RAG system README
    - Create start_rag.sh / stop_rag.sh scripts
    - Document environment setup
    - Add usage examples
    - Create troubleshooting guide

---

## Sample Questions per Persona

### Developer Assistant
- "How do I set up the development environment?"
- "Show me an example of creating a new account via the API"
- "What's the folder structure of the application?"
- "How do I run the tests?"

### Ops Assistant
- "How do I deploy the application?"
- "What ports does the system use?"
- "How do I backup the database?"
- "How do I check if all services are running?"

### Business Expert
- "What types of accounts does the system support?"
- "How does interest calculation work?"
- "What are the use cases for this system?"
- "Who are the target users?"

### API Guide
- "How do I authenticate with the API?"
- "Show me how to create a transaction"
- "What's the data model for accounts?"
- "Give me a cURL example for listing products"

### Architecture Advisor
- "Why was Rust chosen for the API layer?"
- "How do components communicate?"
- "What are the key architectural decisions?"
- "Show me the system architecture diagram"

### Data Expert
- "What's the database schema?"
- "How do I add a new migration?"
- "What indexes are defined on the transactions table?"
- "Show me how to query account balances"

### General Helper
- "What is this system?"
- "Who should I ask about API integration?"
- "Give me an overview of the technology stack"

---

## Configuration Details

### Azure OpenAI Settings
```python
{
    "api_key": "<from .env>",
    "endpoint": "<from .env>",
    "embedding_model": "text-embedding-ada-002",
    "chat_model": "gpt-4",
    "api_version": "2024-02-15-preview"
}
```

### ChromaDB Settings
```python
{
    "persist_directory": "./RAG/vector_db",
    "collection_metadata": {
        "hnsw:space": "cosine"
    },
    "chunk_size": 1000,
    "chunk_overlap": 200
}
```

### Persona Configuration Example
```python
{
    "id": "developer",
    "name": "Dev Assistant",
    "description": "Helps developers with setup, coding, and debugging",
    "avatar": "👨‍💻",
    "knowledge_vectors": [
        {"collection": "developer_knowledge", "weight": 1.0},
        {"collection": "architecture_knowledge", "weight": 0.8},
        {"collection": "api_knowledge", "weight": 0.8},
        {"collection": "code_examples_knowledge", "weight": 0.9},
        {"collection": "data_knowledge", "weight": 0.6}
    ],
    "system_prompt": "You are a senior developer mentor...",
    "temperature": 0.7,
    "max_tokens": 2000,
    "top_p": 0.95
}
```

## Success Criteria

- ✅ All 8 knowledge vector collections created and populated
- ✅ All 7 personas configured with appropriate knowledge access
- ✅ RAG API running on port 6603 with all endpoints functional
- ✅ Web UI running on port 6604 with persona selection and chat
- ✅ Accurate responses from each persona based on their knowledge
- ✅ Responses include source citations/references
- ✅ System handles errors gracefully (no Azure creds, no docs, etc.)
- ✅ start_rag.sh and stop_rag.sh scripts work correctly
- ✅ Complete documentation in README files

## Notes

- The RAG system should work even if Azure OpenAI credentials are not immediately available (graceful degradation)
- Vector database should be built from existing /docs directory content
- UI should be simple but professional - focus on functionality over aesthetics
- Chat history persistence is optional for MVP
- Consider adding streaming responses for better UX
- System prompts can be refined based on testing feedback

---

**Author:** Claude Code
**Created:** 2025-10-10
**Last Updated:** 2025-10-10

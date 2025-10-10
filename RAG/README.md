# RAG System - AI Documentation Assistant

## Overview

A persona-based Retrieval-Augmented Generation (RAG) system that provides specialized AI assistants for the Account Processing System documentation.

## Features

- **7 Specialized AI Personas**: Each tailored for different roles (Developer, DevOps, Business Analyst, API Consumer, Architect, DBA, General Assistant)
- **8 Knowledge Vectors**: Separate collections for Architecture, API, Business, Developer, DevOps, Data, Code Examples, and Domain knowledge
- **Azure OpenAI Integration**: Uses Azure OpenAI for embeddings and chat completions
- **Interactive Web UI**: Simple HTML/JavaScript interface for persona selection and chat
- **FastAPI Backend**: RESTful API with OpenAPI documentation

## Architecture

```
┌──────────────┐
│   Web UI     │  (Port 6604)
│  (HTML/JS)   │
└──────┬───────┘
       │ HTTP
       ↓
┌──────────────┐
│  FastAPI     │  (Port 6603)
│  RAG API     │
└──────┬───────┘
       │
    ┌──┴──┐
    ↓     ↓
┌────────┐  ┌────────────┐
│ ChromaDB│  │ Azure OpenAI│
│ Vectors │  │  (Chat+Emb) │
└─────────┘  └─────────────┘
```

## Prerequisites

- Python 3.11+
- Azure OpenAI account with:
  - GPT-4 (or GPT-4 Turbo) deployment for chat
  - text-embedding-ada-002 deployment for embeddings
- Documentation in `/docs` directory

## Quick Start

### 1. Configure Environment

Edit `backend/.env` with your Azure OpenAI credentials:

```bash
# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=<your_actual_api_key>
AZURE_OPENAI_ENDPOINT=https://<your-resource-name>.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=<your_gpt4_deployment>
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=<your_embedding_deployment>
AZURE_OPENAI_API_VERSION=2024-02-15-preview

# RAG Configuration
RAG_API_PORT=6603
CHROMA_PERSIST_DIRECTORY=../vector_db
DOCS_PATH=../../docs

# LLM Settings
TEMPERATURE=0.7
MAX_TOKENS=2000
TOP_P=0.95

# CORS
CORS_ORIGINS=http://localhost:6604,http://localhost:5173
```

### 2. Ingest Documentation

This creates the vector database from your documentation:

```bash
cd /Users/gpanagiotopoulos/goodbyeSwagger/RAG
source backend/.venv/bin/activate
python3 scripts/ingest_documents.py
```

The script will:
- Scan the `/docs` directory
- Chunk documents into 1000-character segments
- Generate embeddings using Azure OpenAI
- Store in ChromaDB collections by category

### 3. Start the RAG System

```bash
./start_rag.sh
```

This starts:
- **RAG API** on http://localhost:6603
- **RAG UI** on http://localhost:6604

### 4. Access the System

- **Web UI**: http://localhost:6604
- **API Docs**: http://localhost:6603/api/docs
- **Health Check**: http://localhost:6603/api/health

### 5. Stop the System

```bash
./stop_rag.sh
```

## Available Personas

### 1. 👨‍💻 Dev Assistant
**Role**: Software Developer
**Knowledge**: Developer guides, architecture, API, code examples, data models
**Use for**: Setup, coding, debugging, understanding codebase

### 2. 🔧 Ops Assistant
**Role**: DevOps Engineer
**Knowledge**: DevOps, infrastructure, database operations, API
**Use for**: Deployment, database ops, monitoring, system admin

### 3. 💼 Business Expert
**Role**: Business Analyst
**Knowledge**: Business docs, domain knowledge, API (limited)
**Use for**: Features, use cases, business workflows, requirements

### 4. 🔌 API Guide
**Role**: External Developer
**Knowledge**: API docs, code examples, developer setup
**Use for**: API integration, endpoints, authentication

### 5. 🏛️ Architecture Advisor
**Role**: System Architect
**Knowledge**: Architecture, domain, data models, DevOps
**Use for**: Design decisions, patterns, system overview, trade-offs

### 6. 🗄️ Data Expert
**Role**: Database Administrator
**Knowledge**: Data models, domain, DevOps (migrations)
**Use for**: Schema, queries, migrations, data integrity

### 7. 🤖 Universal Helper
**Role**: General Assistant
**Knowledge**: ALL knowledge areas (balanced)
**Use for**: General questions, overviews, routing to specialists

## API Endpoints

### GET /api/personas
Get list of all available personas

```bash
curl http://localhost:6603/api/personas
```

### POST /api/chat
Send a message to a persona

```bash
curl -X POST http://localhost:6603/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "persona_id": "developer",
    "message": "How do I run tests?",
    "conversation_history": []
  }'
```

Response includes:
- Assistant's answer
- Source documents used
- Relevance scores

### GET /api/health
Check system health and collection stats

```bash
curl http://localhost:6603/api/health
```

## Project Structure

```
RAG/
├── backend/
│   ├── src/
│   │   ├── models/          # Data models (Persona, Document, Chat)
│   │   ├── services/        # Core services (Embeddings, Vector Store, Chat)
│   │   ├── api/routes/      # FastAPI endpoints
│   │   ├── utils/           # Document loader utilities
│   │   ├── config.py        # Configuration management
│   │   └── main.py          # FastAPI application
│   ├── .env                 # Environment configuration
│   ├── .venv/               # Python virtual environment
│   └── requirements.txt     # Python dependencies
├── frontend/
│   └── index.html           # Single-page web application
├── vector_db/               # ChromaDB persistence (gitignored)
├── scripts/
│   └── ingest_documents.py  # Document ingestion script
├── start_rag.sh             # Start script
├── stop_rag.sh              # Stop script
└── README.md                # This file
```

## Knowledge Vector Collections

| Collection | Content | System Prompt Focus |
|------------|---------|---------------------|
| architecture_knowledge | ADRs, diagrams, design docs | High-level design, patterns, trade-offs |
| api_knowledge | OpenAPI specs, endpoints, auth | API integration, examples, data models |
| business_knowledge | Requirements, use cases, personas | Business value, workflows, features |
| developer_knowledge | Setup guides, coding standards | Development, testing, debugging |
| devops_knowledge | Deployment, infrastructure, monitoring | Operations, reliability, maintenance |
| data_knowledge | Schema, ER diagrams, migrations | Database design, queries, integrity |
| code_examples_knowledge | Code snippets, integration examples | Working code, practical implementations |
| domain_knowledge | Business rules, calculations | Domain logic, business processes |

## Troubleshooting

### "No documents found to ingest"

**Problem**: The `/docs` directory is empty or doesn't exist
**Solution**: Ensure you have documentation in the `docs` directory at the project root

### "Azure OpenAI validation error"

**Problem**: Missing or invalid Azure OpenAI credentials
**Solution**: Edit `backend/.env` with your actual Azure OpenAI credentials

### "Collection has 0 documents"

**Problem**: Document ingestion didn't run or failed
**Solution**: Run `python3 scripts/ingest_documents.py` and check for errors

### "CORS error" in browser

**Problem**: Frontend can't connect to API
**Solution**: Check that both API and UI are running, verify CORS_ORIGINS in .env

### Port already in use

**Problem**: Port 6603 or 6604 is already taken
**Solution**: Stop other services or change ports in .env and start_rag.sh

## Development

### Running in Development Mode

```bash
# Backend with auto-reload
cd backend
source .venv/bin/activate
uvicorn src.main:app --reload --host 0.0.0.0 --port 6603

# Frontend (separate terminal)
cd frontend
python3 -m http.server 6604
```

### Running Tests

```bash
cd backend
source .venv/bin/activate
pytest
```

### Updating Dependencies

```bash
cd backend
source .venv/bin/activate
pip install --upgrade -r requirements.txt
```

### Rebuilding Vector Database

To refresh embeddings after documentation changes:

```bash
cd /Users/gpanagiotopoulos/goodbyeSwagger/RAG
source backend/.venv/bin/activate
python3 scripts/ingest_documents.py
# Select "yes" when prompted to reset collections
```

## Performance Tips

- **Initial Load**: First embedding generation takes 5-10 minutes depending on documentation size
- **Query Response**: Typical response time is 2-5 seconds
- **Token Limits**: Reduce MAX_CONTEXT_TOKENS in .env if hitting token limits
- **Collection Size**: Each collection stores ~1000-character chunks with embeddings

## Logs

- **API Log**: `rag_api.log`
- **UI Log**: `rag_ui.log`

View live logs:
```bash
tail -f rag_api.log
```

## Integration with Main System

The RAG system runs alongside the Account Processing System:

- **Accounts API**: Port 6600
- **Accounts UI**: Port 6601
- **Database**: Port 6602
- **RAG API**: Port 6603 ✨
- **RAG UI**: Port 6604 ✨

Both systems are independent but share documentation from the `/docs` directory.

## Future Enhancements

- [ ] Conversation history persistence
- [ ] User authentication
- [ ] Streaming responses
- [ ] Multi-language support
- [ ] Custom persona creation
- [ ] Document version tracking
- [ ] Analytics and usage metrics

## Support

For issues or questions:
1. Check the logs: `rag_api.log` and `rag_ui.log`
2. Verify environment configuration
3. Check API health: `curl http://localhost:6603/api/health`
4. Review OpenAPI docs: http://localhost:6603/api/docs

---

**Built with**: Python, FastAPI, ChromaDB, Azure OpenAI, React (HTML/JS)
**Author**: Claude Code
**Date**: 2025-10-10

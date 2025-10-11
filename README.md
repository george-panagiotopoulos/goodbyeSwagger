# Documentation-First Architecture - Complete Implementation

A comprehensive example application showcasing a **documentation-first architectural pattern** with integrated RAG-based knowledge systems. This project demonstrates how rich documentation artifacts serve as both human-readable guides and machine-readable knowledge sources for AI-assisted development.

[![System Architecture](https://img.shields.io/badge/Architecture-Documentation--First-blue.svg)]()
[![Tech Stack](https://img.shields.io/badge/Stack-Rust%20%7C%20Python%20%7C%20React-orange.svg)]()
[![AI Ready](https://img.shields.io/badge/AI-RAG%20Enabled-green.svg)]()

---

## 🏗️ Project Overview

This repository contains two integrated systems:

1. **Accounts Processing System** - A production-grade banking application (MVP)
2. **RAG Documentation Assistant** - An AI-powered knowledge system with 8 specialized personas (including a fun kid who explains everything using superheroes and toys!)

Both systems demonstrate how comprehensive documentation enables:
- Natural language understanding of applications
- AI-assisted development workflows
- Multi-stakeholder knowledge access (developers, users, AI tools)
- Always up-to-date documentation reflecting actual implementation

---

## 📊 Quick Stats

| Component | Technology | Lines of Code | Status |
|-----------|------------|---------------|--------|
| **Accounts API** | Rust (Actix-web) | 3,200+ | ✅ Complete |
| **Business Logic** | Rust | 2,800+ | ✅ Complete |
| **Database** | SQLite + Python | 500+ | ✅ Complete |
| **UI** | React + TypeScript | 4,500+ | ✅ Complete |
| **RAG Backend** | Python + FastAPI | 2,400+ | ✅ Complete |
| **RAG Frontend** | HTML + JavaScript | 800+ | ✅ Complete |
| **Documentation** | Markdown + OpenAPI | 8,000+ | ✅ Complete |
| **Total** | Multi-language | **22,200+** | **100%** |

---

## 🚀 Quick Start

### Prerequisites

- **Rust** 1.70+ (with Cargo)
- **Python** 3.11+ (with pip)
- **Node.js** 18+ (with npm)
- **SQLite** 3.x
- **Azure OpenAI** account (for RAG system)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd goodbyeSwagger
   ```

2. **Configure Azure OpenAI credentials** (for RAG):
   ```bash
   cp RAG/backend/.env.example RAG/backend/.env
   # Edit RAG/backend/.env with your Azure OpenAI credentials
   ```

3. **Start the complete system:**
   ```bash
   ./start-all.sh
   ```

   This single command starts:
   - Accounts API (port 6600)
   - Accounts UI (port 6601)
   - RAG API (port 6603)
   - RAG Chat UI (port 6604)

4. **Access the applications:**
   - **Accounts UI**: http://localhost:6601
   - **Accounts API Docs**: http://localhost:6600/swagger-ui/
   - **RAG Chat UI**: http://localhost:6604
   - **RAG API Docs**: http://localhost:6603/api/docs

5. **Stop everything:**
   ```bash
   ./stop-all.sh
   ```

---

## 💼 Part 1: How the Accounts Application Works

The Accounts Processing System is a production-grade MVP for managing checking/current accounts with full banking operations.

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    React UI (Port 6601)                      │
│              Products • Customers • Accounts                 │
│           Transactions • Ledger • Batch Processing           │
└────────────────────────────┬────────────────────────────────┘
                             │ HTTP REST API
                             ↓
┌─────────────────────────────────────────────────────────────┐
│                  REST API (Port 6600)                        │
│                    Rust/Actix-web                            │
│  18 Endpoints • JWT Auth • OpenAPI Docs • CORS              │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ↓
┌─────────────────────────────────────────────────────────────┐
│              Business Logic Layer (Rust)                     │
│  Domain Models • Repositories • Services • Validation       │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ↓
┌─────────────────────────────────────────────────────────────┐
│                    Database (SQLite)                         │
│  6 Tables • Triggers • Views • Migrations • Seed Data       │
└─────────────────────────────────────────────────────────────┘
```

### Key Features

#### 1. Product Configuration
- Define account products with customizable parameters
- Interest rates, fees, overdraft limits
- Minimum balance requirements
- Currency settings

#### 2. Customer Management
- Individual and corporate customer types
- External customer ID integration
- Account ownership tracking

#### 3. Account Management
- Create accounts linked to products and customers
- Account statuses: Active, Closed
- Opening balance initialization
- Running balance tracking

#### 4. Transaction Processing
- **Credit (Deposit)**: Add funds to accounts
- **Debit (Withdrawal)**: Remove funds from accounts
- Transaction fees automatically applied
- Real-time balance updates
- Complete audit trail

#### 5. Monthly Interest Accrual
- **Convention**: 30/360 (every month = 30 days, year = 360 days)
- **Formula**: Monthly Interest = (Balance × Annual Rate) / 12
- Automatic calculation on month-end
- Minimum balance requirements enforced
- Interest posted as transactions
- Web UI batch trigger

#### 6. Complete Ledger
- All transactions chronologically ordered
- Running balance after each transaction
- Transaction categories: Opening, Credit, Debit, Interest, Fee
- Full audit trail with timestamps

### Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Database** | SQLite 3 | Data persistence |
| **DB Scripts** | Python 3.11 | Migrations, seeding, batch processing |
| **Business Logic** | Rust 1.70 | Domain models, repositories, services |
| **API** | Rust (Actix-web 4.x) | RESTful API with JWT auth |
| **UI** | React 18 + TypeScript | Modern web interface |
| **Build Tools** | Cargo, Vite, npm | Build automation |

### Sample Data

- **6 Products**: Standard Checking, Savings, Premium Checking, etc.
- **5 Customers**: Mix of individual and corporate
- **6 Accounts**: Total balance $22,500.50
- **229+ Transactions**: Realistic banking operations

### API Endpoints (18 Total)

**Products:** List all, list active, get by ID, create

**Customers:** List all, get by ID, create

**Accounts:** List all, get by ID, create, get transactions, credit, debit

**Batch:** Monthly accruals, accrual history

**Utility:** Health check

**📖 Full API documentation:** http://localhost:6600/swagger-ui/

---

## 🤖 Part 2: How the RAG System Works

The RAG (Retrieval-Augmented Generation) Documentation Assistant provides AI-powered knowledge access through specialized personas.

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                  Web UI (Port 6604)                          │
│          Persona Selection • Chat Interface                  │
└────────────────────────────┬────────────────────────────────┘
                             │ HTTP REST API
                             ↓
┌─────────────────────────────────────────────────────────────┐
│              FastAPI Backend (Port 6603)                     │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   Persona   │  │ Chat Service │  │Vector Store  │       │
│  │   Manager   │→ │  (RAG Logic) │→ │  (ChromaDB)  │       │
│  └─────────────┘  └──────────────┘  └──────────────┘       │
└────────────────────────┬─────────────────┬──────────────────┘
                         │                  │
                         ↓                  ↓
           ┌─────────────────────┐  ┌──────────────┐
           │   Azure OpenAI       │  │  ChromaDB    │
           │ Chat + Embeddings    │  │ Vector Store │
           └─────────────────────┘  └──────────────┘
```

### 8 Specialized AI Personas

| Persona | Avatar | Role | Use For |
|---------|--------|------|---------|
| **Dev Assistant** | 👨‍💻 | Software Developer | Setup, coding, debugging |
| **Ops Assistant** | 🔧 | DevOps Engineer | Deployment, infrastructure |
| **Business Expert** | 💼 | Business Analyst | Features, use cases, workflows |
| **API Guide** | 🔌 | External Developer | API integration help |
| **Architecture Advisor** | 🏛️ | System Architect | Design decisions, patterns |
| **Data Expert** | 🗄️ | Database Admin | Schema, queries, migrations |
| **Universal Helper** | 🤖 | General Assistant | General questions |
| **Kid Explainer** | 🎮 | Fun Teacher | Explains using toys/cartoons/superheroes! |

### 8 Knowledge Vector Collections

Documentation organized into specialized collections:
- **architecture_knowledge** - System design, ADRs
- **api_knowledge** - OpenAPI specs, endpoints
- **business_knowledge** - Requirements, use cases
- **developer_knowledge** - Setup, coding standards
- **devops_knowledge** - Deployment, operations
- **data_knowledge** - Schema, migrations
- **code_examples_knowledge** - Code samples
- **domain_knowledge** - Business rules

### Using the RAG System

**1. Ingest Documentation:**
```bash
cd RAG
source backend/.venv/bin/activate
python3 scripts/ingest_documents.py
```

**Available RAG Scripts:**
- `ingest_documents.py` - Main ingestion script for all documentation
- `ingest_demoflow.py` - Ingest API flow demonstration examples
- `ingest_demoflow_quick.py` - Quick ingestion using document loader
- `add_demoflow_direct.py` - Direct demoflow document addition to vector DB
- `test_rag_query.py` - Test RAG queries with different personas
- `test_rag_query_debug.py` - Debug RAG API responses
- `test_rag_curl.py` - Validate curl commands from RAG responses

**2. Access Chat UI:**
```
http://localhost:6604
```

**3. Ask Questions:**

**Dev Assistant:** "How do I add a new API endpoint?"

**Ops Assistant:** "How do I run the monthly interest batch?"

**Business Expert:** "How does interest calculation work?"

**Kid Explainer:** "Explain the database like I'm 10 years old!" (Get ready for superhero comparisons! 🦸‍♂️)

---

## 🛠️ Part 3: Using This Codebase for AI-Assisted Development

This project is designed to work seamlessly with **Claude Code**, **GitHub Copilot**, **Cursor**, and other "vibe coding" tools.

### Why This Codebase is AI-Ready

1. **Comprehensive Documentation** - 8,000+ lines of structured markdown
2. **OpenAPI Specifications** - Complete API contracts
3. **Type Safety** - TypeScript types, Rust types, API vocabulary
4. **Clear Structure** - Consistent organization across all layers
5. **Code Examples** - Postman collections, curl scripts, sample workflows

### Setting Up with Claude Code

**1. Clone and Open:**
```bash
git clone <your-repo-url>
cd goodbyeSwagger
code .  # Or your preferred editor
```

**2. Project Configuration:**

The project includes `CLAUDE.md` and `claude.md` files:
- `/claude.md` - Project overview and philosophy
- `/Accounts/CLAUDE.md` - Accounts application details

**3. Start the System:**
```bash
./start-all.sh
```

### Understanding the System with AI

**Ask Claude Code to explain:**
```
"Explain how the transaction processing flow works"
"Show me the data model for accounts"
"What's the API contract for creating a new account?"
"How does the monthly interest accrual work?"
```

**Navigate the codebase:**
```
"Find all API endpoints related to transactions"
"Show me the Rust domain model for Account"
"Where is the database schema defined?"
```

### Building New Modules with AI

#### Example 1: Adding a Lending Module

**1. Use the RAG System:**
```
Ask Dev Assistant: "How would I add a lending module for loans?"
```

**2. Follow the Pattern:**
```
1. Database: Create schema/migrations/004_add_lending.sql
2. Business Logic: Create domain models in Application/src/domain/loan.rs
3. API: Create handlers in API/src/handlers/loan_handlers.rs
4. UI: Create pages in UI/src/pages/Loans.tsx
5. Documentation: Update openapi.yaml
```

**3. Use Claude Code to Generate:**
```
"Generate the database schema for a lending module"
"Create the Rust domain model for a Loan entity"
"Write the API handler for creating a new loan"
"Generate the React component for loans"
```

#### Example 2: Adding a Reporting Service

**1. Design Architecture:**
```
Ask Architecture Advisor: "How should I structure a reporting service?"
```

**2. Implementation Strategy:**
```
Reporting Module:
├── Database/views/          # SQL views for reports
├── Application/services/    # Report generation logic
├── API/handlers/            # Report endpoints
└── UI/pages/Reports.tsx     # Report interface
```

**3. Generate with AI:**
```
"Create a SQL view for account balance summary"
"Write a function that generates a monthly statement"
"Create an API endpoint that exports transactions as CSV"
"Build a React component for report generation"
```

### Best Practices for AI-Assisted Development

**1. Start with Documentation:**
- Read `/Accounts/docs/` for understanding
- Check `internal_docs/dev_guidelines/DEVELOPER_GUIDE.md`
- Review OpenAPI specs before modifying APIs

**2. Follow Existing Patterns:**
- Use existing domain models as templates
- Follow error handling patterns
- Maintain consistent naming conventions

**3. Leverage the RAG System:**
- Use it to understand unfamiliar parts
- Ask for examples from the codebase
- Get explanations of business logic

**4. Test Incrementally:**
```bash
cd Accounts/Application
cargo test

cd ../API
./test_curl.sh
```

**5. Update Documentation:**
- Add endpoints to `openapi.yaml`
- Update API vocabulary
- Re-ingest for RAG: `python3 scripts/ingest_documents.py`

### Example AI-Assisted Workflow

**Task: Add overdraft limit checking**

1. **Understand:** Ask Dev Assistant about current validation
2. **Design:** Ask Architecture Advisor about implementation approach
3. **Generate:** "Update debit_account handler to check overdraft limits"
4. **Test:** "Write tests for overdraft scenarios"
5. **Document:** "Add overdraft documentation to API vocabulary"

### Extending the RAG System

**Add New Personas:** Edit `RAG/backend/src/models/persona.py`

**Add New Collections:** Create docs category, update mappings, re-ingest

### Resources

**Documentation:**
- `/Accounts/docs/api/openapi.yaml` - API reference
- `/Accounts/docs/api/API_VOCABULARY.md` - Data models
- `/Accounts/docs/user_guides/GETTING_STARTED.md` - Quick start
- `/Accounts/internal_docs/` - Development guides

**Examples:**
- `/Accounts/docs/examples/postman_collection.json` - 25+ examples
- `/Accounts/API/test_curl.sh` - curl scripts
- `/DevLog/` - Implementation history

**Tools:**
- Swagger UI: http://localhost:6600/swagger-ui/
- RAG Chat: http://localhost:6604
- API Docs: http://localhost:6603/api/docs

---

## 📚 Documentation Structure

### External (`/Accounts/docs/`)
For users and API consumers:
- API specifications (OpenAPI/Swagger)
- API vocabulary (data models)
- User guides
- Code examples (Postman)

### Internal (`/Accounts/internal_docs/`)
For development team:
- Project state
- 12-month roadmap
- Developer guidelines
- Technical specs

### Development Log (`/DevLog/`)
Historical records:
- Implementation tasks
- MVP planning
- Functional requirements
- Completion summaries

---

## 🎯 Key Features

### Accounts Application
✅ Product configuration ✅ Customer management ✅ Account management
✅ Transaction processing ✅ Complete ledger ✅ Monthly interest accrual
✅ Batch processing ✅ JWT authentication ✅ RESTful API (18 endpoints)
✅ OpenAPI docs ✅ React UI ✅ Data integrity

### RAG System
✅ 8 AI personas ✅ 8 knowledge vectors ✅ Azure OpenAI
✅ Semantic search ✅ Context-aware responses ✅ Source citation
✅ Web chat interface ✅ Document ingestion ✅ Multi-collection retrieval
✅ Kid-friendly explanations with superhero comparisons! 🎮

---

## 🗂️ Project Organization

```
goodbyeSwagger/
├── Accounts/              # Banking application
│   ├── API/               # Rust REST API (6600)
│   ├── Application/       # Rust business logic
│   ├── Database/          # SQLite + Python
│   ├── UI/                # React frontend (6601)
│   ├── docs/              # External docs
│   ├── internal_docs/     # Internal docs
│   ├── start.sh           # Start Accounts
│   └── stop.sh            # Stop Accounts
│
├── RAG/                   # Documentation assistant
│   ├── backend/           # FastAPI (6603)
│   ├── frontend/          # Chat UI (6604)
│   ├── scripts/           # Ingestion & testing utilities
│   ├── start_rag.sh       # Start RAG
│   └── stop_rag.sh        # Stop RAG
│
├── DevLog/                # Dev history
├── start-all.sh           # Start everything
├── stop-all.sh            # Stop everything
├── README.md              # This file
└── claude.md              # AI overview
```

---

## 🔧 Development Scripts

```bash
./start-all.sh          # Start complete system
./stop-all.sh           # Stop everything

cd Accounts
./start.sh              # Accounts only

cd RAG
./start_rag.sh          # RAG only
```

---

## 🎨 System Ports

| Service | Port | Purpose |
|---------|------|---------|
| Accounts API | 6600 | REST API |
| Accounts UI | 6601 | Web interface |
| RAG API | 6603 | RAG REST API |
| RAG UI | 6604 | Chat interface |

---

## 🚦 Quality Standards

Production-grade MVP with:
- ✅ Complete error handling
- ✅ Data integrity validation
- ✅ Comprehensive testing
- ✅ Full documentation
- ✅ Type safety
- ✅ Security best practices

---

## 📈 Roadmap

**Phase 2**: Advanced Transactions (authorization, clearing, overdraft, transfers)
**Phase 3**: Enhanced Interest & Fees (formulas, dynamic config)
**Phase 4**: Multi-Currency
**Phase 5+**: Reporting, Account Lifecycle, Advanced Features

See `/Accounts/internal_docs/roadmap/ROADMAP.md` for complete 12-month plan.

---

## 🤝 Contributing

To extend this showcase project:

1. Study the existing structure (use RAG system)
2. Follow the layered architecture
3. Document as you build
4. Test thoroughly
5. Update the RAG system

---

## 📝 License

Demonstration project showcasing architectural patterns. Adapt as needed.

---

## 🙏 Built With

**Rust** • **React** • **Python** • **FastAPI** • **Azure OpenAI** • **ChromaDB** • **SQLite** • **Claude Code**

---

**Built to demonstrate documentation-first architecture and AI-assisted development.**

**Version**: 1.0.0 | **Date**: 2025-10-10 | **Status**: ✅ MVP Complete

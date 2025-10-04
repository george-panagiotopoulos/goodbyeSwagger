# Documentation-First Architecture Showcase Project

## Project Overview

This project demonstrates a documentation-first architectural pattern for building applications with comprehensive RAG-based knowledge systems. The goal is to create a complete example application with rich documentation artifacts that serve as both human-readable documentation and machine-readable knowledge sources for AI-assisted development.

## Core Philosophy

Rather than documenting after development, this project follows a **360-degree documentation approach** where diverse documentation artifacts are created alongside the application and then used to build a RAG (Retrieval-Augmented Generation) system that enables:

- **Natural language understanding** of the application through a chatbot interface
- **AI-assisted development** via Claude Code and similar tools
- **Unified knowledge interface** for all stakeholders (developers, product managers, users, etc.)
- **Always up-to-date documentation** that reflects actual implementation

## Project Components

### 1. Sample Application (Core System)

A fully functional application demonstrating the pattern, consisting of:

#### Database Layer
- **Technology**: SQLite with Python
- **Port**: 6602
- **Purpose**: Lightweight, file-based relational database
- **Content**: Sample schema with realistic business entities and relationships

#### Business Logic Layer
- **Technology**: Rust
- **Purpose**: Core business operations, validation, and data processing
- **Integration**: Direct database access and API layer support

#### API Layer
- **Technology**: Rust (RESTful with HATEOAS)
- **Port**: 6600
- **Features**:
  - RESTful endpoints following HATEOAS principles
  - Authentication and authorization services
  - Comprehensive error handling
  - Request/response validation
  - API versioning support

#### User Interface
- **Technology**: React
- **Port**: 6601
- **Features**:
  - Modern, responsive UI
  - Integration with API layer
  - User authentication flows
  - Sample business workflows

### 2. Documentation Artifacts (Knowledge Base)

Following the 9-category RAG input model from the architectural pattern:

#### Category 1: Code & Execution 💻
- Implementation scripts for common workflows
- Execution logs and sample outputs
- Integration examples
- Test execution results

#### Category 2: Strategic Documentation 📚
- Architecture decision records (ADRs)
- Design specifications
- Technical guides
- System overview documents

#### Category 3: Business Documents 💼
- Marketing brochure
- Business value propositions
- Benefits and ROI documentation
- User personas
- Use case descriptions

#### Category 4: DevOps & Infrastructure 🚀
- `start.sh` - Starts all application components
- `stop.sh` - Stops all running components
- Deployment instructions
- Environment configuration guides
- Health check and monitoring setup

#### Category 5: System Architecture Diagrams 🏛️
- Component diagrams (Mermaid/PlantUML)
- Class diagrams for business logic
- Sequence diagrams for key workflows
- Data flow diagrams
- Deployment architecture

#### Category 6: Domain Mapping 🌐
- Business domain vocabulary
- Domain model documentation
- Cross-reference to industry standards (if applicable)
- Bounded context definitions

#### Category 7: API Specifications 🔌
- OpenAPI/Swagger specifications for all endpoints
- Authentication flow documentation
- Error code reference
- Rate limiting and throttling policies
- API versioning strategy

#### Category 8: Live API Examples 📋
- Postman/Thunder Client collections
- Sample request/response payloads
- Integration test scenarios
- cURL command examples
- SDK usage examples

#### Category 9: Data Models 🗄️
- Entity-relationship diagrams
- Logical data model documentation
- Database schema documentation
- API data model specifications
- **API Vocabulary**: Comprehensive JSON vocabulary defining all API entities, fields, and relationships
- Field-level documentation with types, constraints, and business rules

### 3. RAG System (Knowledge Interface)

#### Vector Database
- **Technology**: ChromaDB with OpenAI embeddings
- **Content**: All documentation artifacts from categories 1-9
- **Purpose**: Semantic search and context retrieval

#### RAG API
- **Port**: 6603
- **Features**:
  - Query endpoint for natural language questions
  - Context retrieval from vector database
  - LLM integration for answer generation
  - Response formatting and citation

#### Chatbot Interface
- **Port**: 6604
- **Features**:
  - Interactive Q&A about the application
  - Context-aware responses
  - Code example generation
  - Documentation navigation
  - Diagram visualization

#### Claude Code Integration
- **Purpose**: Enable AI-assisted development using the knowledge base
- **Features**:
  - Project structure that Claude Code can understand
  - Rich context for code generation
  - Documentation-driven development workflow
  - Automated code generation from specs

## Technology Stack Summary

| Component | Technology | Port | Purpose |
|-----------|------------|------|---------|
| Database | SQLite + Python | 6602 | Data persistence |
| Business Logic | Rust | - | Core operations |
| API | Rust (REST + HATEOAS) | 6600 | External interface |
| UI | React | 6601 | User interface |
| RAG API | Python | 6603 | Knowledge queries |
| Chatbot UI | React/Python | 6604 | Interactive assistant |

## Port Range

All services use ports in the **6600-6699** range:
- **6600**: REST API
- **6601**: React UI
- **6602**: SQLite Database (if exposed)
- **6603**: RAG API
- **6604**: Chatbot UI

## Project Structure

```
goodbyeSwagger/
├── About/                          # Original architecture docs (DO NOT MODIFY)
├── claude.md                       # This file - project overview
├── Implementation_tasks.md         # Detailed task breakdown
├── Implementation_progress.md      # Progress tracking
├── start.sh                       # Start all components
├── stop.sh                        # Stop all components
│
├── app/                           # Core application
│   ├── database/                  # SQLite + Python
│   ├── business_logic/            # Rust core logic
│   ├── api/                       # Rust REST API
│   └── ui/                        # React frontend
│
├── docs/                          # Documentation artifacts
│   ├── architecture/              # Category 5: Architecture diagrams
│   ├── api/                       # Category 7: API specs
│   ├── data_models/               # Category 9: Data models
│   ├── business/                  # Category 3: Business docs
│   ├── guides/                    # Category 2: Strategic docs
│   ├── examples/                  # Category 8: Live examples
│   ├── devops/                    # Category 4: DevOps
│   ├── domain/                    # Category 6: Domain mapping
│   └── execution/                 # Category 1: Code & execution
│
├── rag/                           # RAG system
│   ├── embeddings/                # Vector database
│   ├── api/                       # RAG API service
│   └── chatbot/                   # Chatbot interface
│
└── utils/                         # Utility scripts
    ├── refresh_embeddings.py      # Update vector DB
    └── validate_docs.py           # Check documentation completeness
```

## Development Workflow

### Phase 1: Application Development
1. Design database schema
2. Implement business logic in Rust
3. Build REST API with authentication
4. Create React UI
5. Integrate components
6. Write start/stop scripts

### Phase 2: Documentation Creation
1. Generate API specifications (Swagger/OpenAPI)
2. Create data model documentation and API vocabulary
3. Write architecture diagrams
4. Develop business user guides
5. Create marketing materials
6. Build example collections
7. Document deployment processes

### Phase 3: RAG System Implementation
1. Set up ChromaDB vector database
2. Implement embedding generation for all docs
3. Build RAG API service
4. Create chatbot interface
5. Integrate with Claude Code workflow
6. Test and refine retrieval quality

## Success Criteria

- ✅ Fully functional application with all components working together
- ✅ Comprehensive documentation covering all 9 input categories
- ✅ Working RAG system that can answer questions about the application
- ✅ Chatbot that provides accurate, context-aware responses
- ✅ Claude Code integration enables AI-assisted development
- ✅ All documentation artifacts are machine-readable and human-friendly
- ✅ Start/stop scripts manage entire system lifecycle
- ✅ Authentication and authorization fully implemented
- ✅ HATEOAS principles properly applied in API design

## Key Differentiators

This project showcases:

1. **Documentation as a First-Class Citizen**: Not an afterthought, but integral to development
2. **Multi-Stakeholder Perspective**: Documentation serves developers, users, product managers, and AI tools
3. **Machine-Readable Knowledge**: Documentation structured for both humans and AI consumption
4. **Living Documentation**: RAG system keeps knowledge accessible and queryable
5. **AI-Assisted Development**: Claude Code can use the knowledge base for code generation
6. **Complete 360° View**: All aspects of the application documented from multiple perspectives

## Notes

- The `/About` folder contains the reference architecture and must NOT be modified during development
- The `/About` folder will be deleted at project completion and replaced with project-specific documentation
- All references to "Temenos", "Modular Banking", or banking-specific terminology should be replaced with generic application concepts
- This is a demonstration/showcase project, not a production banking system
- Focus is on the **documentation pattern and RAG architecture**, not the specific business domain

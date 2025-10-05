# System Architecture
## Account Processing System

**Version**: 1.0
**Last Updated**: October 2025

---

## Overview

The Account Processing System follows a layered architecture pattern with clear separation of concerns across four primary layers: UI, API, Business Logic, and Data.

### Source Code Ownership Model

**Complete Technology Transfer**: Unlike proprietary banking solutions, the Account Processing System is delivered with **full source code access**. Financial institutions receive:

- **All source code** for UI, API, Business Logic, and Database layers
- **Build and deployment scripts** for complete operational control
- **Architecture documentation** enabling independent development
- **No licensing restrictions** on modifications or extensions
- **Freedom to evolve** the platform according to institutional needs

This open-access model eliminates vendor lock-in while providing enterprise-grade functionality, allowing banks to develop freely on top of the platform without restrictions or risks associated with proprietary systems.

**AI-Assisted Development Era**: In 2025 and beyond, source code access provides exponential value through AI coding assistants (GitHub Copilot, Claude Code, ChatGPT). These tools can:
- Analyze and understand the complete codebase instantly
- Generate custom features and enhancements in hours instead of months
- Reduce development costs by 60-80% compared to vendor-led customizations
- Enable rapid prototyping and innovation cycles
- Provide automated documentation and testing assistance

Unlike proprietary systems where AI tools are locked out, clients can leverage cutting-edge AI development tools to accelerate their customization roadmap dramatically.

---

## High-Level Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        WEB[Web Browser]
        MOBILE[Mobile App - Future]
        API_CLIENT[Third-Party API Clients]
    end

    subgraph "Presentation Layer - Port 6601"
        UI[React UI<br/>TypeScript + Vite]
    end

    subgraph "API Layer - Port 6600"
        REST[REST API<br/>Rust + Actix-web]
        AUTH[Authentication Service<br/>JWT + bcrypt]
        CORS[CORS Handler]
        LOGGING[Request Logging]
    end

    subgraph "Business Logic Layer"
        MODELS[Domain Models<br/>Account, Product, Customer]
        SERVICES[Business Services<br/>Interest, Fees, Validation]
        REPOS[Repositories<br/>Data Access Layer]
    end

    subgraph "Data Layer"
        DB[(SQLite Database<br/>Migrations + Seeds)]
    end

    WEB --> UI
    MOBILE -.-> UI
    API_CLIENT --> REST
    UI --> REST
    REST --> AUTH
    REST --> CORS
    REST --> LOGGING
    REST --> MODELS
    MODELS --> SERVICES
    SERVICES --> REPOS
    REPOS --> DB

    style UI fill:#61dafb
    style REST fill:#ff6b6b
    style MODELS fill:#ffd93d
    style DB fill:#6bcf7f
```

---

## Component Architecture

```mermaid
graph LR
    subgraph "Frontend Components"
        ROUTES[React Router]
        PAGES[Pages Layer]
        COMPONENTS[Reusable Components]
        API_CLIENT[API Client Service]
    end

    subgraph "API Components"
        HANDLERS[Request Handlers]
        MIDDLEWARE[Middleware Stack]
        VALIDATORS[Request Validators]
    end

    subgraph "Business Components"
        DOMAIN[Domain Layer]
        OPERATIONS[Operations Layer]
        DATA[Data Access Layer]
    end

    ROUTES --> PAGES
    PAGES --> COMPONENTS
    PAGES --> API_CLIENT
    API_CLIENT --> HANDLERS
    HANDLERS --> MIDDLEWARE
    HANDLERS --> VALIDATORS
    HANDLERS --> DOMAIN
    DOMAIN --> OPERATIONS
    OPERATIONS --> DATA
```

---

## Data Flow Architecture

```mermaid
sequenceDiagram
    participant User
    participant UI as React UI<br/>(Port 6601)
    participant API as REST API<br/>(Port 6600)
    participant Auth as Auth Service
    participant BL as Business Logic
    participant DB as Database

    User->>UI: Interact with UI
    UI->>API: HTTP Request
    API->>Auth: Validate JWT
    Auth-->>API: Token Valid
    API->>BL: Execute Business Logic
    BL->>DB: Query/Update Data
    DB-->>BL: Data Result
    BL-->>API: Business Result
    API-->>UI: JSON Response
    UI-->>User: Updated UI
```

---

## Deployment Architecture

```mermaid
graph TB
    subgraph "Production Environment"
        subgraph "Web Tier"
            LB[Load Balancer<br/>nginx/HAProxy]
            UI1[React UI Instance 1]
            UI2[React UI Instance 2]
        end

        subgraph "Application Tier"
            API1[API Instance 1<br/>Port 6600]
            API2[API Instance 2<br/>Port 6600]
            API3[API Instance 3<br/>Port 6600]
        end

        subgraph "Data Tier"
            DB_PRIMARY[(PostgreSQL Primary)]
            DB_REPLICA[(PostgreSQL Replica)]
        end

        subgraph "Monitoring"
            PROMETHEUS[Prometheus]
            GRAFANA[Grafana]
            LOGS[Centralized Logging]
        end
    end

    LB --> UI1
    LB --> UI2
    UI1 --> API1
    UI1 --> API2
    UI2 --> API2
    UI2 --> API3
    API1 --> DB_PRIMARY
    API2 --> DB_PRIMARY
    API3 --> DB_PRIMARY
    DB_PRIMARY --> DB_REPLICA

    API1 -.-> PROMETHEUS
    API2 -.-> PROMETHEUS
    API3 -.-> PROMETHEUS
    PROMETHEUS --> GRAFANA
    API1 -.-> LOGS
    API2 -.-> LOGS
    API3 -.-> LOGS
```

---

## Security Architecture

```mermaid
graph TB
    subgraph "Security Layers"
        subgraph "Authentication"
            LOGIN[Login Endpoint]
            JWT[JWT Token Generation]
            BCRYPT[Password Hashing - bcrypt]
        end

        subgraph "Authorization"
            MIDDLEWARE[Auth Middleware]
            RBAC[Role-Based Access - Future]
            PERMISSIONS[Permission Checks]
        end

        subgraph "Data Security"
            VALIDATION[Input Validation]
            SANITIZATION[SQL Injection Prevention]
            ENCRYPTION[Data Encryption at Rest - Future]
        end

        subgraph "Network Security"
            HTTPS[HTTPS/TLS]
            CORS_POLICY[CORS Policy]
            RATE_LIMIT[Rate Limiting - Future]
        end
    end

    LOGIN --> JWT
    LOGIN --> BCRYPT
    JWT --> MIDDLEWARE
    MIDDLEWARE --> RBAC
    MIDDLEWARE --> PERMISSIONS
    PERMISSIONS --> VALIDATION
    VALIDATION --> SANITIZATION
    SANITIZATION --> ENCRYPTION
```

---

## Technology Stack

### Frontend
- **Framework**: React 18
- **Language**: TypeScript
- **Build Tool**: Vite
- **Routing**: React Router DOM
- **HTTP Client**: Fetch API
- **Port**: 6601

### Backend API
- **Language**: Rust
- **Framework**: Actix-web
- **Authentication**: JWT (jsonwebtoken crate)
- **Password Hashing**: bcrypt
- **Serialization**: serde + serde_json
- **Port**: 6600

### Business Logic
- **Language**: Rust
- **Pattern**: Repository Pattern
- **Domain Models**: Strong typing with Rust structs
- **Validation**: Custom validators

### Database
- **Development**: SQLite
- **Production**: PostgreSQL (recommended)
- **Migration Tool**: Custom SQL scripts
- **ORM**: rusqlite (development)

---

## API Architecture

### Endpoint Structure

```
/api
├── /health                    # Health check
├── /auth
│   └── /login                # Authentication
├── /products
│   ├── GET    /              # List all products
│   ├── POST   /              # Create product
│   ├── GET    /{id}          # Get product
│   └── PUT    /{id}          # Update product
├── /customers
│   ├── GET    /              # List all customers
│   ├── POST   /              # Create customer
│   └── GET    /{id}          # Get customer
├── /accounts
│   ├── GET    /              # List all accounts
│   ├── POST   /              # Create account
│   └── GET    /{id}          # Get account
├── /transactions
│   ├── POST   /credit        # Credit transaction
│   ├── POST   /debit         # Debit transaction
│   └── GET    /ledger/{id}   # Get ledger
└── /batch
    ├── POST   /interest      # Calculate interest
    └── POST   /fees          # Apply fees
```

### Response Format

All API responses follow this structure:

```json
{
  "success": true,
  "data": { ... },
  "message": "Operation successful",
  "timestamp": "2025-10-05T12:00:00Z"
}
```

Error responses:

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input provided",
    "details": { ... }
  },
  "timestamp": "2025-10-05T12:00:00Z"
}
```

---

## Data Model Architecture

```mermaid
erDiagram
    PRODUCT ||--o{ ACCOUNT : "defines"
    CUSTOMER ||--o{ ACCOUNT : "owns"
    ACCOUNT ||--o{ TRANSACTION : "records"

    PRODUCT {
        string product_id PK
        string product_name
        string product_type
        decimal interest_rate
        decimal transaction_fee
        decimal monthly_fee
        decimal min_balance_for_interest
        timestamp created_at
    }

    CUSTOMER {
        string customer_id PK
        string first_name
        string last_name
        string email
        string phone
        timestamp created_at
    }

    ACCOUNT {
        string account_id PK
        string customer_id FK
        string product_id FK
        string status
        decimal balance
        date opening_date
        date closing_date
        timestamp created_at
        timestamp updated_at
    }

    TRANSACTION {
        string transaction_id PK
        string account_id FK
        string transaction_type
        decimal amount
        decimal balance_after
        string reference
        timestamp transaction_date
    }
```

---

## Integration Architecture

```mermaid
graph TB
    subgraph "Internal Systems"
        APS[Account Processing System]
    end

    subgraph "Future Integrations"
        CORE[Core Banking System]
        PAYMENT[Payment Gateway]
        KYC[KYC Service]
        FRAUD[Fraud Detection]
        REPORTING[Reporting Engine]
        NOTIFICATION[Notification Service]
    end

    subgraph "External Systems"
        BUREAU[Credit Bureau]
        BANK_NET[Banking Network]
        REGULATORY[Regulatory Reporting]
    end

    APS <-.-> CORE
    APS <-.-> PAYMENT
    APS <-.-> KYC
    APS <-.-> FRAUD
    APS <-.-> REPORTING
    APS <-.-> NOTIFICATION

    REPORTING -.-> REGULATORY
    PAYMENT -.-> BANK_NET
    KYC -.-> BUREAU

    style APS fill:#ff6b6b
    style CORE fill:#ffd93d
    style PAYMENT fill:#6bcf7f
```

---

## Scalability Architecture

```mermaid
graph TB
    subgraph "Horizontal Scaling"
        subgraph "UI Tier - Stateless"
            UI1[UI Instance 1]
            UI2[UI Instance 2]
            UI3[UI Instance N]
        end

        subgraph "API Tier - Stateless"
            API1[API Instance 1]
            API2[API Instance 2]
            API3[API Instance N]
        end

        subgraph "Data Tier - Stateful"
            DB_WRITE[(Write DB)]
            DB_READ1[(Read Replica 1)]
            DB_READ2[(Read Replica 2)]
        end
    end

    UI1 --> API1
    UI2 --> API2
    UI3 --> API3

    API1 --> DB_WRITE
    API2 --> DB_WRITE
    API3 --> DB_WRITE

    API1 --> DB_READ1
    API2 --> DB_READ2
    API3 --> DB_READ1

    DB_WRITE --> DB_READ1
    DB_WRITE --> DB_READ2
```

### Scaling Strategy

1. **UI Layer**: Add more instances behind load balancer
2. **API Layer**: Horizontal scaling with container orchestration (Kubernetes)
3. **Data Layer**: Read replicas for query performance, write master for consistency
4. **Caching**: Redis/Memcached for frequently accessed data (future)
5. **Message Queue**: Async processing for batch operations (future)

---

## Performance Characteristics

| Component | Metric | Current | Target |
|-----------|--------|---------|--------|
| UI Load Time | Initial render | < 2s | < 1s |
| API Response | Average latency | 45ms | < 100ms |
| API Response | P95 latency | 120ms | < 200ms |
| API Response | P99 latency | 280ms | < 500ms |
| Database | Query time | < 10ms | < 50ms |
| Throughput | Requests/sec | 500+ | 5000+ |
| Concurrent Users | Supported | 100+ | 1000+ |

---

## Monitoring & Observability

```mermaid
graph LR
    subgraph "Application"
        API[API Service]
        UI[UI Service]
    end

    subgraph "Metrics Collection"
        METRICS[Metrics Exporter]
        TRACES[Distributed Tracing]
        LOGS[Log Aggregator]
    end

    subgraph "Monitoring Stack"
        PROMETHEUS[Prometheus]
        JAEGER[Jaeger]
        ELK[ELK Stack]
    end

    subgraph "Visualization"
        GRAFANA[Grafana Dashboards]
        KIBANA[Kibana]
        ALERTS[Alert Manager]
    end

    API --> METRICS
    API --> TRACES
    API --> LOGS
    UI --> LOGS

    METRICS --> PROMETHEUS
    TRACES --> JAEGER
    LOGS --> ELK

    PROMETHEUS --> GRAFANA
    JAEGER --> GRAFANA
    ELK --> KIBANA
    PROMETHEUS --> ALERTS
```

---

## Disaster Recovery Architecture

```mermaid
graph TB
    subgraph "Primary Region"
        PRIMARY[Primary Deployment]
        PRIMARY_DB[(Primary Database)]
    end

    subgraph "Secondary Region"
        SECONDARY[Secondary Deployment - Standby]
        SECONDARY_DB[(Secondary Database - Replica)]
    end

    subgraph "Backup"
        S3[Object Storage<br/>Automated Backups]
    end

    PRIMARY --> PRIMARY_DB
    PRIMARY_DB -.Replication.-> SECONDARY_DB
    PRIMARY_DB -.Backup.-> S3
    SECONDARY_DB -.Backup.-> S3

    SECONDARY --> SECONDARY_DB
```

### Recovery Objectives

- **RTO (Recovery Time Objective)**: < 1 hour
- **RPO (Recovery Point Objective)**: < 15 minutes
- **Backup Frequency**: Every 6 hours
- **Backup Retention**: 30 days

---

## Development Architecture

```mermaid
graph TB
    subgraph "Developer Workstation"
        IDE[VS Code / IDE]
        LOCAL_UI[Local UI - Port 6601]
        LOCAL_API[Local API - Port 6600]
        LOCAL_DB[(Local SQLite)]
    end

    subgraph "Version Control"
        GIT[Git Repository]
        GITHUB[GitHub]
    end

    subgraph "CI/CD Pipeline"
        BUILD[Build & Test]
        QUALITY[Code Quality]
        SECURITY[Security Scan]
        DEPLOY[Deploy]
    end

    subgraph "Environments"
        DEV[Development]
        STAGING[Staging]
        PROD[Production]
    end

    IDE --> LOCAL_UI
    IDE --> LOCAL_API
    LOCAL_API --> LOCAL_DB

    IDE --> GIT
    GIT --> GITHUB
    GITHUB --> BUILD
    BUILD --> QUALITY
    QUALITY --> SECURITY
    SECURITY --> DEPLOY

    DEPLOY --> DEV
    DEPLOY --> STAGING
    DEPLOY --> PROD
```

---

## Future Architecture Enhancements

### Phase 2 (Q1 2026)
- Event-driven architecture with message queues
- Caching layer (Redis)
- API Gateway with rate limiting
- Advanced monitoring and tracing

### Phase 3 (Q2 2026)
- Microservices decomposition
- Service mesh (Istio/Linkerd)
- GraphQL API option
- Real-time notifications (WebSocket)

### Phase 4 (Q3-Q4 2026)
- Multi-tenancy support
- Advanced analytics platform
- Machine learning integration
- Mobile native SDKs

---

## Architecture Decision Records (ADRs)

Key architectural decisions are documented in separate ADR files:

1. **ADR-001**: Use of Rust for backend services
2. **ADR-002**: SQLite for development, PostgreSQL for production
3. **ADR-003**: JWT for authentication
4. **ADR-004**: Repository pattern for data access
5. **ADR-005**: React with TypeScript for UI

See `/docs/architecture/adr/` for detailed decision records.

---

**Document Owner**: David Kim, CTO
**Contributors**: Engineering Team
**Last Review**: October 2025
**Next Review**: January 2026

---

© 2025 Account Processing System | Internal Documentation

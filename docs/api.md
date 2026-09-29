# REST API Specification

FinAI Nexus exposes RESTful endpoints versioned under `/api/v1`. Interactive OpenAPI specs are available at `/docs` when running the application.

## Primary Endpoints

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| POST | `/api/v1/auth/login` | Authenticate user & issue JWT token | No |
| POST | `/api/v1/chat` | Execute Multi-Agent pricing intelligence workflow | Yes (VIEWER+) |
| POST | `/api/v1/documents/upload` | Upload & index pricing/interchange document | Yes (ANALYST+) |
| GET | `/api/v1/documents` | List indexed policy documents | Yes (VIEWER+) |
| DELETE | `/api/v1/documents/{id}` | Delete document and vector index | Yes (ANALYST+) |
| POST | `/api/v1/documents/search` | Test semantic vector search | Yes (VIEWER+) |
| POST | `/api/v1/analytics/query` | Execute read-only SQL data query | Yes (ANALYST+) |
| POST | `/api/v1/evaluations/run` | Trigger evaluation benchmark run | Yes (ANALYST+) |
| GET | `/api/v1/evaluations` | List historical evaluation scores | Yes (VIEWER+) |
| GET | `/api/v1/traces/{id}` | Inspect agent run execution trace | Yes (VIEWER+) |
| GET | `/api/v1/observability/metrics` | Retrieve dashboard observability metrics | Yes (VIEWER+) |
| GET | `/api/v1/agents` | List registered autonomous agents | Yes (VIEWER+) |
| GET | `/api/v1/audit-logs` | Retrieve enterprise security audit logs | Yes (ADMIN) |

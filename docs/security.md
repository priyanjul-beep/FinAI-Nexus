# Platform Security & Compliance

## Security Architecture

1. **Authentication & Authorization**
   - OAuth2 Password Bearer authentication with JWT access tokens.
   - SHA-256 password hashing.
   - Role-Based Access Control (RBAC):
     - `ADMIN`: Full access to system configuration, audit logs, and user management.
     - `ANALYST`: Query execution, document upload/deletion, analytics, and report generation.
     - `VIEWER`: Read-only access to dashboard and historical traces.

2. **Database Security**
   - Parameterized SQL execution preventing SQL injection.
   - Read-only SQL validator blocking DDL/DML statements.

3. **Audit Logging**
   - All security-relevant events (logins, document uploads, SQL queries, configuration changes) are recorded in `audit_logs`.

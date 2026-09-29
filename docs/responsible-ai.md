# Responsible AI & Safety Guardrails

## Safety Architecture

FinAI Nexus incorporates dedicated safety and validation layers to prevent hallucinations, unsafe SQL execution, prompt injection, and PII leakage.

## Guardrail Controls

1. **Prompt Injection Protection**
   - Regex and pattern matching for injection phrases (e.g., `ignore previous instructions`, `system prompt override`).
   - Requests flagged for injection are blocked before LLM invocation.

2. **PII Detection & Redaction**
   - Automatic redaction of SSNs, credit card numbers, and email addresses prior to sending context to LLMs.

3. **Read-Only SQL Validation**
   - AST / Keyword validator ensuring generated SQL queries start strictly with `SELECT` or `WITH`.
   - Rejects non-read operations (`DROP`, `DELETE`, `UPDATE`, `INSERT`, `ALTER`, `TRUNCATE`).
   - Enforces query row limits.

4. **Hallucination Detection & Citation Audit**
   - Responsible AI Agent verifies candidate outputs against retrieved vector chunks.
   - Assigns a hallucination risk score (threshold ≤ 0.25).
   - Downgrades confidence score to `MEDIUM` or `LOW` if citations are unverified.

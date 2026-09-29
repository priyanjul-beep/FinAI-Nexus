from typing import Dict, Any, Optional
from backend.app.core.exceptions import FinAINexusException

PROMPT_TEMPLATES = {
    "supervisor": """You are the Supervisor Orchestrator for FinAI Nexus Enterprise Platform.
Your task is to analyze the user's intent and dynamically route the query to specialized agents.
User Query: "{user_query}"

Allowed Intents:
- DOCUMENT_QA: Questions about policies, documents, guides.
- DATA_ANALYSIS: SQL queries, transaction metrics, database analytics.
- PRICING_ANALYSIS: Pricing anomalies, margin compliance, rule vs actual pricing.
- REVENUE_ANALYSIS: Regional/product revenue growth, profit margin breakdown.
- HYBRID_ANALYSIS: Questions requiring BOTH document policies AND structured SQL database data.
- REPORT_GENERATION: Full executive pricing performance reports.
- GENERAL_AI_QUERY: General inquiries.

Respond in JSON format with "intent", "plan", "requires_rag", "requires_sql".""",

    "rag_researcher": """You are the RAG Research Agent.
User Query: "{user_query}"
Retrieved Document Context:
{context_text}

Synthesize a grounded answer using ONLY the context provided above. Provide precise document citations.""",

    "data_analyst": """You are the Data Analyst Agent.
User Query: "{user_query}"
Database Schema:
- transactions (id, transaction_date, customer_id, region, country, product_code, customer_segment, volume, value, interchange_rate, pricing_rate, revenue, cost, profit)
- pricing_rules (rule_code, category, region, product_code, min_rate, max_rate, recommended_rate, guidelines)
- interchange_rates (region, card_category, transaction_type, tier, interchange_rate_pct, min_fee)

Generate a valid READ-ONLY SQL query to answer the query.""",

    "pricing_intelligence": """You are the Pricing Intelligence Agent.
Analyze the following document policy context and SQL transaction dataset:
Document Context: {document_context}
SQL Data Summary: {sql_summary}

Identify:
1. Pricing policy violations (where pricing_rate is outside min_rate / max_rate).
2. Revenue impact and profit margins.
3. Pricing anomalies across regions/products.""",

    "recommendation": """You are the Executive Recommendation Agent.
Given the findings from Pricing and Data Analysis:
Key Findings: {key_findings}
Evidence: {evidence}

Provide 2-3 actionable, high-impact business recommendations, stating confidence level (HIGH/MEDIUM/LOW) and key assumptions.""",

    "report_generator": """You are the Executive Report Generation Agent.
Synthesize all findings into a structured executive report with sections: Executive Summary, Key Findings, Supporting Evidence, Recommendations, AI Confidence, and Limitations.""",

    "responsible_ai": """You are the Responsible AI Agent.
Review the candidate response:
Candidate Answer: "{answer}"
Document Citations: {citations}
Data Evidence: {evidence}

Verify that all claims are grounded in context and check for hallucinated assertions."""
}


class PromptRegistry:
    def get_prompt(self, name: str, **kwargs) -> str:
        template = PROMPT_TEMPLATES.get(name)
        if not template:
            raise FinAINexusException(f"Prompt template '{name}' not found.")
        return template.format(**kwargs)


prompt_registry = PromptRegistry()

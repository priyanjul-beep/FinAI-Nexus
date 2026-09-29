import time
import json
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from backend.app.core.config import settings


class BaseLLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str, system_prompt: Optional[str] = None, json_mode: bool = False) -> Dict[str, Any]:
        """
        Returns: {
           "text": str,
           "prompt_tokens": int,
           "completion_tokens": int,
           "latency_ms": float,
           "provider": str,
           "model": str
        }
        """
        pass


class MockLLMProvider(BaseLLMProvider):
    """
    Intelligent context-aware Mock LLM Provider for DEMO_MODE.
    Generates realistic pricing responses, SQL queries, safety checks, and recommendations.
    """

    def generate(self, prompt: str, system_prompt: Optional[str] = None, json_mode: bool = False) -> Dict[str, Any]:
        start_time = time.time()
        p_lower = prompt.lower()
        sys_lower = (system_prompt or "").lower()

        text_out = ""

        # Check intent / routing logic
        if "supervisor" in sys_lower or "intent" in sys_lower:
            if "region" in p_lower and ("revenue" in p_lower or "declined" in p_lower or "violating" in p_lower):
                intent = "HYBRID_ANALYSIS"
            elif "sql" in p_lower or "highest revenue" in p_lower or "growth" in p_lower or "compare" in p_lower:
                intent = "DATA_ANALYSIS"
            elif "policy" in p_lower or "summarize" in p_lower or "document" in p_lower:
                intent = "DOCUMENT_QA"
            elif "report" in p_lower or "executive" in p_lower:
                intent = "REPORT_GENERATION"
            else:
                intent = "PRICING_ANALYSIS"

            res_obj = {
                "intent": intent,
                "plan": [
                    "Classify intent and parse key variables",
                    "Query vector store for document context if required",
                    "Generate and execute safe read-only SQL if structured data needed",
                    "Analyze pricing metrics & policy compliance",
                    "Synthesize evidence-backed recommendations and evaluate confidence"
                ],
                "requires_rag": intent in ["DOCUMENT_QA", "HYBRID_ANALYSIS", "PRICING_ANALYSIS", "REPORT_GENERATION"],
                "requires_sql": intent in ["DATA_ANALYSIS", "HYBRID_ANALYSIS", "REVENUE_ANALYSIS", "REPORT_GENERATION"]
            }
            text_out = json.dumps(res_obj)

        elif "sql" in sys_lower or "data analyst" in sys_lower:
            # SQL generator mock
            if "region" in p_lower and "revenue" in p_lower:
                sql = "SELECT region, SUM(revenue) as total_revenue, SUM(volume) as total_volume, AVG(pricing_rate) as avg_rate FROM transactions GROUP BY region ORDER BY total_revenue DESC;"
            elif "violating" in p_lower or "outside" in p_lower or "product x" in p_lower or "pricing range" in p_lower:
                sql = "SELECT t.region, t.product_code, t.pricing_rate, p.min_rate, p.max_rate, p.recommended_rate, SUM(t.revenue) as revenue FROM transactions t JOIN pricing_rules p ON t.product_code = p.product_code AND t.region = p.region GROUP BY t.region, t.product_code, t.pricing_rate, p.min_rate, p.max_rate, p.recommended_rate HAVING t.pricing_rate < p.min_rate OR t.pricing_rate > p.max_rate;"
            elif "volume" in p_lower or "declined" in p_lower:
                sql = "SELECT product_code, region, AVG(pricing_rate) as avg_rate, SUM(volume) as total_vol, SUM(revenue) as total_rev FROM transactions GROUP BY product_code, region ORDER BY total_vol ASC;"
            else:
                sql = "SELECT region, product_code, SUM(volume) as volume, SUM(revenue) as revenue, SUM(profit) as profit FROM transactions GROUP BY region, product_code ORDER BY revenue DESC LIMIT 10;"

            res_obj = {
                "sql": sql,
                "explanation": "Generated read-only aggregation query grouping transactions by region and product code."
            }
            text_out = json.dumps(res_obj)

        elif "pricing intelligence" in sys_lower or "pricing" in sys_lower:
            res_obj = {
                "observations": [
                    "US Enterprise Credit processing (PRD_CREDIT_PREM) is currently priced at 1.70% for select accounts, which is 15 bps below the mandatory threshold of 1.85%.",
                    "India Debit Instant (PRD_DEBIT_INST) compliant with RBI regulatory 0.40% cap, maintaining a healthy volume growth of +18% YoY.",
                    "Cross-border transaction volume has expanded by 24%, but average yield dropped from 3.10% to 2.70% in APAC_SG due to unindexed merchant contracts."
                ],
                "anomalies": [
                    "Pricing rule violation detected in 14% of PRD_CREDIT_PREM US transactions.",
                    "Cross-border FX assessment fee was omitted in 8 customer accounts."
                ],
                "revenue_impact_usd": 1425000.00
            }
            text_out = json.dumps(res_obj)

        elif "recommendation" in sys_lower:
            res_obj = {
                "recommendations": [
                    "Re-index the 14% out-of-compliance US PRD_CREDIT_PREM accounts back to standard 1.95% rate to capture $840k in annual gross revenue.",
                    "Enforce automated contract renewal locks for APAC_SG cross-border accounts to mandate the 3.10% baseline FX spread.",
                    "Implement automated pricing rule checks in the billing engine to alert account managers when quotes drop below gross margin thresholds."
                ],
                "confidence": "HIGH",
                "assumptions": ["Merchant transaction volumes remain consistent over the next 4 quarters."]
            }
            text_out = json.dumps(res_obj)

        elif "responsible ai" in sys_lower or "safety" in sys_lower:
            res_obj = {
                "is_grounded": True,
                "hallucination_score": 0.05,
                "citation_valid": True,
                "safety_status": "PASSED",
                "sanitized_response": prompt
            }
            text_out = json.dumps(res_obj)

        else:
            # Default response
            text_out = "Based on our enterprise pricing intelligence system and multi-agent analysis: The platform has evaluated all relevant pricing rules, interchange schedules, and transaction metrics. Revenue across primary regions remains strong, with key optimization opportunities identified in US Credit and APAC Cross-Border card processing."

        latency_ms = (time.time() - start_time) * 1000 + 150.0  # Realistic latency simulation
        return {
            "text": text_out,
            "prompt_tokens": len(prompt.split()) + 20,
            "completion_tokens": len(text_out.split()) + 10,
            "latency_ms": round(latency_ms, 2),
            "provider": "mock",
            "model": "mock-gpt-4o"
        }


class OpenAIProvider(BaseLLMProvider):
    def __init__(self, api_key: str, model: str = "gpt-4o"):
        from langchain_openai import ChatOpenAI
        self.client = ChatOpenAI(openai_api_key=api_key, model=model, temperature=0.1)
        self.model = model

    def generate(self, prompt: str, system_prompt: Optional[str] = None, json_mode: bool = False) -> Dict[str, Any]:
        start_time = time.time()
        messages = []
        if system_prompt:
            messages.append(("system", system_prompt))
        messages.append(("human", prompt))

        kw = {}
        if json_mode:
            kw["response_format"] = {"type": "json_object"}

        res = self.client.invoke(messages, **kw)
        latency_ms = (time.time() - start_time) * 1000

        token_usage = getattr(res, "usage_metadata", {}) or {}
        p_tokens = token_usage.get("input_tokens", len(prompt.split()))
        c_tokens = token_usage.get("output_tokens", len(res.content.split()))

        return {
            "text": res.content,
            "prompt_tokens": p_tokens,
            "completion_tokens": c_tokens,
            "latency_ms": round(latency_ms, 2),
            "provider": "openai",
            "model": self.model
        }


class GeminiProvider(BaseLLMProvider):
    def __init__(self, api_key: str, model: str = "gemini-1.5-pro"):
        from langchain_google_genai import ChatGoogleGenerativeAI
        self.client = ChatGoogleGenerativeAI(google_api_key=api_key, model=model, temperature=0.1)
        self.model = model

    def generate(self, prompt: str, system_prompt: Optional[str] = None, json_mode: bool = False) -> Dict[str, Any]:
        start_time = time.time()
        messages = []
        if system_prompt:
            messages.append(("system", system_prompt))
        messages.append(("human", prompt))

        res = self.client.invoke(messages)
        latency_ms = (time.time() - start_time) * 1000

        return {
            "text": res.content,
            "prompt_tokens": len(prompt.split()),
            "completion_tokens": len(res.content.split()),
            "latency_ms": round(latency_ms, 2),
            "provider": "gemini",
            "model": self.model
        }


def get_llm_provider() -> BaseLLMProvider:
    prov = settings.LLM_PROVIDER.lower()
    if prov == "openai" and settings.OPENAI_API_KEY:
        return OpenAIProvider(settings.OPENAI_API_KEY, settings.OPENAI_MODEL)
    elif prov == "gemini" and settings.GEMINI_API_KEY:
        return GeminiProvider(settings.GEMINI_API_KEY, settings.GEMINI_MODEL)
    return MockLLMProvider()

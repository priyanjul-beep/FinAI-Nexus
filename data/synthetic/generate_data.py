import os
import uuid
import datetime
import random

# Regions, Products, Customer Segments
REGIONS = [
    {"code": "US", "name": "United States", "currency": "USD", "compliance": "PCI-DSS v4.0 / FedNow"},
    {"code": "EU", "name": "European Union", "currency": "EUR", "compliance": "PSD2 / GDPR / EBA"},
    {"code": "APAC_IN", "name": "India", "currency": "INR", "compliance": "RBI Digital Payments / NPCI"},
    {"code": "APAC_SG", "name": "Singapore", "currency": "SGD", "compliance": "MAS Payments Act"},
    {"code": "LATAM_BR", "name": "Brazil", "currency": "BRL", "compliance": "BACEN Pix / Open Finance"}
]

PRODUCTS = [
    {"code": "PRD_CREDIT_PREM", "name": "Enterprise Premium Credit Suite", "category": "Credit", "desc": "High-tier rewards credit processing for enterprise merchants."},
    {"code": "PRD_DEBIT_INST", "name": "Instant Debit Settlement Engine", "category": "Debit", "desc": "Low-latency direct account debit processing with instant settlement."},
    {"code": "PRD_XBORDER_PAY", "name": "Cross-Border Gateway", "category": "Cross-Border", "desc": "Multi-currency FX routing and compliance engine for global trade."},
    {"code": "PRD_COMMERCIAL_CARD", "name": "Corporate Purchasing Card API", "category": "Commercial", "desc": "B2B commercial card processing with Level 3 line-item data."},
    {"code": "PRD_RECURRING_BILL", "name": "Subscription & Recurring Token", "category": "SaaS", "desc": "Automated card updater and recurring subscription billing gateway."}
]

CUSTOMER_SEGMENTS = ["Enterprise", "Mid-Market", "SMB", "Fintech Startup"]
TIERS = ["Platinum", "Gold", "Silver"]


def generate_synthetic_documents():
    docs_dir = os.path.join(os.path.dirname(__file__), "..", "documents")
    os.makedirs(docs_dir, exist_ok=True)

    doc_files = {
        "pricing_strategy_guide.md": """# Enterprise Pricing Strategy Guide v2.4 (2026)

## Executive Summary
This document defines FinAI Nexus standard pricing guidelines across all global regions and card categories. All pricing tiers must maintain gross margin targets above 42%.

## Recommended Pricing Ranges by Product
- **PRD_CREDIT_PREM (Enterprise Premium Credit)**: 1.85% - 2.25% (Recommended Baseline: 1.95%)
- **PRD_DEBIT_INST (Instant Debit Engine)**: 0.45% - 0.75% (Recommended Baseline: 0.55%)
- **PRD_XBORDER_PAY (Cross-Border Gateway)**: 2.80% - 3.40% (Recommended Baseline: 3.10%)
- **PRD_COMMERCIAL_CARD (Corporate Purchasing)**: 2.10% - 2.60% (Recommended Baseline: 2.35%)
- **PRD_RECURRING_BILL (Subscription Billing)**: 1.20% - 1.60% (Recommended Baseline: 1.35%)

## Regional Pricing Variances & Constraints
1. **India (APAC_IN)**: Due to regulatory caps, instant debit fees cannot exceed 0.40%. Credit card processing is targeted at 1.70% - 1.90%.
2. **European Union (EU)**: PSD2 interchange caps restrict consumer card interchange to 0.20% for debit and 0.30% for credit. Target net pricing margin is capped at 0.85% total merchant discount rate (MDR).
3. **United States (US)**: Highly competitive. Enterprise volume discounts (> $50M annual volume) qualify for a 15 bps discount below baseline.

## Penalty & Violation Governance
Any merchant account charged below the minimum pricing threshold without explicit CFO sign-off is flagged as a Pricing Violation. The automatic margin auditor will flag transactions yielding less than 15 bps net spread over interchange cost.
""",
        "interchange_policy.md": """# Global Interchange Fee Policy & Compliance Matrix

## Overview
Interchange fees form the foundational pass-through costs in payment processing. Rates vary by region, card category, and transaction modality.

## Standard Interchange Schedules
| Region | Card Category | Modality | Interchange Rate (%) | Fixed Fee ($) |
|---|---|---|---|---|
| US | Consumer Credit | E-commerce | 1.65% | $0.10 |
| US | Commercial Card | In-store / B2B | 2.10% | $0.15 |
| EU | Consumer Debit | E-commerce | 0.20% | €0.05 |
| EU | Consumer Credit | E-commerce | 0.30% | €0.05 |
| APAC_IN | Consumer Credit | QR / Online | 1.10% | ₹1.00 |
| APAC_SG | Cross-border Credit| E-commerce | 2.20% | $0.20 |

## Surcharging Policy
Cross-border transactions incur a compulsory 0.40% FX assessment fee added directly to the base interchange rate.
""",
        "regional_pricing_rules.md": """# Regional Pricing Compliance & Rules Manual

## APAC Region (India & Singapore)
- **India (APAC_IN)**: Pricing for UPI/Debit must comply with NPCI zero-MDR rules for small merchants (< ₹20 Lakh turnover). Commercial merchants are billed standard 0.40% debit rates.
- **Singapore (APAC_SG)**: Standard Tier 1 pricing applies. Cross-border settlement from non-SGD accounts incurs an additional 0.35% clearing fee.

## North America (US)
- Interchange-plus pricing is mandatory for all Enterprise Tier customers. Tiered (Blended) pricing is permitted only for SMB merchants with monthly volume below $50,000.

## Latin America (Brazil)
- Installment payments (Parcelado) incur a financing surcharge of 1.2% per installment month.
""",
        "product_pricing_handbook.md": """# Product Pricing Handbook 2026

## Product Line Overview
FinAI Nexus offers 5 core infrastructure payment engines:

1. **PRD_CREDIT_PREM**: Designed for high-ticket online retail. Includes automated fraud protection and chargeback guarantee.
2. **PRD_DEBIT_INST**: Low latency API processing. Ideal for quick-service restaurants and rideshare platforms.
3. **PRD_XBORDER_PAY**: Real-time currency conversion across 45 currencies. Includes automated tax calculation.
4. **PRD_COMMERCIAL_CARD**: Specialized for enterprise procurement with Level 3 line item reporting.
5. **PRD_RECURRING_BILL**: Account Updater integration, smart retries for declined recurring cards.

## Pricing Elasticity Insights
Historical data indicates that a 10 bps increase in PRD_XBORDER_PAY pricing leads to only a 1.2% drop in transaction volume, indicating low price elasticity due to high switching costs.
""",
        "revenue_optimization_guidelines.md": """# Revenue Optimization & Margin Expansion Guidelines

## Key Revenue Drivers
- **Volume Tiering**: Volume discounts start at $10M, $50M, and $250M annual processed volume.
- **Cross-Border Route Optimization**: Routing cross-border transactions through local acquirers increases approval rates by 4.2% and saves up to 50 bps in interchange fees.
- **Blended Rate Renegotiation**: Review all SMB contracts older than 18 months. Re-indexing legacy accounts to current standard pricing yields an estimated +12% net revenue expansion.
""",
        "risk_governance_policy.md": """# AI Decision Risk & Governance Policy

## Principles of AI Operation
1. **Human-in-the-loop**: High-risk decisions involving contract terminations or pricing changes exceeding 50 bps require explicit manager approval.
2. **Explainability**: Every AI agent recommendation must present verifiable data evidence and exact page citations.
3. **Hallucination Zero Tolerance**: Claims regarding numerical volume, margin rates, or rule codes must originate directly from verified SQL queries or document vector chunks.
"""
    }

    for fname, content in doc_files.items():
        filepath = os.path.join(docs_dir, fname)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[Generated Doc] {filepath}")

if __name__ == "__main__":
    generate_synthetic_documents()

# Enterprise Pricing Strategy Guide v2.4 (2026)

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

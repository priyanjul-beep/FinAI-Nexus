import os
import uuid
import datetime
import random
from sqlalchemy.orm import Session
from backend.app.database.session import SessionLocal, engine
from backend.app.auth.security import get_password_hash
from backend.app.models.domain import (
    Base, User, Product, Region, Customer, PricingRule, InterchangeRate,
    Transaction, PromptVersion, Document, DocumentChunk
)


def seed_database():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    try:
        # Check if users already seeded
        if db.query(User).first():
            print("[Seed] Database already seeded. Skipping initial seed.")
            return

        print("[Seed] Starting database seeding...")

        # 1. Users
        admin_user = User(
            id=str(uuid.uuid4()),
            email="admin@finai-nexus.io",
            hashed_password=get_password_hash("admin123"),
            full_name="Admin Director",
            role="ADMIN",
            is_active=True
        )
        analyst_user = User(
            id=str(uuid.uuid4()),
            email="analyst@finai-nexus.io",
            hashed_password=get_password_hash("analyst123"),
            full_name="Senior Pricing Analyst",
            role="ANALYST",
            is_active=True
        )
        viewer_user = User(
            id=str(uuid.uuid4()),
            email="viewer@finai-nexus.io",
            hashed_password=get_password_hash("viewer123"),
            full_name="Executive Viewer",
            role="VIEWER",
            is_active=True
        )
        db.add_all([admin_user, analyst_user, viewer_user])

        # 2. Regions
        regions = [
            Region(id=str(uuid.uuid4()), region_code="US", name="United States", currency="USD", compliance_framework="PCI-DSS / FedNow"),
            Region(id=str(uuid.uuid4()), region_code="EU", name="European Union", currency="EUR", compliance_framework="PSD2 / GDPR"),
            Region(id=str(uuid.uuid4()), region_code="APAC_IN", name="India", currency="INR", compliance_framework="RBI Digital Payments"),
            Region(id=str(uuid.uuid4()), region_code="APAC_SG", name="Singapore", currency="SGD", compliance_framework="MAS Payments Act"),
            Region(id=str(uuid.uuid4()), region_code="LATAM_BR", name="Brazil", currency="BRL", compliance_framework="BACEN Pix")
        ]
        db.add_all(regions)

        # 3. Products
        products = [
            Product(id=str(uuid.uuid4()), product_code="PRD_CREDIT_PREM", name="Enterprise Premium Credit Suite", category="Credit", description="High-tier rewards credit processing for enterprise merchants."),
            Product(id=str(uuid.uuid4()), product_code="PRD_DEBIT_INST", name="Instant Debit Settlement Engine", category="Debit", description="Low-latency direct account debit processing."),
            Product(id=str(uuid.uuid4()), product_code="PRD_XBORDER_PAY", name="Cross-Border Gateway", category="Cross-Border", description="Multi-currency FX routing and compliance engine."),
            Product(id=str(uuid.uuid4()), product_code="PRD_COMMERCIAL_CARD", name="Corporate Purchasing Card API", category="Commercial", description="B2B commercial card processing."),
            Product(id=str(uuid.uuid4()), product_code="PRD_RECURRING_BILL", name="Subscription & Recurring Token", category="SaaS", description="Automated card updater and recurring subscription billing gateway.")
        ]
        db.add_all(products)

        # 4. Customers
        customer_objs = []
        segments = ["Enterprise", "Mid-Market", "SMB", "Fintech Startup"]
        reg_codes = ["US", "EU", "APAC_IN", "APAC_SG", "LATAM_BR"]
        customer_names = [
            "Apex Global Retail", "Nexus Pay Technologies", "Aether Cloud SaaS",
            "Vanguard Logistics", "Horizon E-commerce", "Starlight FinTech",
            "OmniMart Direct", "Quantum Pay Systems", "Solaris Digital", "Zenith Commerce"
        ]

        for idx, name in enumerate(customer_names):
            cust = Customer(
                id=str(uuid.uuid4()),
                customer_name=name,
                segment=segments[idx % len(segments)],
                region=reg_codes[idx % len(reg_codes)],
                tier="Platinum" if idx < 3 else ("Gold" if idx < 7 else "Silver")
            )
            customer_objs.append(cust)
            db.add(cust)

        # 5. Pricing Rules
        rules = [
            PricingRule(id=str(uuid.uuid4()), rule_code="RULE_US_CREDIT", category="Credit", region="US", product_code="PRD_CREDIT_PREM", min_rate=1.85, max_rate=2.25, recommended_rate=1.95, guidelines="Target 40%+ gross margin on credit processing."),
            PricingRule(id=str(uuid.uuid4()), rule_code="RULE_US_DEBIT", category="Debit", region="US", product_code="PRD_DEBIT_INST", min_rate=0.45, max_rate=0.75, recommended_rate=0.55, guidelines="Instant debit pricing range."),
            PricingRule(id=str(uuid.uuid4()), rule_code="RULE_EU_CREDIT", category="Credit", region="EU", product_code="PRD_CREDIT_PREM", min_rate=0.70, max_rate=1.10, recommended_rate=0.85, guidelines="EU PSD2 interchange cap constrained rate."),
            PricingRule(id=str(uuid.uuid4()), rule_code="RULE_IN_DEBIT", category="Debit", region="APAC_IN", product_code="PRD_DEBIT_INST", min_rate=0.30, max_rate=0.45, recommended_rate=0.40, guidelines="RBI regulatory cap for debit merchant discount rate."),
            PricingRule(id=str(uuid.uuid4()), rule_code="RULE_XBORDER", category="Cross-Border", region="APAC_SG", product_code="PRD_XBORDER_PAY", min_rate=2.80, max_rate=3.40, recommended_rate=3.10, guidelines="Includes FX multi-currency assessment spread.")
        ]
        db.add_all(rules)

        # 6. Interchange Rates
        ic_rates = [
            InterchangeRate(id=str(uuid.uuid4()), region="US", card_category="Consumer Credit", transaction_type="E-commerce", tier="Standard", interchange_rate_pct=1.65, min_fee=0.10, max_fee=0.0),
            InterchangeRate(id=str(uuid.uuid4()), region="US", card_category="Commercial Card", transaction_type="In-store", tier="Standard", interchange_rate_pct=2.10, min_fee=0.15, max_fee=0.0),
            InterchangeRate(id=str(uuid.uuid4()), region="EU", card_category="Consumer Debit", transaction_type="E-commerce", tier="Standard", interchange_rate_pct=0.20, min_fee=0.05, max_fee=0.0),
            InterchangeRate(id=str(uuid.uuid4()), region="EU", card_category="Consumer Credit", transaction_type="E-commerce", tier="Standard", interchange_rate_pct=0.30, min_fee=0.05, max_fee=0.0),
            InterchangeRate(id=str(uuid.uuid4()), region="APAC_IN", card_category="Consumer Credit", transaction_type="Online", tier="Standard", interchange_rate_pct=1.10, min_fee=0.0, max_fee=0.0)
        ]
        db.add_all(ic_rates)

        # 7. Transactions (Generate 250 realistic transactions)
        base_date = datetime.datetime(2026, 1, 1)
        prod_codes = ["PRD_CREDIT_PREM", "PRD_DEBIT_INST", "PRD_XBORDER_PAY", "PRD_COMMERCIAL_CARD", "PRD_RECURRING_BILL"]
        countries = {"US": "United States", "EU": "Germany", "APAC_IN": "India", "APAC_SG": "Singapore", "LATAM_BR": "Brazil"}

        for i in range(250):
            cust = random.choice(customer_objs)
            p_code = random.choice(prod_codes)
            tx_date = base_date + datetime.timedelta(days=random.randint(0, 180), hours=random.randint(0, 23))

            volume = random.randint(100, 50000)
            avg_ticket = random.uniform(25.0, 450.0)
            tx_value = volume * avg_ticket

            # Pricing & Interchange logic
            if p_code == "PRD_CREDIT_PREM":
                ic_pct = 1.65
                pr_pct = random.choice([1.95, 1.90, 2.10, 1.70])  # Note 1.70 is below recommended 1.85!
            elif p_code == "PRD_DEBIT_INST":
                ic_pct = 0.25
                pr_pct = random.choice([0.55, 0.50, 0.60, 0.40])
            elif p_code == "PRD_XBORDER_PAY":
                ic_pct = 2.20
                pr_pct = random.choice([3.10, 3.20, 2.90, 2.70])  # 2.70 below min 2.80!
            else:
                ic_pct = 1.80
                pr_pct = random.choice([2.35, 2.20, 2.50])

            rev = tx_value * (pr_pct / 100.0)
            cost = tx_value * (ic_pct / 100.0) + (volume * 0.05)
            profit = rev - cost

            tx = Transaction(
                id=str(uuid.uuid4()),
                transaction_date=tx_date,
                customer_id=cust.id,
                region=cust.region,
                country=countries.get(cust.region, "United States"),
                product_code=p_code,
                customer_segment=cust.segment,
                volume=volume,
                value=round(tx_value, 2),
                interchange_rate=ic_pct,
                pricing_rate=pr_pct,
                revenue=round(rev, 2),
                cost=round(cost, 2),
                profit=round(profit, 2)
            )
            db.add(tx)

        # 8. Initial Prompt Versions
        pv_supervisor = PromptVersion(
            id=str(uuid.uuid4()),
            prompt_name="supervisor_intent_classifier",
            version="1.0.0",
            description="Supervisor agent intent classification prompt",
            template="""You are the Orchestrator Supervisor for FinAI Nexus Enterprise Platform.
Analyze the user query: "{user_query}"
Classify intent into one of: DOCUMENT_QA, DATA_ANALYSIS, PRICING_ANALYSIS, REVENUE_ANALYSIS, HYBRID_ANALYSIS, REPORT_GENERATION, DOCUMENT_SUMMARY, GENERAL_AI_QUERY.
Determine required sub-agents.""",
            variables_json=["user_query"],
            is_active=True
        )
        db.add(pv_supervisor)

        db.commit()
        print("[Seed] Database successfully seeded with synthetic records, pricing rules, and transactions!")

    except Exception as e:
        db.rollback()
        print(f"[Seed Error] {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()

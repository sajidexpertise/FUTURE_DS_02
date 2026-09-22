"""Rebuild the deterministic Retention Engine demonstration project.

Run from any location: python scripts/build.py
Requires only the Python standard library.
"""
from __future__ import annotations

import csv
import json
import random
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RNG = random.Random(20260922)
PLAN_PRICE = {"Basic": 15, "Standard": 29, "Premium": 49, "Enterprise": 89}
BASE_HAZARD = {"Basic": .027, "Standard": .021, "Premium": .016, "Enterprise": .012}
REASONS = ["Price", "Low usage", "Alternative", "Product experience", "Changed needs", "Payment issue"]
REASON_WEIGHTS = [29, 25, 19, 13, 9, 5]
FIELDS = ["customer_id", "signup_date", "signup_quarter", "region", "segment", "plan",
          "billing_cycle", "acquisition_channel", "engagement_score", "monthly_price_usd",
          "churn_month", "churn_reason", "risk_at_month_3", "risk_at_month_12",
          "status_month_3", "status_month_12", "months_billed", "observed_revenue_12m_usd"]


def quarter(month: int) -> str:
    return f"Q{(month - 1) // 3 + 1} 2024"


def generate() -> list[dict]:
    rows = []
    for i in range(1, 4801):
        month = RNG.choices(range(1, 13), weights=[84, 80, 91, 95, 101, 103, 96, 99, 105, 113, 125, 132])[0]
        signup_date = date(2024, month, RNG.randint(1, 28)).isoformat()
        plan = RNG.choices(list(PLAN_PRICE), [34, 37, 22, 7])[0]
        segment = RNG.choices(["Individual", "Freelancer", "Small Business", "Team"], [49, 21, 24, 6])[0]
        region = RNG.choices(["North America", "Europe", "Asia-Pacific", "Other"], [38, 29, 23, 10])[0]
        source = RNG.choices(["Organic", "Paid Search", "Referral", "Social", "Partner"], [32, 26, 18, 15, 9])[0]
        annual_probability = {"Basic": .18, "Standard": .32, "Premium": .48, "Enterprise": .68}[plan]
        billing = "Annual" if RNG.random() < annual_probability else "Monthly"
        price = PLAN_PRICE[plan] * (.85 if billing == "Annual" else 1)
        engagement = round(RNG.betavariate(2.4, 1.8), 3)
        churn_month = 13
        for m in range(1, 13):
            early = 1.85 if m == 1 else 1.45 if m <= 3 else .96
            engagement_factor = 1.32 if engagement < .32 else 1.12 if engagement < .5 else .77 if engagement > .78 else 1
            cycle_factor = .82 if billing == "Annual" else 1
            source_factor = 1.12 if source == "Paid Search" else .92 if source == "Referral" else 1
            if RNG.random() < BASE_HAZARD[plan] * early * engagement_factor * cycle_factor * source_factor:
                churn_month = m
                break
        risk3 = churn_month > 3 and (engagement < .33 or RNG.random() < .055)
        risk12 = churn_month > 12 and (engagement < .34 or RNG.random() < .068)
        m3 = "Churned" if churn_month <= 3 else "At risk" if risk3 else "Active"
        m12 = "Churned" if churn_month <= 12 else "At risk" if risk12 else "Renewed" if billing == "Annual" else "Active"
        reason = RNG.choices(REASONS, REASON_WEIGHTS)[0] if churn_month <= 12 else ""
        months_billed = min(churn_month, 12)
        rows.append({
            "customer_id": f"RC-{i:05d}", "signup_date": signup_date, "signup_quarter": quarter(month),
            "region": region, "segment": segment, "plan": plan, "billing_cycle": billing,
            "acquisition_channel": source, "engagement_score": engagement,
            "monthly_price_usd": round(price, 2), "churn_month": churn_month if churn_month <= 12 else "",
            "churn_reason": reason, "risk_at_month_3": risk3, "risk_at_month_12": risk12,
            "status_month_3": m3, "status_month_12": m12, "months_billed": months_billed,
            "observed_revenue_12m_usd": round(price * months_billed, 2)
        })
    return rows


def summary(rows: list[dict]) -> dict:
    n = len(rows)
    churned = [r for r in rows if r["churn_month"] != ""]
    active = n - len(churned)
    annual = [r for r in rows if r["billing_cycle"] == "Annual"]
    reasons = dict(Counter(r["churn_reason"] for r in churned))
    cohorts = {}
    for q in ["Q1 2024", "Q2 2024", "Q3 2024", "Q4 2024"]:
        group = [r for r in rows if r["signup_quarter"] == q]
        cohorts[q] = {"size": len(group), "retention": [round(sum(r["churn_month"] == "" or r["churn_month"] > m for r in group) / len(group), 4) for m in range(1, 13)]}
    plans = {}
    for p in PLAN_PRICE:
        group = [r for r in rows if r["plan"] == p]
        plans[p] = {"customers": len(group), "retained_12m": sum(r["churn_month"] == "" for r in group),
                    "retention_rate_12m": round(sum(r["churn_month"] == "" for r in group) / len(group), 4)}
    return {
        "data_note": "Deterministic synthetic subscription data; no actual customer records.",
        "customers": n, "retained_12m": active, "churned_within_12m": len(churned),
        "retention_rate_12m": round(active / n, 4), "churn_rate_12m": round(len(churned) / n, 4),
        "renewed_annual": sum(r["status_month_12"] == "Renewed" for r in rows),
        "annual_customers": len(annual),
        "annual_renewal_rate": round(sum(r["status_month_12"] == "Renewed" for r in rows) / len(annual), 4),
        "value_per_customer_12m_usd": round(sum(r["observed_revenue_12m_usd"] for r in rows) / n, 2),
        "revenue_observed_12m_usd": round(sum(r["observed_revenue_12m_usd"] for r in rows), 2),
        "churn_first_3m": sum(r["churn_month"] != "" and r["churn_month"] <= 3 for r in rows),
        "reasons": reasons, "cohorts": cohorts, "plans": plans,
        "month_3_status": dict(Counter(r["status_month_3"] for r in rows)),
        "month_12_status": dict(Counter(r["status_month_12"] for r in rows))
    }


def main() -> None:
    rows = generate()
    with (ROOT / "data" / "customers.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    result = summary(rows)
    (ROOT / "data" / "summary.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    template = (ROOT / "dashboard.template.html").read_text(encoding="utf-8")
    payload = json.dumps(rows, separators=(",", ":")).replace("<", "\\u003c")
    (ROOT / "index.html").write_text(template.replace("/*__DATA__*/[]", payload), encoding="utf-8")
    print(f"{len(rows)} customers, {result['retained_12m']} retained at month 12, "
          f"{result['churned_within_12m']} churned, {result['retention_rate_12m']:.1%} retention")


if __name__ == "__main__":
    main()

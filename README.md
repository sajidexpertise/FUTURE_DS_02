# Retention Engine

An interactive customer retention and churn analysis dashboard for **Future Interns Data Science & Analytics — Task 2**. The layout follows a wide customer journey workspace: Sankey style flows, lifecycle ring, churn reason bars, 12-month cohort heatmap, retention waterfall, and practical experiment prompts.

## Open the dashboard

Open `index.html` in any modern browser. No server, install, API key, or network connection is needed for the data or charts. The optional Google Fonts request can fail offline; local fallback fonts keep the dashboard usable. The dashboard works on desktop and mobile; on small screens, scroll horizontally inside the customer journey graphic to see all four stages.

Select a signup cohort, region, segment, or plan at the top. **Every** number and chart recalculates from the matching customers. Use **Export filtered CSV** to download the selected records.

## Files

| Path | Purpose |
| --- | --- |
| `index.html` | Standalone dashboard with embedded customer data |
| `dashboard.template.html` | Editable dashboard source; `/*__DATA__*/[]` is replaced by the generator |
| `data/customers.csv` | 4,800 synthetic customer records |
| `data/summary.json` | Reconciled whole-population results |
| `scripts/build.py` | Seeded dataset generation and dashboard rebuild (Python standard library) |
| `docs/ANALYSIS.md` | Methodology, findings, limits, recommended experiments |

## Rebuild

```bash
python scripts/build.py
```

The seed is fixed; rerunning regenerates the same CSV, summary, and embedded dashboard. If you change dashboard code, edit `dashboard.template.html`, then rebuild; `index.html` is generated output.

## Metric definitions

- Each signup is observed for its **first twelve months**, including Q4 2024 signups into 2025. Months are relative to signup, so no cohort is right-censored in this demonstration.
- `churn_month = 1` means the customer pays for month 1 and is no longer subscribed at the **end** of month 1. Retained at month `m` means `churn_month > m` or no churn in the first 12 months.
- Month 12 retention is retained signups divided by selected signups. Churn is its complement.
- Active, Renewed, At risk, and Churned are mutually exclusive month 12 labels. Active + Renewed + At risk equals retained; annual subscribers who remain and are not flagged at risk are labeled Renewed.
- Annual plan renewal is customers labeled Renewed divided by selected annual plan signups. At-risk annual customers are excluded from the numerator; this is a **simulated confirmed-renewal proxy**, not payment-system renewal data.
- 12-month value per customer is observed billed revenue during the first 12 months divided by selected signups. It is **not** lifetime value. Annual plans use a discounted monthly equivalent and the same observed billed-month model; this is a simplified synthetic billing assumption.
- The cohort heatmap uses each signup quarter as its denominator. Churn reason percentages use the selected churned population; reasons are assigned once per churned customer.

## Publish to GitHub

Create a repository named `FUTURE_DS_02` and upload the **contents** of this folder at its root. If you want a public live demo, go to repository **Settings → Pages**, choose deployment from the main branch root, and save. `index.html` is already at root. The CSV and methodology make the project auditable for an internship submission.

Suggested repository description: **Interactive customer retention and churn analysis with cohort tracking, lifecycle flows, and actionable insights.**

## Data provenance

**All customers and churn outcomes are simulated.** This project does not claim real company results or measured intervention effects. The generator describes the exact assumptions; the recommendations are hypotheses to test.

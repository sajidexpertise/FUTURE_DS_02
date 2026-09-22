# Customer retention and churn analysis

## Objective

Study which subscribers leave during their first year, where the largest drop occurs, how retention varies across signup cohorts and plans, and what experiments the business might run next. This is a **demonstration on synthetic data**, generated using a fixed seed. No real customer information is used.

## Dataset and preparation

4,800 simulated subscribers signed up in 2024. Each is followed for exactly twelve relative months; late-2024 signups therefore have simulated follow-up into 2025. A row records signup date and quarter, segment, region, acquisition channel, plan, billing cycle, engagement score, churn month and reason, month 3/month 12 status, months billed, and first-year observed revenue. There are no unobserved 12-month outcomes.

The generator assigns base monthly churn hazards by plan, adjusts them for early tenure, engagement, billing, and acquisition, then simulates first churn month and a single reported reason. Those built-in relationships are **assumptions of the simulation**, not discoveries about real customers.

## Results for the full sample

| Measure | Value | Calculation |
| --- | ---: | --- |
| 2024 signups | 4,800 | Count of customer records |
| Retained at month 12 | 3,656 (76.2%) | No churn during months 1–12 |
| Churned within 12 months | 1,144 (23.8%) | Churn month between 1 and 12 |
| Churned by month 3 | 437 | First three relative months |
| Annual plan renewal proxy | 1,011 / 1,640 (61.6%) | Renewed status / annual signups; at-risk annual users are excluded |
| First-year observed revenue | $1,572,785.85 | Sum of billed-month equivalents |
| First-year value per signup | $327.66 | Observed revenue / 4,800 |

The month 12 lifecycle comprises 1,903 Active, 1,011 Renewed, 742 At risk, and 1,144 Churned. These sum to 4,800; the first three sum to the 3,656 retained.

| Signup cohort | Customers | Month 12 retention |
| --- | ---: | ---: |
| Q1 2024 | 1,037 | 74.4% |
| Q2 2024 | 1,157 | 76.7% |
| Q3 2024 | 1,142 | 77.1% |
| Q4 2024 | 1,464 | 76.2% |

| Plan | Customers | Month 12 retention |
| --- | ---: | ---: |
| Basic | 1,656 | 68.4% |
| Standard | 1,732 | 78.1% |
| Premium | 1,084 | 81.6% |
| Enterprise | 328 | 87.5% |

The largest recorded churn reason is Price (325 of 1,144 churns), followed by Low usage (300). The reason shares are about 28% and 26%, respectively. These are simulated self-reported labels, not independent causal evidence.

## Recommendations to test

1. **First-week onboarding:** 437 churns occur by month 3. Test clearer setup and early usage prompts against an unchanged holdout, with month-3 and month-12 retention as outcomes.
2. **At-risk outreach:** 742 subscribers remain active but flagged at risk at month 12. Randomize a support or value education message and measure subsequent renewal, guardrails, and intervention costs.
3. **Pricing research:** Price is the most frequent recorded churn reason. Interview customers and test carefully targeted packaging before assuming a general discount would improve net revenue.

## Limits

The observed plan differences cannot establish that upgrading a subscriber would change their survival; plan choices and base hazards are generated. The dashboard uses simple deterministic flags for at-risk labels. Revenue assumes a monthly equivalent even on annual plans. No confidence intervals, verified causal effects, or forecasts are presented. A real implementation would require consented customer data, actual renewal events, transaction ledgers, complete cohorts, and validation of churn reasons.

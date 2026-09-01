# Funnel Conversion Reporter

Takes stage-by-stage funnel counts (visitor → lead → MQL → SQL → opportunity → closed-won) over time and reports conversion rates, drop-off points, and — if you provide spend — CAC and cost-per-stage.

Built for exactly the "data-driven reporting on program ROI and customer acquisition costs" work that sits at the center of most GTM/RevOps roles — the report you'd actually bring to a pipeline review or board update.

## What it does

1. Takes weekly/monthly funnel stage counts plus optional marketing spend
2. Calculates stage-to-stage conversion rates (e.g. Lead → MQL %)
3. Flags the single biggest drop-off stage — where to focus first
4. Calculates CAC (spend ÷ closed-won) if spend data is present
5. Prints a clean text funnel report with a simple ASCII bar chart — no charting library needed

## Quick start

```bash
git clone https://github.com/rubianaseem/funnel-conversion-reporter.git
cd funnel-conversion-reporter
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python funnel_conversion_reporter.py --input sample_funnel_data.csv
```

No API key needed — this is pure arithmetic on your funnel numbers.

## Example output

```
FUNNEL REPORT — Aug 2026

Visitors        12,400  ██████████████████████████████████████████████████
Leads              620  ██  (5.0% of Visitors)
MQLs                210  █  (33.9% of Leads)
SQLs                 84  █  (40.0% of MQLs)
Opportunities        38  █  (45.2% of SQLs)
Closed Won           11  █  (28.9% of Opportunities)

Biggest drop-off: Visitors -> Leads (95.0% lost here)
Overall conversion: 0.09% (visitor to closed-won)

Spend: $18,500 | CAC: $1,682 per closed-won deal
```

## Cost note

Zero LLM calls — entirely arithmetic. Run this as often as your funnel data updates (daily/weekly), no cost concern at all.

## GTM tech stack this maps to

| Step | Tool used here | Swap with |
|---|---|---|
| Funnel stage counts in | CSV | GA4 (via API/export), HubSpot funnel report export, Salesforce report |
| Spend data | CSV column | GA4/ad platform export, Looker Studio data source |
| Report output | Console text | Push into Looker Studio as a data source, post to Slack, or email a formatted summary |

## Customising for your stack

- `FUNNEL_STAGES` at the top of the script defines your stage names and order — edit to match your actual funnel (add/remove stages freely)
- Swap `sample_funnel_data.csv` for a live export and schedule this to run weekly for a standing funnel health check
- If you track spend by channel, extend the script to break CAC out per channel rather than one blended number

## How this runs today (and what production would add)

**Trigger:** none built in — run manually (`python funnel_conversion_reporter.py --input ...`) or schedule it (weekly/monthly cron) once you've automated the data pull. It doesn't refresh itself.

**Action taken:** prints the funnel report to your terminal. It does **not** push anything into Looker Studio, Slack, or email — you'd add that step to actually distribute the report.

**Self-learning:** no. It's pure arithmetic (conversion rates, CAC) — no model, no learning from trends over time beyond what you compute yourself period over period.

**Loop:** no persistent process — reads one period's data, reports, exits.

**What a production version would add:**
- Automated data pulls from GA4/HubSpot/Salesforce APIs instead of a manual CSV per period
- A Slack post or email of the report to leadership on a schedule
- Feeding output into Looker Studio as a data source, so it becomes a live dashboard rather than a point-in-time terminal report
- Period-over-period comparison (this version only reports one period at a time)

# Setup Guide

## 1. Where this installs

Plain Python script, no external dependencies — nothing to install beyond Python itself.

```bash
git clone https://github.com/rubianaseem/funnel-conversion-reporter.git
cd funnel-conversion-reporter
```

## 2. Run it with sample data

```bash
python funnel_conversion_reporter.py --input sample_funnel_data.csv
```

## 3. Connecting real funnel data

This script expects one row per reporting period with a count for each funnel stage plus optional spend — here's how to build that row from common sources:

**GA4 (visitors)**
Use GA4's Reporting API (or just the GA4 UI's Explore reports) to pull total users/sessions for your date range — that's your `visitors` count. If you're comfortable with the API, `google-analytics-data` (Python package) can pull this automatically.

**HubSpot (leads, MQLs, SQLs)**
HubSpot's lifecycle stages map directly: count contacts that entered "Lead," "Marketing Qualified Lead," and "Sales Qualified Lead" stages in the period. Pull via a HubSpot report export, or the Contacts API filtered by lifecycle stage and stage-entry date.

**Salesforce (opportunities, closed-won)**
A simple report grouped by Stage, filtered to Created Date in the period, gives you `opportunities`. Filter to Stage = Closed Won for `closed_won`.

**Ad spend (GA4 / ad platforms / Looker Studio)**
If you're already pulling cost data into Looker Studio from your ad platforms, export that total for the same period into the `spend` column.

## 4. Automating this

Once each source above has an API pull instead of a manual export, replace `load_period()` in the script with a function that queries each source and assembles the row — or, simpler, keep pulling into a shared Google Sheet/warehouse table and have this script read the latest row from there.

## 5. Using this repo with an AI coding assistant (Cursor, Claude Code, Codex, Grok)

**Cursor** — open the folder, ask in chat (Cmd+L): *"Add a function that pulls visitor counts from the GA4 Data API for a given date range and returns them in the format load_period expects"*

**Claude Code** — `cd` into the folder, run `claude`, ask the same way

**Codex CLI** — `cd` into the folder, run `codex`, same approach

**Grok (or any chat-only assistant)** — paste `funnel_conversion_reporter.py`'s contents into the chat with your request, then copy the result back into the file

## Troubleshooting

- **"StopIteration" error** — your CSV is empty or missing a header row; it expects exactly one data row per run
- **CAC shows "n/a"** — either `spend` is blank in your CSV, or `closed_won` is 0 for that period
- **Bar chart looks off / all one length** — check `visitors` (the first stage) isn't 0, since every bar is scaled relative to it

#!/usr/bin/env python3
"""
Funnel Conversion Reporter
----------------------------
Reports stage-to-stage conversion rates, the biggest drop-off point, and
CAC (if spend data is provided) from a funnel stage-counts CSV.

Usage:
    python funnel_conversion_reporter.py --input sample_funnel_data.csv
"""

import argparse
import csv
import os
import sys

FUNNEL_STAGES = ["visitors", "leads", "mqls", "sqls", "opportunities", "closed_won"]
STAGE_LABELS = {
    "visitors": "Visitors",
    "leads": "Leads",
    "mqls": "MQLs",
    "sqls": "SQLs",
    "opportunities": "Opportunities",
    "closed_won": "Closed Won",
}
BAR_MAX_WIDTH = 50


def load_period(path: str) -> dict:
    with open(path, newline="", encoding="utf-8") as f:
        row = next(csv.DictReader(f))
    return row


def bar(value: int, max_value: int) -> str:
    if max_value == 0:
        return ""
    width = max(1, int((value / max_value) * BAR_MAX_WIDTH))
    return "█" * width


def main():
    parser = argparse.ArgumentParser(description="Report funnel conversion rates and CAC.")
    parser.add_argument("--input", required=True, help="Path to a funnel data CSV file")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    row = load_period(args.input)
    period_label = row.get("period", "Reporting Period")
    counts = {stage: int(row.get(stage, 0)) for stage in FUNNEL_STAGES}
    spend = float(row["spend"]) if row.get("spend", "").strip() else None

    max_count = counts[FUNNEL_STAGES[0]]

    print(f"FUNNEL REPORT — {period_label}\n")

    biggest_drop = None
    biggest_drop_pct = -1

    for i, stage in enumerate(FUNNEL_STAGES):
        count = counts[stage]
        label = STAGE_LABELS[stage]
        bar_str = bar(count, max_count)
        if i == 0:
            print(f"{label:<15}{count:>8,}  {bar_str}")
        else:
            prev_stage = FUNNEL_STAGES[i - 1]
            prev_count = counts[prev_stage]
            conv_pct = (count / prev_count * 100) if prev_count else 0
            drop_pct = 100 - conv_pct
            print(
                f"{label:<15}{count:>8,}  {bar_str}  "
                f"({conv_pct:.1f}% of {STAGE_LABELS[prev_stage]})"
            )
            if drop_pct > biggest_drop_pct:
                biggest_drop_pct = drop_pct
                biggest_drop = f"{STAGE_LABELS[prev_stage]} -> {label}"

    overall_conversion = (
        (counts["closed_won"] / counts["visitors"] * 100) if counts["visitors"] else 0
    )

    print(f"\nBiggest drop-off: {biggest_drop} ({biggest_drop_pct:.1f}% lost here)")
    print(f"Overall conversion: {overall_conversion:.2f}% (visitor to closed-won)")

    if spend is not None and counts["closed_won"] > 0:
        cac = spend / counts["closed_won"]
        print(f"\nSpend: ${spend:,.0f} | CAC: ${cac:,.0f} per closed-won deal")
    elif spend is not None:
        print(f"\nSpend: ${spend:,.0f} | CAC: n/a (no closed-won deals this period)")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Count records in raw dataset"""

import glob
import csv
import os

files = sorted(glob.glob('D:/Temp/lottery_analyzer/data/raw/*.csv'))

print('=' * 80)
print('COMPLETE RAW DATASET SUMMARY')
print('=' * 80)
print(f"{'Lottery':<40} {'Records':>10} {'Date Range':<25}")
print('-' * 80)

nlb_total = 0
dlb_total = 0

for f in files:
    name = os.path.basename(f).replace('.csv', '').replace('_', ' ').title()
    with open(f, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
        count = len(rows)

        # Get date range
        if rows:
            dates = [r.get('draw_date', '') for r in rows if r.get('draw_date')]
            if dates:
                date_range = f"{min(dates)} to {max(dates)}"
            else:
                date_range = "N/A"
        else:
            date_range = "N/A"

    if 'nlb' in f.lower():
        nlb_total += count
    else:
        dlb_total += count

    print(f'{name:<40} {count:>10,} {date_range:<25}')

print('-' * 80)
print(f"{'NLB Subtotal (8 lotteries)':<40} {nlb_total:>10,}")
print(f"{'DLB Subtotal (9 lotteries)':<40} {dlb_total:>10,}")
print('-' * 80)
print(f"{'TOTAL RECORDS (17 lotteries)':<40} {nlb_total + dlb_total:>10,}")
print('=' * 80)

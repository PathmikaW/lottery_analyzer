"""
Scrape lottery data WITH prize information.

Prize data availability:
- NLB: Full prize data available via HTML tables (pattern, prize, winners, total)
- DLB: Prize data is displayed as images, cannot be scraped

This script creates CSV files with '_with_prizes' suffix for NLB lotteries only.
"""

from src.scrapers.nlb_scraper import NLBScraper
import pandas as pd
import os

print("="*70)
print("Sri Lankan Lottery Data Collection - WITH PRIZES")
print("="*70)
print("\nNote: Only NLB lotteries support prize data scraping.")
print("DLB displays prizes as images which cannot be parsed.\n")

# NLB Lotteries - Prize data is consistently available via HTML
print("[NLB] Scraping NLB Lotteries with Prize Data...")
print("-"*70)

nlb_scraper = NLBScraper()
nlb_lotteries = [
    'mahajana_sampatha',
    'govisetha',
    'dhana_nidhanaya',
    'handahana',
    'mega_power',
    'ada_sampatha',
    'suba_dawasak',
    'nlb_jaya'
]

nlb_total = 0
nlb_success = 0
nlb_failed = 0

for game in nlb_lotteries:
    print(f"\nScraping {game} with prizes...")
    try:
        # Scrape with prizes - this fetches prize data for each draw
        results = nlb_scraper.scrape_game(game, fetch_prizes=True)

        if results:
            # Save to CSV with '_with_prizes' suffix
            df = pd.DataFrame(results)
            output_path = f'data/raw/nlb_{game}_with_prizes.csv'
            df.to_csv(output_path, index=False)

            nlb_total += len(results)
            nlb_success += 1

            # Count how many draws have prize data
            prize_cols = [col for col in df.columns if 'prize' in col.lower() or 'winner' in col.lower()]
            has_prizes = len(prize_cols) > 0

            print(f"  [OK] Found {len(results)} draws with prize data")
            print(f"  [OK] Saved to {output_path}")
            if has_prizes:
                print(f"  [OK] Prize columns: {len(prize_cols)}")
        else:
            print(f"  [ERROR] No data found")
            nlb_failed += 1

    except Exception as e:
        print(f"  [ERROR] Error: {e}")
        nlb_failed += 1

print("\n" + "="*70)
print("PRIZE SCRAPING COMPLETE")
print("="*70)
print(f"NLB Lotteries:")
print(f"  - Successfully scraped: {nlb_success}/{len(nlb_lotteries)}")
print(f"  - Total draws with prizes: {nlb_total}")
print(f"  - Files saved to: data/raw/nlb_*_with_prizes.csv")
print()
print(f"DLB Lotteries:")
print(f"  - Prize data displayed as images (not scrapable)")
print(f"  - Use basic CSV files: data/raw/dlb_*.csv")
print("="*70)

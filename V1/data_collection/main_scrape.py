
import argparse, csv
from typing import List, Dict
from scrapers import NLBScraper

def write_csv(rows: List[Dict], path: str) -> None:
    if not rows:
        print("No rows parsed; nothing written.")
        return
    keys = sorted({k for r in rows for k in r.keys()})
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"Wrote {len(rows)} rows -> {path}")

def main():
    ap = argparse.ArgumentParser(description="NLB Lottery Scraper (Mahajana Sampatha & Govisetha)")
    ap.add_argument("--game", choices=["mahajana_sampatha", "govisetha"], required=True)
    ap.add_argument("--out", required=True, help="Output CSV path")
    ap.add_argument("--prizes", action="store_true", help="Fetch prize structure for each draw (slower)")
    args = ap.parse_args()

    scraper = NLBScraper(fetch_prizes=args.prizes)
    print(f"Scraping {args.game}{'with prize data' if args.prizes else ''}...")
    rows = scraper.scrape_game(args.game)
    write_csv(rows, args.out)

if __name__ == "__main__":
    main()

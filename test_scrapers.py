#!/usr/bin/env python3
"""
Test and validate scrapers for both NLB and DLB
"""

from src.scrapers import NLBScraper, DLBScraper

def test_nlb_scraper():
    """Test NLB scraper with sample lotteries"""
    print("=" * 70)
    print("TESTING NLB SCRAPER")
    print("=" * 70)

    scraper = NLBScraper()
    test_games = ['mahajana_sampatha', 'govisetha']
    nlb_results = {}

    for game in test_games:
        try:
            print(f"\nTesting: {game}")
            results = scraper.scrape_game(game)
            nlb_results[game] = results

            if results:
                print(f"[PASS] Found {len(results)} draws")
                # Show first result
                first = results[0]
                print(f"  Sample: Draw {first.get('draw_id')} - {first.get('draw_date')}")
                print(f"  Numbers: {first.get('numbers')}")
                print(f"  Letter: {first.get('letter')}")
            else:
                print(f"[FAIL] No draws found")

        except Exception as e:
            print(f"[ERROR] {e}")
            nlb_results[game] = []

    return nlb_results

def test_dlb_scraper():
    """Test DLB scraper with sample lotteries"""
    print("\n" + "=" * 70)
    print("TESTING DLB SCRAPER")
    print("=" * 70)

    scraper = DLBScraper()
    test_games = ['shanida', 'ada_kotipathi']
    dlb_results = {}

    for game in test_games:
        try:
            print(f"\nTesting: {game}")
            results = scraper.scrape_game(game)
            dlb_results[game] = results

            if results:
                print(f"[PASS] Found {len(results)} draws")
                # Show first result
                first = results[0]
                print(f"  Sample: Draw {first.get('draw_id')} - {first.get('draw_date')}")
                print(f"  Numbers: {first.get('numbers')}")
                print(f"  Letter: {first.get('letter')}")
            else:
                print(f"[FAIL] No draws found - need to fix HTML parsing")

        except Exception as e:
            print(f"[ERROR] {e}")
            dlb_results[game] = []

    return dlb_results

def validate_data_quality(results, source):
    """Validate scraped data quality"""
    print(f"\n  Validating {source} data quality...")

    if not results:
        print(f"  [FAIL] No data to validate")
        return False

    required_fields = ['draw_id', 'draw_date', 'numbers', 'game']
    valid_count = 0

    for result in results[:5]:  # Check first 5
        all_fields_present = True
        for field in required_fields:
            if field not in result or not result[field]:
                print(f"  [FAIL] Missing {field} in draw {result.get('draw_id', 'unknown')}")
                all_fields_present = False
        if all_fields_present:
            valid_count += 1

    if valid_count == len(results[:5]):
        print(f"  [PASS] Data validation passed ({valid_count}/5 records)")
        return True
    else:
        print(f"  [WARN] Partial validation ({valid_count}/5 records)")
        return False

if __name__ == "__main__":
    nlb_results = test_nlb_scraper()
    dlb_results = test_dlb_scraper()

    print("\n" + "=" * 70)
    print("DATA VALIDATION")
    print("=" * 70)

    # Validate NLB
    for game, results in nlb_results.items():
        if results:
            validate_data_quality(results, f"NLB {game}")

    # Validate DLB
    for game, results in dlb_results.items():
        if results:
            validate_data_quality(results, f"DLB {game}")

    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    nlb_total = sum(len(r) for r in nlb_results.values())
    dlb_total = sum(len(r) for r in dlb_results.values())
    print(f"NLB Total Draws: {nlb_total}")
    print(f"DLB Total Draws: {dlb_total}")
    print(f"Grand Total: {nlb_total + dlb_total}")
    print("=" * 70)

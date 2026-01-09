#!/usr/bin/env python3
"""
CLI tool to scrape Sri Lankan lottery data
Usage:
    python run_scrapers.py --all                    # Scrape all 18 lotteries
    python run_scrapers.py --source nlb --game mahajana_sampatha  # Scrape single lottery
"""

import argparse
import sys
from src.scrapers import ScraperManager, NLBScraper, DLBScraper


def main():
    parser = argparse.ArgumentParser(description='Sri Lankan Lottery Data Scraper')

    parser.add_argument('--all', action='store_true',
                        help='Scrape all 18 lotteries (9 NLB + 9 DLB)')

    parser.add_argument('--source', choices=['nlb', 'dlb'],
                        help='Lottery source (nlb or dlb)')

    parser.add_argument('--game', type=str,
                        help='Specific game to scrape')

    parser.add_argument('--list', action='store_true',
                        help='List all available lotteries')

    parser.add_argument('--output', type=str, default='data/raw',
                        help='Output directory (default: data/raw)')

    args = parser.parse_args()

    # List available lotteries
    if args.list:
        print("\nAvailable NLB Lotteries:")
        for game, config in NLBScraper.LOTTERIES.items():
            print(f"  - {game:<25} ({config['name']})")

        print("\nAvailable DLB Lotteries:")
        for game, config in DLBScraper.LOTTERIES.items():
            print(f"  - {game:<25} ({config['name']})")

        return

    # Create scraper manager
    manager = ScraperManager(output_dir=args.output)

    # Scrape all lotteries
    if args.all:
        manager.scrape_all_lotteries(save_individual=True)
        manager.generate_summary_report()

    # Scrape single lottery
    elif args.source and args.game:
        manager.scrape_single_lottery(args.source, args.game, save=True)

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()

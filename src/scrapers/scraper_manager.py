"""
Scraper Manager
Orchestrates data collection from all 18 Sri Lankan lotteries (9 NLB + 9 DLB)
"""

import csv
import os
import time
from datetime import datetime
from typing import List, Dict

from .nlb_scraper import NLBScraper
from .dlb_scraper import DLBScraper


class ScraperManager:
    """Manages scraping operations for all lotteries"""

    def __init__(self, output_dir: str = "data/raw"):
        self.output_dir = output_dir
        self.nlb_scraper = NLBScraper()
        self.dlb_scraper = DLBScraper()

        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)

    def scrape_all_lotteries(self, save_individual: bool = True) -> Dict[str, List[Dict]]:
        """
        Scrape all 18 lotteries (9 NLB + 9 DLB)

        Args:
            save_individual: If True, save each lottery to a separate CSV

        Returns:
            Dictionary with lottery results
        """
        print("=" * 70)
        print("Sri Lankan Lottery Data Collection")
        print("Scraping 18 lotteries (9 NLB + 9 DLB)")
        print("=" * 70)

        all_results = {}
        total_draws = 0

        # Scrape NLB lotteries
        print("\n[1/2] Scraping NLB Lotteries...")
        print("-" * 70)
        for game in self.nlb_scraper.LOTTERIES:
            try:
                results = self.nlb_scraper.scrape_game(game)
                all_results[f"nlb_{game}"] = results
                total_draws += len(results)

                if save_individual and results:
                    self._save_to_csv(results, f"nlb_{game}.csv")

                # Rate limiting
                time.sleep(1)

            except Exception as e:
                print(f"  ERROR: Failed to scrape {game}: {e}")
                all_results[f"nlb_{game}"] = []

        # Scrape DLB lotteries
        print("\n[2/2] Scraping DLB Lotteries...")
        print("-" * 70)
        for game in self.dlb_scraper.LOTTERIES:
            try:
                results = self.dlb_scraper.scrape_game(game)
                all_results[f"dlb_{game}"] = results
                total_draws += len(results)

                if save_individual and results:
                    self._save_to_csv(results, f"dlb_{game}.csv")

                # Rate limiting
                time.sleep(1)

            except Exception as e:
                print(f"  ERROR: Failed to scrape {game}: {e}")
                all_results[f"dlb_{game}"] = []

        # Summary
        print("\n" + "=" * 70)
        print("SCRAPING COMPLETE")
        print("=" * 70)
        print(f"Total lotteries scraped: {len(all_results)}")
        print(f"Total draws collected: {total_draws}")
        print(f"Output directory: {os.path.abspath(self.output_dir)}")
        print("=" * 70)

        return all_results

    def scrape_single_lottery(self, source: str, game: str, save: bool = True) -> List[Dict]:
        """
        Scrape a single lottery

        Args:
            source: 'nlb' or 'dlb'
            game: Game key (e.g., 'mahajana_sampatha')
            save: Whether to save to CSV

        Returns:
            List of draw results
        """
        if source.lower() == 'nlb':
            results = self.nlb_scraper.scrape_game(game)
            filename = f"nlb_{game}.csv"
        elif source.lower() == 'dlb':
            results = self.dlb_scraper.scrape_game(game)
            filename = f"dlb_{game}.csv"
        else:
            raise ValueError(f"Unknown source: {source}. Use 'nlb' or 'dlb'")

        if save and results:
            self._save_to_csv(results, filename)

        return results

    def _save_to_csv(self, data: List[Dict], filename: str) -> None:
        """Save lottery data to CSV file"""
        if not data:
            print(f"  No data to save for {filename}")
            return

        filepath = os.path.join(self.output_dir, filename)

        # Get all unique keys from all records
        keys = sorted(set(k for record in data for k in record.keys()))

        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)

        print(f"  Saved {len(data)} draws to {filepath}")

    def generate_summary_report(self) -> None:
        """Generate a summary report of collected data"""
        print("\nGenerating data collection summary...")

        csv_files = [f for f in os.listdir(self.output_dir) if f.endswith('.csv')]

        if not csv_files:
            print("No data files found!")
            return

        summary = []
        total_draws = 0

        for csv_file in sorted(csv_files):
            filepath = os.path.join(self.output_dir, csv_file)

            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = list(reader)

                if rows:
                    lottery_name = rows[0].get('game_name', csv_file)
                    draw_count = len(rows)
                    total_draws += draw_count

                    # Get date range
                    dates = [r.get('draw_date') for r in rows if r.get('draw_date')]
                    if dates:
                        min_date = min(dates)
                        max_date = max(dates)
                        date_range = f"{min_date} to {max_date}"
                    else:
                        date_range = "N/A"

                    summary.append({
                        'Lottery': lottery_name,
                        'Draws': draw_count,
                        'Date Range': date_range,
                        'File': csv_file
                    })

        # Print summary table
        print("\n" + "=" * 100)
        print("DATA COLLECTION SUMMARY")
        print("=" * 100)
        print(f"{'Lottery':<30} {'Draws':<10} {'Date Range':<30} {'File':<30}")
        print("-" * 100)

        for row in summary:
            print(f"{row['Lottery']:<30} {row['Draws']:<10} {row['Date Range']:<30} {row['File']:<30}")

        print("-" * 100)
        print(f"{'TOTAL':<30} {total_draws:<10}")
        print("=" * 100)

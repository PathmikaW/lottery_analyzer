"""
Data Validator for lottery datasets.

Validates data quality, checks for missing values, duplicates, and outliers.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime, timedelta


class DataValidator:
    """Validates lottery data for quality and consistency."""

    # Expected number ranges for each lottery type
    NLB_RANGES = {
        'mahajana_sampatha': (0, 80),  # 6 numbers from 0-80
        'govisetha': (0, 60),  # 5 numbers from 0-60
        'dhana_nidhanaya': (0, 80),  # 6 numbers from 0-80
        'handahana': (0, 40),  # 4 numbers from 0-40
        'mega_power': (0, 45),  # 6 numbers from 0-45
        'ada_sampatha': (0, 49),  # 5 numbers from 0-49
        'suba_dawasak': (0, 70),  # 5 numbers from 0-70
        'nlb_jaya': (0, 80),  # 6 numbers from 0-80
    }

    DLB_RANGES = {
        'shanida': (0, 80),  # 5 numbers from 0-80
        'lagna_wasana': (0, 80),  # 5 numbers from 0-80
        'super_ball': (0, 80),  # 4 numbers from 0-80
        'jayoda': (0, 80),  # 4 numbers from 0-80
        'ada_kotipathi': (0, 80),  # 5 numbers from 0-80
        'kapruka': (0, 80),  # 5 numbers from 0-80
        'sasiri': (0, 40),  # 3 numbers from 0-40
        'supiri_dhana_sampatha': (0, 80),  # 6 numbers from 0-80
        'jaya_sampatha': (0, 80),  # 4 numbers from 0-80
    }

    def __init__(self, data_dir: str = 'data/raw'):
        """
        Initialize the data validator.

        Args:
            data_dir: Directory containing raw CSV files
        """
        self.data_dir = Path(data_dir)
        self.validation_results = {}

    def validate_all(self) -> Dict:
        """
        Validate all lottery CSV files in the data directory.

        Returns:
            Dictionary with validation results for each lottery
        """
        print("="*70)
        print("DATA VALIDATION REPORT")
        print("="*70)

        csv_files = list(self.data_dir.glob('*.csv'))
        # Exclude prize files
        csv_files = [f for f in csv_files if '_with_prizes' not in f.name]

        for csv_file in sorted(csv_files):
            lottery_name = csv_file.stem  # e.g., 'nlb_mahajana_sampatha'
            print(f"\nValidating {lottery_name}...")

            try:
                df = pd.read_csv(csv_file)
                result = self._validate_lottery(df, lottery_name)
                self.validation_results[lottery_name] = result

                self._print_lottery_report(lottery_name, result)

            except Exception as e:
                print(f"  [ERROR] Failed to validate: {e}")
                self.validation_results[lottery_name] = {'error': str(e)}

        self._print_summary()
        return self.validation_results

    def _validate_lottery(self, df: pd.DataFrame, lottery_name: str) -> Dict:
        """
        Validate a single lottery dataset.

        Args:
            df: DataFrame containing lottery data
            lottery_name: Name of the lottery

        Returns:
            Dictionary with validation results
        """
        result = {
            'total_rows': len(df),
            'date_range': self._check_date_range(df),
            'missing_values': self._check_missing_values(df),
            'duplicates': self._check_duplicates(df),
            'number_ranges': self._check_number_ranges(df, lottery_name),
            'date_gaps': self._check_date_gaps(df),
            'status': 'pass'
        }

        # Determine overall status
        if result['duplicates']['count'] > 0:
            result['status'] = 'warning'
        if result['missing_values']['critical_missing'] > 0:
            result['status'] = 'fail'
        if not result['number_ranges']['valid']:
            result['status'] = 'fail'

        return result

    def _check_date_range(self, df: pd.DataFrame) -> Dict:
        """Check date range coverage."""
        df['draw_date'] = pd.to_datetime(df['draw_date'])

        return {
            'min_date': df['draw_date'].min().strftime('%Y-%m-%d'),
            'max_date': df['draw_date'].max().strftime('%Y-%m-%d'),
            'total_days': (df['draw_date'].max() - df['draw_date'].min()).days
        }

    def _check_missing_values(self, df: pd.DataFrame) -> Dict:
        """Check for missing values in critical columns."""
        critical_cols = ['draw_date', 'draw_id', 'numbers']
        optional_cols = ['letter']

        critical_missing = df[critical_cols].isnull().sum().sum()
        optional_missing = df[optional_cols].isnull().sum().sum() if 'letter' in df.columns else 0

        return {
            'critical_missing': int(critical_missing),
            'optional_missing': int(optional_missing),
            'total_missing': int(df.isnull().sum().sum())
        }

    def _check_duplicates(self, df: pd.DataFrame) -> Dict:
        """Check for duplicate draws."""
        # Duplicate draw IDs
        dup_ids = df['draw_id'].duplicated().sum()

        # Duplicate dates
        dup_dates = df['draw_date'].duplicated().sum()

        # Duplicate draw_id + numbers combination
        dup_complete = df.duplicated(subset=['draw_id', 'numbers']).sum()

        return {
            'count': int(dup_complete),
            'duplicate_ids': int(dup_ids),
            'duplicate_dates': int(dup_dates)
        }

    def _check_number_ranges(self, df: pd.DataFrame, lottery_name: str) -> Dict:
        """Validate that numbers are within expected ranges."""
        # Extract lottery type and name
        parts = lottery_name.split('_', 1)
        source = parts[0]  # 'nlb' or 'dlb'
        game = parts[1] if len(parts) > 1 else lottery_name

        # Get expected range
        if source == 'nlb':
            expected_range = self.NLB_RANGES.get(game, (0, 80))
        else:
            expected_range = self.DLB_RANGES.get(game, (0, 80))

        # Parse numbers and check ranges
        invalid_count = 0
        out_of_range = []

        for idx, row in df.iterrows():
            numbers_str = str(row['numbers'])
            try:
                numbers = [int(n) for n in numbers_str.split(';')]
                for num in numbers:
                    if num < expected_range[0] or num > expected_range[1]:
                        invalid_count += 1
                        out_of_range.append((idx, num))
                        break  # Only count once per row
            except:
                invalid_count += 1

        return {
            'valid': invalid_count == 0,
            'expected_range': expected_range,
            'invalid_count': invalid_count,
            'sample_errors': out_of_range[:5]  # First 5 errors
        }

    def _check_date_gaps(self, df: pd.DataFrame) -> Dict:
        """Check for gaps in draw dates."""
        df_sorted = df.sort_values('draw_date').copy()
        df_sorted['draw_date'] = pd.to_datetime(df_sorted['draw_date'])

        # Calculate gaps between consecutive draws
        df_sorted['date_diff'] = df_sorted['draw_date'].diff().dt.days

        # Find large gaps (> 14 days)
        large_gaps = df_sorted[df_sorted['date_diff'] > 14]

        return {
            'max_gap_days': int(df_sorted['date_diff'].max()) if len(df_sorted) > 1 else 0,
            'mean_gap_days': float(df_sorted['date_diff'].mean()) if len(df_sorted) > 1 else 0,
            'large_gaps_count': len(large_gaps),
            'large_gaps': large_gaps[['draw_date', 'date_diff']].head(3).to_dict('records') if len(large_gaps) > 0 else []
        }

    def _print_lottery_report(self, lottery_name: str, result: Dict):
        """Print validation report for a single lottery."""
        if 'error' in result:
            print(f"  [ERROR] {result['error']}")
            return

        status_symbol = {
            'pass': '[PASS]',
            'warning': '[WARN]',
            'fail': '[FAIL]'
        }[result['status']]

        print(f"  {status_symbol} {result['total_rows']} draws")
        print(f"    Date range: {result['date_range']['min_date']} to {result['date_range']['max_date']}")
        print(f"    Missing values: {result['missing_values']['critical_missing']} critical, {result['missing_values']['optional_missing']} optional")
        print(f"    Duplicates: {result['duplicates']['count']} complete, {result['duplicates']['duplicate_dates']} dates")
        print(f"    Number range: {result['number_ranges']['expected_range']} - {result['number_ranges']['invalid_count']} invalid")
        print(f"    Date gaps: max {result['date_gaps']['max_gap_days']} days, {result['date_gaps']['large_gaps_count']} large gaps (>14 days)")

    def _print_summary(self):
        """Print overall validation summary."""
        print("\n" + "="*70)
        print("VALIDATION SUMMARY")
        print("="*70)

        total_lotteries = len(self.validation_results)
        pass_count = sum(1 for r in self.validation_results.values() if r.get('status') == 'pass')
        warn_count = sum(1 for r in self.validation_results.values() if r.get('status') == 'warning')
        fail_count = sum(1 for r in self.validation_results.values() if r.get('status') == 'fail')
        error_count = sum(1 for r in self.validation_results.values() if 'error' in r)

        total_draws = sum(r.get('total_rows', 0) for r in self.validation_results.values())

        print(f"\nTotal lotteries validated: {total_lotteries}")
        print(f"  [PASS]: {pass_count}")
        print(f"  [WARN]: {warn_count}")
        print(f"  [FAIL]: {fail_count}")
        print(f"  [ERROR]: {error_count}")
        print(f"\nTotal draws: {total_draws:,}")

    def save_report(self, output_path: str = 'outputs/validation_report.txt'):
        """Save validation report to file."""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w') as f:
            f.write("="*70 + "\n")
            f.write("DATA VALIDATION REPORT\n")
            f.write("="*70 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            for lottery_name, result in sorted(self.validation_results.items()):
                f.write(f"\n{lottery_name}:\n")
                f.write(f"  Status: {result.get('status', 'error')}\n")
                if 'error' in result:
                    f.write(f"  Error: {result['error']}\n")
                else:
                    f.write(f"  Total rows: {result['total_rows']}\n")
                    f.write(f"  Date range: {result['date_range']['min_date']} to {result['date_range']['max_date']}\n")
                    f.write(f"  Missing values: {result['missing_values']}\n")
                    f.write(f"  Duplicates: {result['duplicates']}\n")
                    f.write(f"  Number ranges: {result['number_ranges']}\n")
                    f.write(f"  Date gaps: {result['date_gaps']}\n")

        print(f"\nValidation report saved to: {output_path}")


if __name__ == '__main__':
    validator = DataValidator('data/raw')
    results = validator.validate_all()
    validator.save_report()

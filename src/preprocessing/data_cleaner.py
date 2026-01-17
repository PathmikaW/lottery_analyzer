"""
Data Cleaner for lottery datasets.

Standardizes formats, handles missing values, and prepares data for feature engineering.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List
from datetime import datetime


class DataCleaner:
    """Cleans and standardizes lottery data."""

    def __init__(self, input_dir: str = 'data/raw', output_dir: str = 'data/processed'):
        """
        Initialize the data cleaner.

        Args:
            input_dir: Directory containing raw CSV files
            output_dir: Directory to save cleaned data
        """
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def clean_all(self):
        """Clean all lottery CSV files."""
        print("="*70)
        print("DATA CLEANING")
        print("="*70)

        csv_files = list(self.input_dir.glob('*.csv'))
        # Exclude prize files
        csv_files = [f for f in csv_files if '_with_prizes' not in f.name]

        cleaned_count = 0

        for csv_file in sorted(csv_files):
            lottery_name = csv_file.stem
            print(f"\nCleaning {lottery_name}...")

            try:
                df = pd.read_csv(csv_file)
                df_cleaned = self._clean_lottery(df, lottery_name)

                # Save cleaned data
                output_path = self.output_dir / f"{lottery_name}_cleaned.csv"
                df_cleaned.to_csv(output_path, index=False)

                print(f"  [OK] Cleaned {len(df)} -> {len(df_cleaned)} rows")
                print(f"  [OK] Saved to {output_path}")
                cleaned_count += 1

            except Exception as e:
                print(f"  [ERROR] Failed to clean: {e}")

        print(f"\n" + "="*70)
        print(f"Cleaned {cleaned_count}/{len(csv_files)} lotteries")
        print("="*70)

    def _clean_lottery(self, df: pd.DataFrame, lottery_name: str) -> pd.DataFrame:
        """
        Clean a single lottery dataset.

        Args:
            df: DataFrame containing lottery data
            lottery_name: Name of the lottery

        Returns:
            Cleaned DataFrame
        """
        df_clean = df.copy()

        # 1. Standardize date format
        df_clean = self._standardize_dates(df_clean)

        # 2. Parse and validate numbers
        df_clean = self._parse_numbers(df_clean)

        # 3. Remove duplicates
        df_clean = self._remove_duplicates(df_clean)

        # 4. Handle missing values
        df_clean = self._handle_missing_values(df_clean)

        # 5. Sort by date (oldest first)
        df_clean = df_clean.sort_values('draw_date').reset_index(drop=True)

        # 6. Add draw sequence number
        df_clean['draw_sequence'] = range(1, len(df_clean) + 1)

        return df_clean

    def _standardize_dates(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Standardize date formats to YYYY-MM-DD.

        Args:
            df: DataFrame with draw_date column

        Returns:
            DataFrame with standardized dates
        """
        df_clean = df.copy()

        # Convert to datetime
        df_clean['draw_date'] = pd.to_datetime(df_clean['draw_date'], errors='coerce')

        # Remove rows with invalid dates
        invalid_dates = df_clean['draw_date'].isnull().sum()
        if invalid_dates > 0:
            print(f"    Removing {invalid_dates} rows with invalid dates")
            df_clean = df_clean[df_clean['draw_date'].notnull()]

        # Convert back to string format (YYYY-MM-DD)
        df_clean['draw_date'] = df_clean['draw_date'].dt.strftime('%Y-%m-%d')

        return df_clean

    def _parse_numbers(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Parse and validate winning numbers.

        Args:
            df: DataFrame with numbers column

        Returns:
            DataFrame with validated numbers
        """
        df_clean = df.copy()

        # Ensure numbers are properly formatted (semicolon-separated)
        def validate_numbers(numbers_str):
            try:
                # Split and convert to integers
                numbers = [int(n.strip()) for n in str(numbers_str).split(';')]
                # Re-format with zero-padding
                return ';'.join([f"{n:02d}" for n in numbers])
            except:
                return None

        df_clean['numbers'] = df_clean['numbers'].apply(validate_numbers)

        # Remove rows with invalid numbers
        invalid_numbers = df_clean['numbers'].isnull().sum()
        if invalid_numbers > 0:
            print(f"    Removing {invalid_numbers} rows with invalid numbers")
            df_clean = df_clean[df_clean['numbers'].notnull()]

        return df_clean

    def _remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Remove duplicate draws based on draw_id and numbers.

        Args:
            df: DataFrame

        Returns:
            DataFrame without duplicates
        """
        df_clean = df.copy()

        # Remove exact duplicates (draw_id + numbers)
        before_count = len(df_clean)
        df_clean = df_clean.drop_duplicates(subset=['draw_id', 'numbers'], keep='first')
        after_count = len(df_clean)

        if before_count != after_count:
            print(f"    Removed {before_count - after_count} duplicate draws")

        return df_clean

    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Handle missing values in the dataset.

        Args:
            df: DataFrame

        Returns:
            DataFrame with handled missing values
        """
        df_clean = df.copy()

        # Fill missing letters with empty string (some lotteries don't have letters)
        if 'letter' in df_clean.columns:
            df_clean['letter'] = df_clean['letter'].fillna('')

        # Critical columns should not have missing values
        # If they do, remove those rows
        critical_cols = ['draw_date', 'draw_id', 'numbers']
        missing_critical = df_clean[critical_cols].isnull().any(axis=1).sum()

        if missing_critical > 0:
            print(f"    Removing {missing_critical} rows with missing critical data")
            df_clean = df_clean.dropna(subset=critical_cols)

        return df_clean

    def generate_cleaning_report(self):
        """Generate a report comparing raw vs cleaned data."""
        print("\n" + "="*70)
        print("CLEANING REPORT")
        print("="*70)

        raw_files = list(self.input_dir.glob('*.csv'))
        raw_files = [f for f in raw_files if '_with_prizes' not in f.name]

        total_raw = 0
        total_cleaned = 0

        print(f"\n{'Lottery':<30} {'Raw':<10} {'Cleaned':<10} {'Removed':<10}")
        print("-"*70)

        for raw_file in sorted(raw_files):
            lottery_name = raw_file.stem
            cleaned_file = self.output_dir / f"{lottery_name}_cleaned.csv"

            if cleaned_file.exists():
                raw_count = len(pd.read_csv(raw_file))
                cleaned_count = len(pd.read_csv(cleaned_file))
                removed = raw_count - cleaned_count

                total_raw += raw_count
                total_cleaned += cleaned_count

                print(f"{lottery_name:<30} {raw_count:<10} {cleaned_count:<10} {removed:<10}")

        print("-"*70)
        print(f"{'TOTAL':<30} {total_raw:<10} {total_cleaned:<10} {total_raw - total_cleaned:<10}")
        print("="*70)


if __name__ == '__main__':
    cleaner = DataCleaner('data/raw', 'data/processed')
    cleaner.clean_all()
    cleaner.generate_cleaning_report()

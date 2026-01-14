"""
Feature Engineering for lottery prediction.

Generates 20-25 features from raw lottery data for ML model training.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List


class FeatureEngineer:
    """
    Engineer features from lottery draw data.

    Features created:
    - Frequency features (6): appearances in last N draws
    - Temporal features (5): date-based features
    - Statistical features (5): gap analysis
    - Hot/Cold features (4): temperature scoring
    """

    def __init__(self, input_dir: str = 'data/processed', output_dir: str = 'data/processed'):
        """
        Initialize the feature engineer.

        Args:
            input_dir: Directory containing cleaned CSV files
            output_dir: Directory to save featured data
        """
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)

    def engineer_all(self):
        """Engineer features for all lottery datasets."""
        print("="*70)
        print("FEATURE ENGINEERING")
        print("="*70)

        csv_files = list(self.input_dir.glob('*_cleaned.csv'))

        engineered_count = 0
        total_records = 0

        for csv_file in sorted(csv_files):
            lottery_name = csv_file.stem.replace('_cleaned', '')
            print(f"\nEngineering features for {lottery_name}...")

            try:
                df = pd.read_csv(csv_file)
                df_featured = self._engineer_lottery(df, lottery_name)

                # Save featured data
                output_path = self.output_dir / f"{lottery_name}_featured.csv"
                df_featured.to_csv(output_path, index=False)

                print(f"  [OK] Generated {len(df_featured)} records with {len(df_featured.columns)} columns")
                print(f"  [OK] Saved to {output_path}")

                engineered_count += 1
                total_records += len(df_featured)

            except Exception as e:
                print(f"  [ERROR] Failed to engineer features: {e}")
                import traceback
                traceback.print_exc()

        print(f"\n" + "="*70)
        print(f"Feature engineering complete:")
        print(f"  - Lotteries processed: {engineered_count}/{len(csv_files)}")
        print(f"  - Total records generated: {total_records:,}")
        print("="*70)

    def _engineer_lottery(self, df: pd.DataFrame, lottery_name: str) -> pd.DataFrame:
        """
        Engineer features for a single lottery.

        Args:
            df: Cleaned lottery DataFrame
            lottery_name: Name of the lottery

        Returns:
            DataFrame with engineered features
        """
        # Parse numbers into a list column for easier processing
        df['numbers_list'] = df['numbers'].apply(lambda x: [int(n) for n in str(x).split(';')])

        # Get unique numbers from this lottery
        all_numbers = set()
        for nums in df['numbers_list']:
            all_numbers.update(nums)

        all_numbers = sorted(list(all_numbers))
        print(f"    Found {len(all_numbers)} unique numbers: {min(all_numbers)}-{max(all_numbers)}")

        # Create one row per number per draw
        # This transforms each draw into multiple rows (one for each possible number)
        records = []

        for idx, row in df.iterrows():
            draw_date = pd.to_datetime(row['draw_date'])
            draw_id = row['draw_id']
            draw_sequence = row['draw_sequence']
            winning_numbers = set(row['numbers_list'])

            # Create a record for each possible number
            for number in all_numbers:
                # Target variable: did this number appear in this draw?
                appeared = 1 if number in winning_numbers else 0

                # Add basic info
                record = {
                    'lottery': lottery_name,
                    'draw_date': row['draw_date'],
                    'draw_id': draw_id,
                    'draw_sequence': draw_sequence,
                    'number': number,
                    'appeared': appeared  # Target variable
                }

                records.append(record)

        # Convert to DataFrame
        df_expanded = pd.DataFrame(records)
        df_expanded['draw_date'] = pd.to_datetime(df_expanded['draw_date'])

        print(f"    Expanded to {len(df_expanded)} records (draws × numbers)")

        # Now engineer features for each number
        df_featured = self._add_all_features(df_expanded)

        return df_featured

    def _add_all_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add all feature categories to the DataFrame."""
        df_featured = df.copy()

        print(f"    Engineering frequency features...")
        df_featured = self._add_frequency_features(df_featured)

        print(f"    Engineering temporal features...")
        df_featured = self._add_temporal_features(df_featured)

        print(f"    Engineering statistical features...")
        df_featured = self._add_statistical_features(df_featured)

        print(f"    Engineering hot/cold features...")
        df_featured = self._add_hot_cold_features(df_featured)

        return df_featured

    def _add_frequency_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add frequency-based features.

        Features:
        1. frequency_last_10: Appearances in last 10 draws
        2. frequency_last_30: Appearances in last 30 draws
        3. frequency_last_50: Appearances in last 50 draws
        4. frequency_all_time: Total appearances so far
        5. appearance_rate: Percentage of all draws
        6. days_since_last: Days since last appearance
        """
        df_featured = df.copy()

        # Sort by number and draw sequence
        df_featured = df_featured.sort_values(['number', 'draw_sequence']).reset_index(drop=True)

        # For each number, calculate frequency features
        for window in [10, 30, 50]:
            col_name = f'frequency_last_{window}'
            df_featured[col_name] = (
                df_featured.groupby('number')['appeared']
                .rolling(window=window, min_periods=1)
                .sum()
                .shift(1)  # Shift to avoid data leakage
                .fillna(0)
                .reset_index(level=0, drop=True)
            )

        # All-time frequency (cumulative sum up to current draw)
        df_featured['frequency_all_time'] = (
            df_featured.groupby('number')['appeared']
            .cumsum()
            .shift(1)
            .fillna(0)
        )

        # Appearance rate (all-time frequency / draw sequence)
        df_featured['appearance_rate'] = (
            df_featured['frequency_all_time'] / df_featured['draw_sequence'].replace(0, 1)
        )

        # Days since last appearance
        df_featured['days_since_last'] = df_featured.groupby('number').apply(
            lambda group: self._calculate_days_since_last(group)
        ).reset_index(level=0, drop=True)

        return df_featured

    def _calculate_days_since_last(self, group: pd.DataFrame) -> pd.Series:
        """Calculate days since last appearance for a number."""
        days_since = []
        last_appearance_date = None

        for idx, row in group.iterrows():
            if last_appearance_date is None:
                # First occurrence or never appeared yet
                days_since.append(999)  # Large default value
            else:
                days_diff = (row['draw_date'] - last_appearance_date).days
                days_since.append(days_diff)

            # Update last appearance if this number appeared
            if row['appeared'] == 1:
                last_appearance_date = row['draw_date']

        return pd.Series(days_since, index=group.index)

    def _add_temporal_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add temporal features.

        Features:
        7. day_of_week: Monday(0) to Sunday(6)
        8. is_weekend: Binary (Saturday/Sunday = 1)
        9. month: 1-12
        10. week_of_year: 1-52
        11. draw_sequence: Already exists from cleaning
        """
        df_featured = df.copy()

        df_featured['day_of_week'] = df_featured['draw_date'].dt.dayofweek
        df_featured['is_weekend'] = (df_featured['day_of_week'] >= 5).astype(int)
        df_featured['month'] = df_featured['draw_date'].dt.month
        df_featured['week_of_year'] = df_featured['draw_date'].dt.isocalendar().week

        return df_featured

    def _add_statistical_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add statistical gap features.

        Features:
        12. mean_gap: Average days between appearances
        13. std_gap: Standard deviation of gaps
        14. min_gap: Minimum gap
        15. max_gap: Maximum gap
        16. current_gap: Same as days_since_last
        """
        df_featured = df.copy()

        # Calculate gaps for each number
        df_featured = df_featured.sort_values(['number', 'draw_sequence']).reset_index(drop=True)

        # Initialize gap statistic columns
        df_featured['mean_gap'] = 0.0
        df_featured['std_gap'] = 0.0
        df_featured['min_gap'] = 0.0
        df_featured['max_gap'] = 0.0

        # Calculate for each number
        for number in df_featured['number'].unique():
            number_mask = df_featured['number'] == number
            number_df = df_featured[number_mask].copy()

            # Get appearances
            appearances = number_df[number_df['appeared'] == 1]

            if len(appearances) < 2:
                continue  # Keep defaults

            # Calculate gaps between consecutive appearances
            appearance_dates = appearances['draw_date'].values
            gaps = []
            for i in range(1, len(appearance_dates)):
                gap = (pd.to_datetime(appearance_dates[i]) -
                       pd.to_datetime(appearance_dates[i-1])).days
                gaps.append(gap)

            # For each row, calculate stats based on history up to that point
            for idx in number_df.index:
                draw_seq = number_df.loc[idx, 'draw_sequence']

                # Get gaps from appearances before this draw
                past_apps = appearances[appearances['draw_sequence'] < draw_seq]

                if len(past_apps) < 2:
                    continue

                past_dates = past_apps['draw_date'].values
                past_gaps = []
                for i in range(1, len(past_dates)):
                    gap = (pd.to_datetime(past_dates[i]) -
                           pd.to_datetime(past_dates[i-1])).days
                    past_gaps.append(gap)

                if past_gaps:
                    df_featured.loc[idx, 'mean_gap'] = np.mean(past_gaps)
                    df_featured.loc[idx, 'std_gap'] = np.std(past_gaps) if len(past_gaps) > 1 else 0
                    df_featured.loc[idx, 'min_gap'] = np.min(past_gaps)
                    df_featured.loc[idx, 'max_gap'] = np.max(past_gaps)

        # Current gap is same as days_since_last
        df_featured['current_gap'] = df_featured['days_since_last']

        return df_featured

    def _calculate_gap_statistics(self, group: pd.DataFrame) -> pd.DataFrame:
        """Calculate gap statistics for a number."""
        stats = []

        for idx, row in group.iterrows():
            # Get all appearances up to this point
            past_appearances = group[
                (group['draw_sequence'] < row['draw_sequence']) &
                (group['appeared'] == 1)
            ]

            if len(past_appearances) < 2:
                # Not enough history
                stats.append({
                    'mean_gap': 0,
                    'std_gap': 0,
                    'min_gap': 0,
                    'max_gap': 0
                })
            else:
                # Calculate gaps between consecutive appearances
                appearance_dates = past_appearances['draw_date'].values
                gaps = []
                for i in range(1, len(appearance_dates)):
                    gap = (pd.to_datetime(appearance_dates[i]) -
                           pd.to_datetime(appearance_dates[i-1])).days
                    gaps.append(gap)

                stats.append({
                    'mean_gap': np.mean(gaps),
                    'std_gap': np.std(gaps) if len(gaps) > 1 else 0,
                    'min_gap': np.min(gaps),
                    'max_gap': np.max(gaps)
                })

        stats_df = pd.DataFrame(stats, index=group.index)
        stats_df['number'] = group['number'].values
        stats_df['draw_sequence'] = group['draw_sequence'].values

        return stats_df

    def _add_hot_cold_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add hot/cold temperature features.

        Features:
        17. is_hot: Binary (top 20% frequency in last 30 draws)
        18. is_cold: Binary (bottom 20% frequency in last 30 draws)
        19. temperature_score: Normalized 0-100
        20. trend: Categorical (heating_up/cooling_down/stable)
        """
        df_featured = df.copy()

        # Calculate temperature score (0-100) based on last 30 draws
        # Higher frequency = higher temperature
        max_possible = 30  # Maximum appearances in last 30 draws
        df_featured['temperature_score'] = (
            (df_featured['frequency_last_30'] / max_possible * 100)
            .fillna(0)
        )

        # Hot: top 20% (temperature >= 80th percentile)
        # Cold: bottom 20% (temperature <= 20th percentile)
        # Calculate percentiles per draw
        df_featured['is_hot'] = df_featured.groupby('draw_sequence')['temperature_score'].transform(
            lambda x: (x >= x.quantile(0.80)).astype(int)
        )

        df_featured['is_cold'] = df_featured.groupby('draw_sequence')['temperature_score'].transform(
            lambda x: (x <= x.quantile(0.20)).astype(int)
        )

        # Trend: compare frequency_last_10 with frequency_last_30
        def categorize_trend(row):
            if row['frequency_last_10'] == 0 and row['frequency_last_30'] == 0:
                return 'stable'
            elif row['frequency_last_10'] / 10 > row['frequency_last_30'] / 30:
                return 'heating_up'
            elif row['frequency_last_10'] / 10 < row['frequency_last_30'] / 30:
                return 'cooling_down'
            else:
                return 'stable'

        df_featured['trend'] = df_featured.apply(categorize_trend, axis=1)

        return df_featured


if __name__ == '__main__':
    engineer = FeatureEngineer('data/processed', 'data/processed')
    engineer.engineer_all()

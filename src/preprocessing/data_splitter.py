"""
Data Splitter for lottery datasets.

Splits data into train/validation/test sets with stratification to maintain class balance.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
import json
from typing import Dict, Tuple


class DataSplitter:
    """
    Split lottery datasets into train/validation/test sets.

    Uses stratified splitting to maintain class balance across splits.
    """

    def __init__(
        self,
        input_dir: str = 'data/processed',
        output_dir: str = 'data/splits',
        train_ratio: float = 0.70,
        val_ratio: float = 0.15,
        test_ratio: float = 0.15,
        random_state: int = 42
    ):
        """
        Initialize the data splitter.

        Args:
            input_dir: Directory containing featured CSV files
            output_dir: Directory to save split datasets
            train_ratio: Proportion for training set (default 0.70)
            val_ratio: Proportion for validation set (default 0.15)
            test_ratio: Proportion for test set (default 0.15)
            random_state: Random seed for reproducibility
        """
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        assert abs(train_ratio + val_ratio + test_ratio - 1.0) < 0.01, \
            "Train, val, and test ratios must sum to 1.0"

        self.train_ratio = train_ratio
        self.val_ratio = val_ratio
        self.test_ratio = test_ratio
        self.random_state = random_state

        self.split_stats = {}

    def split_all(self):
        """Split all featured lottery datasets."""
        print("="*70)
        print("DATA SPLITTING")
        print("="*70)
        print(f"Split ratios: Train={self.train_ratio}, Val={self.val_ratio}, Test={self.test_ratio}")
        print(f"Random state: {self.random_state}")
        print("="*70)

        csv_files = list(self.input_dir.glob('*_featured.csv'))

        split_count = 0

        for csv_file in sorted(csv_files):
            lottery_name = csv_file.stem.replace('_featured', '')
            print(f"\nSplitting {lottery_name}...")

            try:
                df = pd.read_csv(csv_file)
                splits = self._split_lottery(df, lottery_name)

                # Save splits
                for split_name, split_df in splits.items():
                    output_path = self.output_dir / f"{lottery_name}_{split_name}.csv"
                    split_df.to_csv(output_path, index=False)
                    print(f"  [OK] {split_name:5s}: {len(split_df):6d} records -> {output_path.name}")

                split_count += 1

            except Exception as e:
                print(f"  [ERROR] Failed to split: {e}")
                import traceback
                traceback.print_exc()

        print(f"\n" + "="*70)
        print(f"Splitting complete: {split_count}/{len(csv_files)} lotteries")
        print("="*70)

        # Save split statistics
        self._save_statistics()

    def _split_lottery(self, df: pd.DataFrame, lottery_name: str) -> Dict[str, pd.DataFrame]:
        """
        Split a single lottery dataset with stratification.

        Args:
            df: Featured lottery DataFrame
            lottery_name: Name of the lottery

        Returns:
            Dictionary with 'train', 'val', 'test' DataFrames
        """
        # Calculate class distribution
        class_dist = df['appeared'].value_counts()
        pos_count = class_dist.get(1, 0)
        neg_count = class_dist.get(0, 0)
        total = len(df)

        imbalance_ratio = neg_count / pos_count if pos_count > 0 else 0

        print(f"    Total: {total:,} records")
        print(f"    Positive (appeared=1): {pos_count:,} ({pos_count/total*100:.2f}%)")
        print(f"    Negative (appeared=0): {neg_count:,} ({neg_count/total*100:.2f}%)")
        print(f"    Imbalance ratio: 1:{imbalance_ratio:.2f}")

        # First split: train + val vs test
        train_val_df, test_df = train_test_split(
            df,
            test_size=self.test_ratio,
            stratify=df['appeared'],
            random_state=self.random_state
        )

        # Second split: train vs val
        # Adjust val_ratio to account for already removed test set
        val_ratio_adjusted = self.val_ratio / (self.train_ratio + self.val_ratio)

        train_df, val_df = train_test_split(
            train_val_df,
            test_size=val_ratio_adjusted,
            stratify=train_val_df['appeared'],
            random_state=self.random_state
        )

        # Store statistics
        self.split_stats[lottery_name] = {
            'total_records': total,
            'positive_count': int(pos_count),
            'negative_count': int(neg_count),
            'imbalance_ratio': float(imbalance_ratio),
            'positive_ratio': float(pos_count / total),
            'train_size': len(train_df),
            'val_size': len(val_df),
            'test_size': len(test_df),
            'train_positive': int((train_df['appeared'] == 1).sum()),
            'val_positive': int((val_df['appeared'] == 1).sum()),
            'test_positive': int((test_df['appeared'] == 1).sum())
        }

        return {
            'train': train_df,
            'val': val_df,
            'test': test_df
        }

    def _save_statistics(self):
        """Save split statistics to JSON file."""
        stats_output = {
            'split_config': {
                'train_ratio': self.train_ratio,
                'val_ratio': self.val_ratio,
                'test_ratio': self.test_ratio,
                'random_state': self.random_state
            },
            'lotteries': self.split_stats
        }

        # Calculate overall statistics
        total_records = sum(s['total_records'] for s in self.split_stats.values())
        total_positive = sum(s['positive_count'] for s in self.split_stats.values())
        total_negative = sum(s['negative_count'] for s in self.split_stats.values())

        stats_output['overall'] = {
            'total_records': total_records,
            'total_positive': total_positive,
            'total_negative': total_negative,
            'overall_imbalance_ratio': total_negative / total_positive if total_positive > 0 else 0,
            'overall_positive_ratio': total_positive / total_records if total_records > 0 else 0
        }

        output_path = Path('outputs/statistics/split_stats.json')
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w') as f:
            json.dump(stats_output, f, indent=2)

        print(f"\nSplit statistics saved to: {output_path}")

    def generate_split_report(self):
        """Generate a detailed report of data splits."""
        print("\n" + "="*70)
        print("DATA SPLIT REPORT")
        print("="*70)

        if not self.split_stats:
            # Load from JSON if not in memory
            stats_file = Path('outputs/statistics/split_stats.json')
            if stats_file.exists():
                with open(stats_file, 'r') as f:
                    stats = json.load(f)
                    self.split_stats = stats['lotteries']
            else:
                print("No split statistics found. Run split_all() first.")
                return

        print(f"\n{'Lottery':<30} {'Total':<10} {'Train':<10} {'Val':<10} {'Test':<10} {'Imb.Ratio':<12}")
        print("-"*90)

        for lottery_name, stats in sorted(self.split_stats.items()):
            print(f"{lottery_name:<30} "
                  f"{stats['total_records']:<10,} "
                  f"{stats['train_size']:<10,} "
                  f"{stats['val_size']:<10,} "
                  f"{stats['test_size']:<10,} "
                  f"1:{stats['imbalance_ratio']:<.2f}")

        # Overall statistics
        total_records = sum(s['total_records'] for s in self.split_stats.values())
        total_train = sum(s['train_size'] for s in self.split_stats.values())
        total_val = sum(s['val_size'] for s in self.split_stats.values())
        total_test = sum(s['test_size'] for s in self.split_stats.values())

        print("-"*90)
        print(f"{'TOTAL':<30} {total_records:<10,} {total_train:<10,} {total_val:<10,} {total_test:<10,}")

        # Class imbalance summary
        print("\n" + "="*70)
        print("CLASS IMBALANCE ANALYSIS")
        print("="*70)

        imbalance_ratios = [s['imbalance_ratio'] for s in self.split_stats.values()]

        print(f"\nImbalance Ratio Statistics:")
        print(f"  - Minimum: 1:{min(imbalance_ratios):.2f}")
        print(f"  - Maximum: 1:{max(imbalance_ratios):.2f}")
        print(f"  - Mean: 1:{np.mean(imbalance_ratios):.2f}")
        print(f"  - Median: 1:{np.median(imbalance_ratios):.2f}")

        print(f"\nRecommended XGBoost scale_pos_weight:")
        print(f"  - Conservative: {int(np.mean(imbalance_ratios))}")
        print(f"  - Median: {int(np.median(imbalance_ratios))}")

        print("\n" + "="*70)


if __name__ == '__main__':
    splitter = DataSplitter(
        input_dir='data/processed',
        output_dir='data/splits',
        train_ratio=0.70,
        val_ratio=0.15,
        test_ratio=0.15,
        random_state=42
    )

    splitter.split_all()
    splitter.generate_split_report()

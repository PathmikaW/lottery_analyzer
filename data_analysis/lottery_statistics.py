"""
Statistics Module
Calculates frequency distributions and statistical metrics for lottery data

"""

import numpy as np
from collections import Counter
import pandas as pd


def calculate_number_frequency(df):
    """
    Calculate frequency of each number across all draws

    Args:
        df (pd.DataFrame): Lottery dataframe with 'numbers_list' column

    Returns:
        dict: Frequency statistics
    """
    # Collect all numbers from all draws
    all_numbers = []
    for numbers_list in df['numbers_list']:
        all_numbers.extend(numbers_list)

    # Count frequencies
    frequency = Counter(all_numbers)
    total_occurrences = sum(frequency.values())

    # Sort by frequency
    sorted_freq = sorted(frequency.items(), key=lambda x: x[1], reverse=True)

    return {
        'frequency': dict(frequency),
        'most_common': sorted_freq[:10],
        'least_common': sorted_freq[-10:] if len(sorted_freq) >= 10 else sorted_freq,
        'total_draws': len(df),
        'total_occurrences': total_occurrences,
        'average_per_number': total_occurrences / len(frequency) if frequency else 0
    }


def calculate_letter_frequency(df):
    """
    Calculate frequency of each letter

    Args:
        df (pd.DataFrame): Lottery dataframe with 'letter' column

    Returns:
        dict: Letter frequency statistics
    """
    if 'letter' not in df.columns:
        return {}

    letter_counts = df['letter'].value_counts().to_dict()
    total = len(df)

    # Calculate percentages
    letter_percentages = {letter: (count/total)*100
                         for letter, count in letter_counts.items()}

    return {
        'frequency': letter_counts,
        'percentages': letter_percentages,
        'most_common': max(letter_counts.items(), key=lambda x: x[1]),
        'least_common': min(letter_counts.items(), key=lambda x: x[1]),
        'total_unique': len(letter_counts)
    }


def calculate_basic_statistics(df, column='numbers_list'):
    """
    Calculate basic statistical metrics

    Args:
        df (pd.DataFrame): Lottery dataframe
        column (str): Column to analyze

    Returns:
        dict: Statistical metrics
    """
    all_numbers = []
    for numbers_list in df[column]:
        all_numbers.extend(numbers_list)

    numbers_array = np.array(all_numbers)

    return {
        'mean': np.mean(numbers_array),
        'median': np.median(numbers_array),
        'mode': float(Counter(all_numbers).most_common(1)[0][0]),
        'std_dev': np.std(numbers_array),
        'variance': np.var(numbers_array),
        'min': np.min(numbers_array),
        'max': np.max(numbers_array),
        'range': np.max(numbers_array) - np.min(numbers_array),
        'total_count': len(all_numbers)
    }


def calculate_position_frequency(df):
    """
    Calculate frequency of numbers by their position in the draw

    Args:
        df (pd.DataFrame): Lottery dataframe

    Returns:
        dict: Position-based frequency
    """
    position_freq = {}

    # Get number of positions from first draw
    num_positions = len(df['numbers_list'].iloc[0])

    for pos in range(num_positions):
        position_numbers = df['numbers_list'].apply(
            lambda x: x[pos] if pos < len(x) else None
        ).dropna()

        position_freq[f'position_{pos+1}'] = dict(Counter(position_numbers))

    return position_freq


def calculate_odd_even_stats(df):
    """
    Calculate odd/even distribution statistics

    Args:
        df (pd.DataFrame): Lottery dataframe

    Returns:
        dict: Odd/even statistics
    """
    odd_counts = []
    even_counts = []

    for numbers_list in df['numbers_list']:
        odd = sum(1 for n in numbers_list if n % 2 == 1)
        even = len(numbers_list) - odd
        odd_counts.append(odd)
        even_counts.append(even)

    return {
        'avg_odd': np.mean(odd_counts),
        'avg_even': np.mean(even_counts),
        'most_common_ratio': f"{int(round(np.mean(odd_counts)))}:{int(round(np.mean(even_counts)))}",
        'odd_distribution': dict(Counter(odd_counts)),
        'even_distribution': dict(Counter(even_counts))
    }


def calculate_high_low_stats(df, threshold=5):
    """
    Calculate high/low number distribution

    Args:
        df (pd.DataFrame): Lottery dataframe
        threshold (int): Boundary between low and high numbers

    Returns:
        dict: High/low statistics
    """
    high_counts = []
    low_counts = []

    for numbers_list in df['numbers_list']:
        low = sum(1 for n in numbers_list if n < threshold)
        high = len(numbers_list) - low
        high_counts.append(high)
        low_counts.append(low)

    return {
        'threshold': threshold,
        'avg_low': np.mean(low_counts),
        'avg_high': np.mean(high_counts),
        'most_common_ratio': f"{int(round(np.mean(low_counts)))}:{int(round(np.mean(high_counts)))}",
        'low_distribution': dict(Counter(low_counts)),
        'high_distribution': dict(Counter(high_counts))
    }


def calculate_prize_statistics(df):
    """
    Calculate statistics for prize tiers

    Args:
        df (pd.DataFrame): Lottery dataframe with prize columns

    Returns:
        dict: Prize statistics
    """
    if '1_winners' not in df.columns:
        return {'error': 'No prize data available'}

    stats = {}

    # Find all prize tier prefixes
    tiers = set()
    for col in df.columns:
        if '_winners' in col:
            tier = col.replace('_winners', '')
            tiers.add(tier)

    for tier in tiers:
        winner_col = f'{tier}_winners'
        total_col = f'{tier}_total'
        prize_col = f'{tier}_prize'

        if winner_col in df.columns:
            stats[tier] = {
                'avg_winners': df[winner_col].mean(),
                'max_winners': df[winner_col].max(),
                'min_winners': df[winner_col].min(),
                'total_winners': df[winner_col].sum(),
                'std_winners': df[winner_col].std()
            }

            if total_col in df.columns:
                stats[tier]['avg_payout'] = df[total_col].mean()
                stats[tier]['total_payout'] = df[total_col].sum()

    return stats


def generate_summary_report(df):
    """
    Generate comprehensive summary statistics report

    Args:
        df (pd.DataFrame): Lottery dataframe

    Returns:
        dict: Complete summary statistics
    """
    summary = {
        'dataset_info': {
            'total_draws': len(df),
            'lottery_type': df['game'].iloc[0] if 'game' in df.columns else 'Unknown',
            'date_range': (str(df['draw_date'].min()), str(df['draw_date'].max()))
        },
        'number_frequency': calculate_number_frequency(df),
        'letter_frequency': calculate_letter_frequency(df),
        'basic_statistics': calculate_basic_statistics(df),
        'odd_even_stats': calculate_odd_even_stats(df),
        'high_low_stats': calculate_high_low_stats(df),
    }

    # Add prize statistics if available
    prize_stats = calculate_prize_statistics(df)
    if 'error' not in prize_stats:
        summary['prize_statistics'] = prize_stats

    return summary


def print_frequency_table(frequency_data, title="Number Frequency"):
    """
    Print formatted frequency table

    Args:
        frequency_data (dict): Frequency statistics
        title (str): Table title
    """
    print(f"\n{'='*60}")
    print(f"{title:^60}")
    print(f"{'='*60}")

    freq = frequency_data['frequency']
    sorted_items = sorted(freq.items(), key=lambda x: x[1], reverse=True)

    print(f"\n{'Number':<10} {'Frequency':<15} {'Percentage':<15}")
    print("-" * 40)

    total = sum(freq.values())
    for num, count in sorted_items[:15]:  # Top 15
        percentage = (count / total) * 100
        print(f"{num:<10} {count:<15} {percentage:>6.2f}%")

    print(f"\nTotal draws: {frequency_data['total_draws']}")
    print(f"Total occurrences: {frequency_data['total_occurrences']}")
    print(f"Average per number: {frequency_data['average_per_number']:.2f}")


if __name__ == "__main__":
    # Test the statistics module
    import sys
    from pathlib import Path

    # Add parent directory to path
    sys.path.insert(0, str(Path(__file__).parent))
    from data_loader import load_lottery_data

    # Test with Mahajana Sampatha
    data_path = Path(__file__).parent.parent / "datasets" / "nlb_mahajana_with_prizes.csv"

    if data_path.exists():
        print("Testing Statistics Module...")
        print("=" * 60)

        # Load data
        df = load_lottery_data(data_path)

        # Calculate statistics
        print("\n1. NUMBER FREQUENCY ANALYSIS")
        num_freq = calculate_number_frequency(df)
        print_frequency_table(num_freq, "Number Frequency Distribution")

        print("\n\n2. LETTER FREQUENCY ANALYSIS")
        letter_freq = calculate_letter_frequency(df)
        print(f"Total unique letters: {letter_freq['total_unique']}")
        print(f"Most common: {letter_freq['most_common']}")
        print(f"Least common: {letter_freq['least_common']}")

        print("\n\n3. BASIC STATISTICS")
        basic_stats = calculate_basic_statistics(df)
        for key, value in basic_stats.items():
            print(f"{key.replace('_', ' ').title():<20}: {value:.2f}")

        print("\n\n4. ODD/EVEN ANALYSIS")
        odd_even = calculate_odd_even_stats(df)
        print(f"Average odd numbers: {odd_even['avg_odd']:.2f}")
        print(f"Average even numbers: {odd_even['avg_even']:.2f}")
        print(f"Most common ratio: {odd_even['most_common_ratio']}")

        print("\n\n5. HIGH/LOW ANALYSIS")
        high_low = calculate_high_low_stats(df, threshold=5)
        print(f"Threshold: {high_low['threshold']}")
        print(f"Average low (0-4): {high_low['avg_low']:.2f}")
        print(f"Average high (5-9): {high_low['avg_high']:.2f}")

        print("\n" + "="*60)
        print("[OK] Statistics module test complete")
    else:
        print(f"Dataset not found: {data_path}")

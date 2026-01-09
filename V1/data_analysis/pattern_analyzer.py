"""
Pattern Analyzer Module
Detects patterns and trends in lottery draws

"""

import numpy as np
from collections import Counter
import pandas as pd


def detect_hot_cold_numbers(df, window=30, hot_threshold=5, cold_threshold=2):
    """
    Detect hot and cold numbers based on recent draws

    Args:
        df (pd.DataFrame): Lottery dataframe
        window (int): Number of recent draws to analyze
        hot_threshold (int): Minimum occurrences to be "hot"
        cold_threshold (int): Maximum occurrences to be "cold"

    Returns:
        dict: Hot and cold numbers with statistics
    """
    # Get recent draws
    recent_draws = df.tail(window).copy()

    # Count all numbers in recent window
    all_numbers = []
    for numbers_list in recent_draws['numbers_list']:
        all_numbers.extend(numbers_list)

    frequency = Counter(all_numbers)

    # Classify as hot or cold
    hot_numbers = {num: count for num, count in frequency.items()
                   if count >= hot_threshold}
    cold_numbers = {num: count for num, count in frequency.items()
                    if count <= cold_threshold}

    return {
        'window_size': window,
        'hot_threshold': hot_threshold,
        'cold_threshold': cold_threshold,
        'hot_numbers': dict(sorted(hot_numbers.items(), key=lambda x: x[1], reverse=True)),
        'cold_numbers': dict(sorted(cold_numbers.items(), key=lambda x: x[1])),
        'frequency': dict(frequency),
        'total_hot': len(hot_numbers),
        'total_cold': len(cold_numbers)
    }


def analyze_consecutive_numbers(df):
    """
    Analyze consecutive number patterns in draws

    Args:
        df (pd.DataFrame): Lottery dataframe

    Returns:
        dict: Consecutive number statistics
    """
    consecutive_counts = []
    draws_with_consecutive = 0

    for numbers_list in df['numbers_list']:
        sorted_nums = sorted(numbers_list)
        consecutive = 0

        for i in range(len(sorted_nums) - 1):
            if sorted_nums[i+1] - sorted_nums[i] == 1:
                consecutive += 1

        consecutive_counts.append(consecutive)
        if consecutive > 0:
            draws_with_consecutive += 1

    return {
        'total_draws': len(df),
        'draws_with_consecutive': draws_with_consecutive,
        'percentage_with_consecutive': (draws_with_consecutive / len(df)) * 100,
        'avg_consecutive_pairs': np.mean(consecutive_counts),
        'max_consecutive_pairs': max(consecutive_counts),
        'distribution': dict(Counter(consecutive_counts))
    }


def analyze_repeating_numbers(df):
    """
    Analyze numbers that repeat in consecutive draws

    Args:
        df (pd.DataFrame): Lottery dataframe

    Returns:
        dict: Repeating number statistics
    """
    repeaters = []
    repeat_counts = []

    for i in range(1, len(df)):
        prev_numbers = set(df['numbers_list'].iloc[i-1])
        curr_numbers = set(df['numbers_list'].iloc[i])

        common = prev_numbers.intersection(curr_numbers)
        repeaters.extend(common)
        repeat_counts.append(len(common))

    return {
        'total_comparisons': len(repeat_counts),
        'avg_repeats_per_draw': np.mean(repeat_counts),
        'max_repeats': max(repeat_counts) if repeat_counts else 0,
        'most_common_repeaters': Counter(repeaters).most_common(10),
        'distribution': dict(Counter(repeat_counts))
    }


def analyze_odd_even_patterns(df):
    """
    Analyze odd/even patterns in each draw

    Args:
        df (pd.DataFrame): Lottery dataframe

    Returns:
        dict: Odd/even pattern analysis
    """
    patterns = []

    for numbers_list in df['numbers_list']:
        odd = sum(1 for n in numbers_list if n % 2 == 1)
        even = len(numbers_list) - odd
        pattern = f"{odd}:{even}"
        patterns.append(pattern)

    pattern_counts = Counter(patterns)

    return {
        'pattern_distribution': dict(pattern_counts),
        'most_common_pattern': pattern_counts.most_common(1)[0],
        'total_unique_patterns': len(pattern_counts),
        'expected_balanced': f"{len(df['numbers_list'].iloc[0])//2}:{len(df['numbers_list'].iloc[0])//2}"
    }


def analyze_sum_patterns(df):
    """
    Analyze sum of numbers in each draw

    Args:
        df (pd.DataFrame): Lottery dataframe

    Returns:
        dict: Sum pattern statistics
    """
    sums = [sum(numbers_list) for numbers_list in df['numbers_list']]

    return {
        'min_sum': min(sums),
        'max_sum': max(sums),
        'avg_sum': np.mean(sums),
        'median_sum': np.median(sums),
        'std_sum': np.std(sums),
        'sum_range': max(sums) - min(sums)
    }


def detect_number_gaps(df, window=10):
    """
    Detect numbers that haven't appeared recently (gaps)

    Args:
        df (pd.DataFrame): Lottery dataframe
        window (int): Number of recent draws

    Returns:
        dict: Gap analysis
    """
    recent_draws = df.tail(window)

    # Get all unique numbers that have appeared
    all_possible = set()
    for numbers_list in df['numbers_list']:
        all_possible.update(numbers_list)

    # Numbers in recent window
    recent_numbers = set()
    for numbers_list in recent_draws['numbers_list']:
        recent_numbers.update(numbers_list)

    # Find gaps (numbers not in recent window)
    gaps = all_possible - recent_numbers

    return {
        'window_size': window,
        'total_possible_numbers': len(all_possible),
        'numbers_in_window': len(recent_numbers),
        'gap_numbers': sorted(gaps),
        'total_gaps': len(gaps),
        'gap_percentage': (len(gaps) / len(all_possible)) * 100 if all_possible else 0
    }


def analyze_prize_winner_patterns(df):
    """
    Analyze patterns in prize winner distributions

    Args:
        df (pd.DataFrame): Lottery dataframe with prize columns

    Returns:
        dict: Prize winner pattern analysis
    """
    if '1_winners' not in df.columns:
        return {'error': 'No prize data available'}

    patterns = {}

    # Analyze jackpot winners
    if '1_winners' in df.columns:
        jackpot_wins = df[df['1_winners'] > 0]
        patterns['jackpot'] = {
            'total_wins': len(jackpot_wins),
            'win_percentage': (len(jackpot_wins) / len(df)) * 100,
            'avg_winners_when_won': jackpot_wins['1_winners'].mean() if len(jackpot_wins) > 0 else 0,
            'max_winners': df['1_winners'].max()
        }

    # Analyze total winner trends
    if 'super_prize_winners' in df.columns:
        patterns['super_prize'] = {
            'total_wins': (df['super_prize_winners'] > 0).sum(),
            'win_percentage': ((df['super_prize_winners'] > 0).sum() / len(df)) * 100
        }

    return patterns


def generate_pattern_report(df, window=30):
    """
    Generate comprehensive pattern analysis report

    Args:
        df (pd.DataFrame): Lottery dataframe
        window (int): Window size for hot/cold analysis

    Returns:
        dict: Complete pattern analysis
    """
    report = {
        'hot_cold': detect_hot_cold_numbers(df, window=window),
        'consecutive': analyze_consecutive_numbers(df),
        'repeating': analyze_repeating_numbers(df),
        'odd_even': analyze_odd_even_patterns(df),
        'sum_patterns': analyze_sum_patterns(df),
        'gaps': detect_number_gaps(df, window=window),
    }

    # Add prize patterns if available
    prize_patterns = analyze_prize_winner_patterns(df)
    if 'error' not in prize_patterns:
        report['prize_patterns'] = prize_patterns

    return report


if __name__ == "__main__":
    # Test the pattern analyzer
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).parent))
    from data_loader import load_lottery_data

    data_path = Path(__file__).parent.parent / "datasets" / "nlb_mahajana_with_prizes.csv"

    if data_path.exists():
        print("Testing Pattern Analyzer Module...")
        print("=" * 70)

        df = load_lottery_data(data_path)

        print("\n1. HOT/COLD NUMBER ANALYSIS (Last 30 draws)")
        hot_cold = detect_hot_cold_numbers(df, window=30)
        print(f"Hot numbers (≥5 occurrences): {list(hot_cold['hot_numbers'].keys())}")
        print(f"Cold numbers (≤2 occurrences): {list(hot_cold['cold_numbers'].keys())}")

        print("\n2. CONSECUTIVE NUMBER ANALYSIS")
        consecutive = analyze_consecutive_numbers(df)
        print(f"Draws with consecutive numbers: {consecutive['draws_with_consecutive']} ({consecutive['percentage_with_consecutive']:.1f}%)")
        print(f"Average consecutive pairs per draw: {consecutive['avg_consecutive_pairs']:.2f}")

        print("\n3. REPEATING NUMBER ANALYSIS")
        repeating = analyze_repeating_numbers(df)
        print(f"Average repeats from previous draw: {repeating['avg_repeats_per_draw']:.2f}")
        print(f"Most common repeaters: {repeating['most_common_repeaters'][:5]}")

        print("\n4. ODD/EVEN PATTERN ANALYSIS")
        odd_even = analyze_odd_even_patterns(df)
        print(f"Most common pattern: {odd_even['most_common_pattern']}")
        print(f"Total unique patterns: {odd_even['total_unique_patterns']}")

        print("\n5. SUM PATTERN ANALYSIS")
        sums = analyze_sum_patterns(df)
        print(f"Average sum: {sums['avg_sum']:.2f}")
        print(f"Range: {sums['min_sum']} - {sums['max_sum']}")

        print("\n6. GAP ANALYSIS (Last 10 draws)")
        gaps = detect_number_gaps(df, window=10)
        print(f"Numbers not appearing: {gaps['gap_numbers']}")
        print(f"Gap percentage: {gaps['gap_percentage']:.1f}%")

        print("\n" + "="*70)
        print("[OK] Pattern analyzer test complete")
    else:
        print(f"Dataset not found: {data_path}")

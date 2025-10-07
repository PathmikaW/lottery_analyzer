"""
Main Analyzer Pipeline
Orchestrates complete lottery statistical analysis

"""

import argparse
import sys
from pathlib import Path
import json

# Import analysis modules
from data_loader import load_lottery_data, get_dataset_info, validate_data
from lottery_statistics import (calculate_number_frequency, calculate_letter_frequency,
                       calculate_basic_statistics, generate_summary_report,
                       print_frequency_table)
from pattern_analyzer import (detect_hot_cold_numbers, analyze_consecutive_numbers,
                              analyze_odd_even_patterns, generate_pattern_report)
from visualizer import create_all_visualizations


def print_header(title):
    """Print formatted section header"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80)


def print_subheader(title):
    """Print formatted subsection header"""
    print(f"\n{title}")
    print("-"*60)


def run_analysis(lottery_name, output_dir, window_size=30):
    """
    Run complete lottery analysis pipeline

    Args:
        lottery_name (str): 'mahajana' or 'govisetha'
        output_dir (str/Path): Output directory for results
        window_size (int): Window size for hot/cold analysis
    """
    # Setup paths
    project_root = Path(__file__).parent.parent
    dataset_path = project_root / "datasets" / f"nlb_{lottery_name}_with_prizes.csv"

    # Set default output path if not provided
    if output_dir is None:
        output_path = project_root / "outputs"
    else:
        output_path = Path(output_dir)

    charts_dir = output_path / "charts"
    stats_dir = output_path / "statistics"

    # Create output directories
    charts_dir.mkdir(parents=True, exist_ok=True)
    stats_dir.mkdir(parents=True, exist_ok=True)

    print_header("SRI LANKAN LOTTERY STATISTICAL ANALYZER")
    print(f"\nAnalyzing: {lottery_name.upper()}")
    print(f"Dataset: {dataset_path}")
    print(f"Output: {output_path}")

    # 1. LOAD AND VALIDATE DATA
    print_header("STEP 1: DATA LOADING & VALIDATION")
    df = load_lottery_data(dataset_path)
    info = get_dataset_info(df)
    validation = validate_data(df)

    print_subheader("Dataset Information")
    print(f"  Lottery Type: {info['lottery_type']}")
    print(f"  Total Draws: {info['total_draws']}")
    print(f"  Date Range: {info['date_range'][0]} to {info['date_range'][1]}")
    print(f"  Numbers per Draw: {info['numbers_per_draw']}")
    print(f"  Unique Letters: {info['unique_letters']}")

    # 2. STATISTICAL ANALYSIS
    print_header("STEP 2: STATISTICAL ANALYSIS")

    print_subheader("2.1 Number Frequency Analysis")
    num_freq = calculate_number_frequency(df)
    print_frequency_table(num_freq, "Number Frequency Distribution")

    print_subheader("2.2 Letter Frequency Analysis")
    letter_freq = calculate_letter_frequency(df)
    print(f"  Total unique letters: {letter_freq['total_unique']}")
    print(f"  Most common: {letter_freq['most_common']}")
    print(f"  Least common: {letter_freq['least_common']}")

    print_subheader("2.3 Basic Statistics")
    basic_stats = calculate_basic_statistics(df)
    for key, value in basic_stats.items():
        print(f"  {key.replace('_', ' ').title():<20}: {value:.2f}")

    # 3. PATTERN ANALYSIS
    print_header("STEP 3: PATTERN ANALYSIS")

    print_subheader("3.1 Hot/Cold Number Analysis")
    hot_cold = detect_hot_cold_numbers(df, window=window_size)
    print(f"  Window Size: {window_size} draws")
    print(f"  Hot Numbers (>={hot_cold['hot_threshold']} occurrences): {list(hot_cold['hot_numbers'].keys())}")
    print(f"  Cold Numbers (<={hot_cold['cold_threshold']} occurrences): {list(hot_cold['cold_numbers'].keys())}")

    print_subheader("3.2 Consecutive Number Analysis")
    consecutive = analyze_consecutive_numbers(df)
    print(f"  Draws with consecutive pairs: {consecutive['draws_with_consecutive']} ({consecutive['percentage_with_consecutive']:.1f}%)")
    print(f"  Average consecutive pairs: {consecutive['avg_consecutive_pairs']:.2f}")
    print(f"  Maximum consecutive pairs: {consecutive['max_consecutive_pairs']}")

    print_subheader("3.3 Odd/Even Pattern Analysis")
    odd_even = analyze_odd_even_patterns(df)
    print(f"  Most common pattern: {odd_even['most_common_pattern']}")
    print(f"  Total unique patterns: {odd_even['total_unique_patterns']}")
    print(f"  Expected balanced pattern: {odd_even['expected_balanced']}")

    # 4. VISUALIZATION
    print_header("STEP 4: GENERATING VISUALIZATIONS")
    create_all_visualizations(df, charts_dir, num_freq, hot_cold, odd_even,
                              consecutive, letter_freq)

    # 5. EXPORT RESULTS
    print_header("STEP 5: EXPORTING RESULTS")

    # Export summary statistics to JSON
    summary = generate_summary_report(df)
    summary_path = stats_dir / f"{lottery_name}_summary_statistics.json"
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2, default=str)
    print(f" Summary statistics: {summary_path}")

    # Export frequency data to CSV
    import pandas as pd
    freq_df = pd.DataFrame([
        {'number': num, 'frequency': count}
        for num, count in num_freq['frequency'].items()
    ]).sort_values('frequency', ascending=False)
    freq_path = stats_dir / f"{lottery_name}_number_frequency.csv"
    freq_df.to_csv(freq_path, index=False)
    print(f" Number frequency CSV: {freq_path}")

    # 6. FINAL SUMMARY
    print_header("ANALYSIS COMPLETE")
    print(f"\n Dataset: {info['total_draws']} draws analyzed")
    print(f" Charts generated: {len(list(charts_dir.glob('*.png')))} PNG files")
    print(f" Statistics exported: {len(list(stats_dir.glob('*')))} files")
    print(f"\nOutput directory: {output_path}")
    print("\nNext steps:")
    print("  1. Review charts in outputs/charts/")
    print("  2. Check statistics in outputs/statistics/")
    print("  3. Use data for educational/research purposes")
    print("\n" + "="*80 + "\n")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Sri Lankan Lottery Statistical Analyzer - IT 5117 Assignment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main_analyzer.py --lottery mahajana
  python main_analyzer.py --lottery govisetha --output custom_output --window 60

        """
    )

    parser.add_argument(
        '--lottery',
        choices=['mahajana', 'govisetha'],
        required=True,
        help='Lottery to analyze (mahajana or govisetha)'
    )

    parser.add_argument(
        '--output',
        default=None,
        help='Output directory for results (default: lottery_analysis/outputs)'
    )

    parser.add_argument(
        '--window',
        type=int,
        default=30,
        help='Window size for hot/cold analysis (default: 30)'
    )

    args = parser.parse_args()

    try:
        run_analysis(args.lottery, args.output, args.window)
    except FileNotFoundError as e:
        print(f"\n[ERROR] Error: Dataset not found - {e}")
        print("Make sure datasets are in the 'datasets/' folder")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Error during analysis: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

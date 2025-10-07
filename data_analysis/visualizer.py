"""
Visualizer Module
Creates charts and visualizations for lottery analysis

"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)


def plot_number_frequency(frequency_data, output_path=None, title="Number Frequency Distribution"):
    """
    Plot bar chart of number frequencies

    Args:
        frequency_data (dict): Frequency statistics from statistics module
        output_path (str): Path to save chart (PNG)
        title (str): Chart title
    """
    freq = frequency_data['frequency']
    numbers = sorted(freq.keys())
    counts = [freq[n] for n in numbers]

    plt.figure(figsize=(14, 6))
    bars = plt.bar(numbers, counts, color='steelblue', edgecolor='navy', alpha=0.7)

    # Highlight max and min
    max_idx = counts.index(max(counts))
    min_idx = counts.index(min(counts))
    bars[max_idx].set_color('green')
    bars[min_idx].set_color('red')

    plt.xlabel('Number', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xticks(numbers)
    plt.grid(axis='y', alpha=0.3)

    # Add average line
    avg = frequency_data['average_per_number']
    plt.axhline(y=avg, color='orange', linestyle='--', label=f'Average: {avg:.1f}')
    plt.legend()

    plt.tight_layout()

    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"[OK] Saved: {output_path}")

    plt.close()


def plot_hot_cold_comparison(hot_cold_data, output_path=None):
    """
    Plot side-by-side comparison of hot and cold numbers

    Args:
        hot_cold_data (dict): Hot/cold statistics
        output_path (str): Path to save chart
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Hot numbers
    hot = hot_cold_data['hot_numbers']
    if hot:
        numbers = list(hot.keys())
        counts = list(hot.values())
        ax1.bar(numbers, counts, color='orangered', edgecolor='darkred', alpha=0.7)
        ax1.set_title(f"Hot Numbers (Last {hot_cold_data['window_size']} Draws)", fontsize=14, fontweight='bold')
        ax1.set_xlabel('Number', fontsize=12)
        ax1.set_ylabel('Frequency', fontsize=12)
        ax1.axhline(y=hot_cold_data['hot_threshold'], color='red', linestyle='--',
                   label=f"Hot threshold: {hot_cold_data['hot_threshold']}")
        ax1.legend()
        ax1.grid(axis='y', alpha=0.3)

    # Cold numbers
    cold = hot_cold_data['cold_numbers']
    if cold:
        numbers = list(cold.keys())
        counts = list(cold.values())
        ax2.bar(numbers, counts, color='skyblue', edgecolor='navy', alpha=0.7)
        ax2.set_title(f"Cold Numbers (Last {hot_cold_data['window_size']} Draws)", fontsize=14, fontweight='bold')
        ax2.set_xlabel('Number', fontsize=12)
        ax2.set_ylabel('Frequency', fontsize=12)
        ax2.axhline(y=hot_cold_data['cold_threshold'], color='blue', linestyle='--',
                   label=f"Cold threshold: {hot_cold_data['cold_threshold']}")
        ax2.legend()
        ax2.grid(axis='y', alpha=0.3)

    plt.tight_layout()

    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"[OK] Saved: {output_path}")

    plt.close()


def plot_odd_even_distribution(odd_even_data, output_path=None):
    """
    Plot pie chart of odd/even distribution

    Args:
        odd_even_data (dict): Odd/even statistics
        output_path (str): Path to save chart
    """
    pattern_dist = odd_even_data['pattern_distribution']

    # Get most common patterns (top 5)
    sorted_patterns = sorted(pattern_dist.items(), key=lambda x: x[1], reverse=True)[:5]
    labels = [f"{p[0]} (Odd:Even)" for p in sorted_patterns]
    sizes = [p[1] for p in sorted_patterns]
    colors = plt.cm.Set3(range(len(labels)))

    plt.figure(figsize=(10, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
    plt.title('Odd/Even Pattern Distribution (Top 5)', fontsize=14, fontweight='bold')

    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"[OK] Saved: {output_path}")

    plt.close()


def plot_consecutive_patterns(consecutive_data, output_path=None):
    """
    Plot consecutive number pattern distribution

    Args:
        consecutive_data (dict): Consecutive pattern statistics
        output_path (str): Path to save chart
    """
    distribution = consecutive_data['distribution']
    pairs = sorted(distribution.keys())
    counts = [distribution[p] for p in pairs]

    plt.figure(figsize=(10, 6))
    plt.bar(pairs, counts, color='mediumseagreen', edgecolor='darkgreen', alpha=0.7)
    plt.xlabel('Number of Consecutive Pairs', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.title('Distribution of Consecutive Number Pairs', fontsize=14, fontweight='bold')
    plt.xticks(pairs)
    plt.grid(axis='y', alpha=0.3)

    # Add percentage labels
    total = sum(counts)
    for i, (p, c) in enumerate(zip(pairs, counts)):
        percentage = (c / total) * 100
        plt.text(p, c + max(counts)*0.01, f'{percentage:.1f}%', ha='center', va='bottom')

    plt.tight_layout()

    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"[OK] Saved: {output_path}")

    plt.close()


def plot_sum_distribution(df, output_path=None):
    """
    Plot histogram of draw sum distribution

    Args:
        df (pd.DataFrame): Lottery dataframe
        output_path (str): Path to save chart
    """
    sums = [sum(numbers_list) for numbers_list in df['numbers_list']]

    plt.figure(figsize=(12, 6))
    plt.hist(sums, bins=20, color='purple', alpha=0.7, edgecolor='darkviolet')
    plt.axvline(np.mean(sums), color='red', linestyle='--', linewidth=2,
               label=f'Mean: {np.mean(sums):.1f}')
    plt.axvline(np.median(sums), color='orange', linestyle='--', linewidth=2,
               label=f'Median: {np.median(sums):.1f}')

    plt.xlabel('Sum of Numbers', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.title('Distribution of Draw Sums', fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(axis='y', alpha=0.3)

    plt.tight_layout()

    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"[OK] Saved: {output_path}")

    plt.close()


def plot_letter_frequency(letter_freq_data, output_path=None):
    """
    Plot bar chart of letter frequencies

    Args:
        letter_freq_data (dict): Letter frequency statistics
        output_path (str): Path to save chart
    """
    freq = letter_freq_data['frequency']
    letters = sorted(freq.keys())
    counts = [freq[l] for l in letters]

    plt.figure(figsize=(14, 6))
    plt.bar(letters, counts, color='coral', edgecolor='darkred', alpha=0.7)
    plt.xlabel('Letter', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.title('Letter Frequency Distribution', fontsize=14, fontweight='bold')
    plt.grid(axis='y', alpha=0.3)

    # Add percentage labels
    total = sum(counts)
    for i, (l, c) in enumerate(zip(letters, counts)):
        percentage = (c / total) * 100
        plt.text(i, c + max(counts)*0.01, f'{percentage:.1f}%', ha='center', va='bottom')

    plt.tight_layout()

    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"[OK] Saved: {output_path}")

    plt.close()


def plot_prize_winners_trend(df, tier='1', output_path=None):
    """
    Plot trend of winners over time for a specific tier

    Args:
        df (pd.DataFrame): Lottery dataframe with prize data
        tier (str): Prize tier to analyze
        output_path (str): Path to save chart
    """
    winner_col = f'{tier}_winners'

    if winner_col not in df.columns:
        print(f"Warning: {winner_col} not found in dataframe")
        return

    df_sorted = df.sort_values('draw_date')

    plt.figure(figsize=(14, 6))
    plt.plot(df_sorted['draw_date'], df_sorted[winner_col],
            marker='o', linestyle='-', color='dodgerblue', markersize=4, alpha=0.7)

    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Number of Winners', fontsize=12)
    plt.title(f'Prize Tier {tier} - Winners Trend Over Time', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)

    # Add average line
    avg = df_sorted[winner_col].mean()
    plt.axhline(y=avg, color='red', linestyle='--', label=f'Average: {avg:.1f}')
    plt.legend()

    plt.tight_layout()

    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"[OK] Saved: {output_path}")

    plt.close()


def create_all_visualizations(df, output_dir, frequency_data, hot_cold_data,
                              odd_even_data, consecutive_data, letter_freq_data=None):
    """
    Create all visualizations and save to output directory

    Args:
        df (pd.DataFrame): Lottery dataframe
        output_dir (str/Path): Directory to save charts
        frequency_data (dict): Number frequency data
        hot_cold_data (dict): Hot/cold analysis data
        odd_even_data (dict): Odd/even pattern data
        consecutive_data (dict): Consecutive pattern data
        letter_freq_data (dict): Letter frequency data (optional)
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print("\nGenerating visualizations...")
    print("=" * 60)

    # 1. Number frequency
    plot_number_frequency(frequency_data,
                         output_dir / "01_number_frequency.png")

    # 2. Hot/Cold comparison
    plot_hot_cold_comparison(hot_cold_data,
                            output_dir / "02_hot_cold_comparison.png")

    # 3. Odd/Even distribution
    plot_odd_even_distribution(odd_even_data,
                              output_dir / "03_odd_even_distribution.png")

    # 4. Consecutive patterns
    plot_consecutive_patterns(consecutive_data,
                             output_dir / "04_consecutive_patterns.png")

    # 5. Sum distribution
    plot_sum_distribution(df,
                         output_dir / "05_sum_distribution.png")

    # 6. Letter frequency (if available)
    if letter_freq_data:
        plot_letter_frequency(letter_freq_data,
                             output_dir / "06_letter_frequency.png")

    # 7. Prize winner trends (if available)
    if '1_winners' in df.columns:
        plot_prize_winners_trend(df, tier='1',
                                output_path=output_dir / "07_jackpot_winners_trend.png")

    print("\n" + "="*60)
    print(f"[OK] All visualizations saved to: {output_dir}")


if __name__ == "__main__":
    # Test visualizations
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).parent))
    from data_loader import load_lottery_data
    from statistics import calculate_number_frequency, calculate_letter_frequency
    from pattern_analyzer import (detect_hot_cold_numbers, analyze_odd_even_patterns,
                                  analyze_consecutive_numbers)

    data_path = Path(__file__).parent.parent / "datasets" / "nlb_mahajana_with_prizes.csv"
    output_dir = Path(__file__).parent.parent / "outputs" / "charts"

    if data_path.exists():
        print("Testing Visualizer Module...")
        print("=" * 70)

        df = load_lottery_data(data_path)

        # Calculate statistics
        freq = calculate_number_frequency(df)
        hot_cold = detect_hot_cold_numbers(df, window=30)
        odd_even = analyze_odd_even_patterns(df)
        consecutive = analyze_consecutive_numbers(df)
        letter_freq = calculate_letter_frequency(df)

        # Create all visualizations
        create_all_visualizations(df, output_dir, freq, hot_cold, odd_even,
                                 consecutive, letter_freq)

        print("\n[OK] Visualizer module test complete")
    else:
        print(f"Dataset not found: {data_path}")

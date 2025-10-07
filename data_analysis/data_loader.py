"""
Data Loader Module
Loads and preprocesses lottery CSV data for analysis

"""

import pandas as pd
import numpy as np
from pathlib import Path


def load_lottery_data(filepath, parse_prizes=True):
    """
    Load and preprocess lottery CSV data

    Args:
        filepath (str): Path to CSV file
        parse_prizes (bool): Whether to process prize columns

    Returns:
        pd.DataFrame: Preprocessed lottery data
    """
    # Load CSV
    df = pd.read_csv(filepath)

    # Convert draw_date to datetime
    df['draw_date'] = pd.to_datetime(df['draw_date'], errors='coerce')

    # Parse semicolon-separated numbers into lists of integers
    df['numbers_list'] = df['numbers'].str.split(';').apply(
        lambda x: [int(n) for n in x] if x is not None else []
    )

    # Extract individual numbers as separate columns for easier analysis
    max_numbers = df['numbers_list'].str.len().max()
    for i in range(max_numbers):
        df[f'num_{i+1}'] = df['numbers_list'].apply(
            lambda x: int(x[i]) if i < len(x) else None
        )

    # Parse prize columns if requested
    if parse_prizes:
        prize_cols = [col for col in df.columns if '_prize' in col or '_total' in col]
        for col in prize_cols:
            # Remove 'Rs.' and commas, convert to numeric
            df[col] = df[col].astype(str).str.replace('Rs. ', '').str.replace(',', '')
            df[col] = pd.to_numeric(df[col], errors='coerce')

        # Convert winner columns to numeric
        winner_cols = [col for col in df.columns if '_winners' in col]
        for col in winner_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Add calculated fields
    df['total_numbers'] = df['numbers_list'].str.len()
    df['year'] = df['draw_date'].dt.year
    df['month'] = df['draw_date'].dt.month
    df['day_of_week'] = df['draw_date'].dt.day_name()

    print(f"[OK] Loaded {len(df)} draws from {filepath}")
    print(f"  Date range: {df['draw_date'].min()} to {df['draw_date'].max()}")
    print(f"  Columns: {len(df.columns)}")

    return df


def get_dataset_info(df):
    """
    Get summary information about the dataset

    Args:
        df (pd.DataFrame): Lottery dataframe

    Returns:
        dict: Dataset statistics
    """
    info = {
        'total_draws': len(df),
        'date_range': (df['draw_date'].min(), df['draw_date'].max()),
        'lottery_type': df['game'].iloc[0] if 'game' in df.columns else 'Unknown',
        'numbers_per_draw': df['total_numbers'].iloc[0] if 'total_numbers' in df.columns else 0,
        'columns': list(df.columns),
        'missing_values': df.isnull().sum().sum(),
        'unique_letters': df['letter'].nunique() if 'letter' in df.columns else 0
    }

    return info


def filter_by_date_range(df, start_date=None, end_date=None):
    """
    Filter draws by date range

    Args:
        df (pd.DataFrame): Lottery dataframe
        start_date (str): Start date (YYYY-MM-DD)
        end_date (str): End date (YYYY-MM-DD)

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    filtered_df = df.copy()

    if start_date:
        filtered_df = filtered_df[filtered_df['draw_date'] >= pd.to_datetime(start_date)]

    if end_date:
        filtered_df = filtered_df[filtered_df['draw_date'] <= pd.to_datetime(end_date)]

    print(f"[OK] Filtered to {len(filtered_df)} draws ({start_date} to {end_date})")

    return filtered_df


def get_recent_draws(df, n=30):
    """
    Get the most recent N draws

    Args:
        df (pd.DataFrame): Lottery dataframe
        n (int): Number of recent draws

    Returns:
        pd.DataFrame: Recent draws
    """
    return df.sort_values('draw_date', ascending=False).head(n)


def validate_data(df):
    """
    Validate lottery data for consistency

    Args:
        df (pd.DataFrame): Lottery dataframe

    Returns:
        dict: Validation results
    """
    validation = {
        'valid': True,
        'issues': []
    }

    # Check for missing draw IDs
    if df['draw_id'].isnull().any():
        validation['valid'] = False
        validation['issues'].append('Missing draw IDs found')

    # Check for duplicate draw IDs
    if df['draw_id'].duplicated().any():
        validation['valid'] = False
        validation['issues'].append('Duplicate draw IDs found')

    # Check number ranges (assuming 0-9 for most lotteries)
    if 'numbers_list' in df.columns:
        all_numbers = [n for nums in df['numbers_list'] for n in nums]
        if any(n < 0 or n > 90 for n in all_numbers):
            validation['valid'] = False
            validation['issues'].append('Numbers out of valid range (0-90)')

    if validation['valid']:
        print("[OK] Data validation passed")
    else:
        print("[WARNING] Data validation issues:")
        for issue in validation['issues']:
            print(f"  - {issue}")

    return validation


if __name__ == "__main__":
    # Test the data loader
    import sys
    from pathlib import Path

    # Test with Mahajana Sampatha
    data_path = Path(__file__).parent.parent / "datasets" / "nlb_mahajana_with_prizes.csv"

    if data_path.exists():
        print("Testing Data Loader...")
        print("=" * 50)

        df = load_lottery_data(data_path)
        info = get_dataset_info(df)

        print("\nDataset Info:")
        print(f"  Lottery: {info['lottery_type']}")
        print(f"  Total draws: {info['total_draws']}")
        print(f"  Numbers per draw: {info['numbers_per_draw']}")
        print(f"  Unique letters: {info['unique_letters']}")

        validate_data(df)

        print("\nSample Data:")
        print(df[['draw_id', 'draw_date', 'letter', 'numbers', 'numbers_list']].head(3))
    else:
        print(f"Dataset not found: {data_path}")

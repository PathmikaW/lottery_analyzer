# Sri Lankan Lottery Statistical Analyzer V1.0.0

---

## Project Overview

Statistical analysis system for Sri Lanka's National Lotteries Board (NLB) lotteries with automated web scraping and comprehensive analysis.

### Key Features

- Web scraping with bot protection bypass
- Statistical analysis with chi-square testing
- Pattern detection (hot/cold, consecutive, odd/even)
- 7 publication-quality charts (300 DPI)
- JSON/CSV data export

---

## Installation

```bash
pip install -r requirements.txt
```

**Required:** pandas, numpy, matplotlib, seaborn, scipy, requests, beautifulsoup4

--- ## Project Structure

```
lottery_analysis/
├── data_collection/        # Web scraping modules
├── data_analysis/          # Analysis modules
├── datasets/               # CSV data files
├── outputs/
│   ├── charts/            # PNG visualizations
│   └── statistics/        # JSON/CSV stats
└── requirements.txt
```

---

## Assignment Execution Commands

### 1. Data Collection (Web Scraping)

#### Mahajana Sampatha

```bash
# Basic dataset
python data_collection/main_scrape.py --game mahajana_sampatha --out datasets/nlb_mahajana.csv

# With prize information
python data_collection/main_scrape.py --game mahajana_sampatha --out datasets/nlb_mahajana_with_prizes.csv --prizes
```

**Output:** `datasets/nlb_mahajana.csv` (basic) or `datasets/nlb_mahajana_with_prizes.csv` (with prizes)

#### Govisetha

```bash
# Basic dataset
python data_collection/main_scrape.py --game govisetha --out datasets/nlb_govisetha.csv

# With prize information
python data_collection/main_scrape.py --game govisetha --out datasets/nlb_govisetha_with_prizes.csv --prizes
```

**Output:** `datasets/nlb_govisetha.csv` (basic) or `datasets/nlb_govisetha_with_prizes.csv` (with prizes)

---

### 2. Data Analysis

#### Mahajana Sampatha

```bash
python data_analysis/main_analyzer.py --lottery mahajana
```

**Outputs:**

- `outputs/charts/mahajana_*.png` (7 charts)
- `outputs/statistics/mahajana_summary_statistics.json`
- `outputs/statistics/mahajana_number_frequency.csv`

#### Govisetha

```bash
python data_analysis/main_analyzer.py --lottery govisetha
```

**Outputs:**

- `outputs/charts/govisetha_*.png` (7 charts)
- `outputs/statistics/govisetha_summary_statistics.json`
- `outputs/statistics/govisetha_number_frequency.csv`

---

### Advanced Options

```bash
# Custom hot/cold window size
python data_analysis/main_analyzer.py --lottery mahajana --window 60

# Custom output directory
python data_analysis/main_analyzer.py --lottery govisetha --output my_results/
```

--- ## Generated Output Files

### Charts (7 PNG files at 300 DPI)

1. Number frequency bar chart
2. Hot/cold comparison chart
3. Odd/even pie chart
4. Consecutive patterns distribution
5. Sum distribution histogram
6. Letter frequency chart
7. Jackpot winners trend

### Statistics Files

- `{lottery}_summary_statistics.json` - Complete statistical report
- `{lottery}_number_frequency.csv` - Frequency table

---

## Analysis Features

### Statistical Analysis

- Number frequency distribution
- Chi-square uniformity test (randomness verification)
- Basic statistics (mean, median, mode, std dev)
- Odd/even analysis
- Prize statistics

### Pattern Detection

- Hot/cold numbers (sliding window)
- Consecutive number pairs
- Odd/even pattern ratios
- Number gaps

### Visualizations

- All charts: 300 DPI PNG format
- Color-coded highlights
- Statistical overlays (normal curves, averages)

---

## Key Findings

### Mahajana Sampatha

- **Chi-square p-value:** 0.0734 > 0.05 → Statistically random
- **Consecutive pairs:** 91.3% of draws contain consecutive numbers
- **Most frequent:** Number 6 (146 occurrences)
- **Odd/even balance:** Avg 3.08 odd, 2.92 even

### Govisetha

- **Number range:** 1-80 (wider distribution)
- **Consecutive pairs:** 14.4% of draws
- **Most frequent:** Number 73 (23 occurrences)
- **Odd/even balance:** Avg 2.01 odd, 1.99 even

---

## Python Libraries

### Data Collection

- requests, beautifulsoup4, urllib

### Data Analysis

- pandas, numpy, scipy

### Visualization

- matplotlib, seaborn

### Standard Library

- argparse, json, collections, datetime

---

## Quick Reference

```bash
# Installation
pip install -r requirements.txt

# Data Collection
python data_collection/main_scrape.py --game mahajana_sampatha --out datasets/nlb_mahajana.csv
python data_collection/main_scrape.py --game govisetha --out datasets/nlb_govisetha.csv

# Data Analysis
python data_analysis/main_analyzer.py --lottery mahajana
python data_analysis/main_analyzer.py --lottery govisetha
```

---

## Documentation Files

- `README.md` - Project overview and commands
- `OUTPUTS_ANALYSIS.md` - Output files summary
- `CODE_REVIEW_VIVA_GUIDE.md` - Viva preparation
- `data_collection/README.md` - Scraping details

---

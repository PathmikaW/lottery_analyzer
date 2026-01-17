# Data Statistics Explanation

This document explains how the project statistics were calculated and provides a detailed breakdown of the data transformation from raw draws to ML records.

---

## Quick Summary

| Metric | Value | Source File |
|--------|-------|-------------|
| Total Lotteries | 17 | `data_quality_stats.json` |
| Total Draws Scraped | 8,085 | `data_quality_stats.json` |
| Total ML Records | 485,094 | `split_stats.json` |
| Date Range | 2021-04-01 to 2026-01-12 | `data_quality_stats.json` |
| Date Span | 1,747 days (~58 months) | `data_quality_stats.json` |
| Data Completeness | 96.47% | `data_quality_stats.json` |
| Positive Class (appeared) | 32,511 (6.70%) | `split_stats.json` |
| Negative Class (not appeared) | 452,583 (93.30%) | `split_stats.json` |
| Imbalance Ratio | 1:13.92 | `split_stats.json` |

---

## 1. From Draws to ML Records: The Expansion

### Why 8,085 Draws Become 485,094 Records

**Key Insight**: Each lottery draw is expanded into multiple ML records - one for each possible number in that lottery's number range.

**Formula**:
```
ML Records = Sum of (Draws × Number_Range) for each lottery
```

### Detailed Breakdown by Lottery

| Lottery | Draws | Numbers per Draw | Number Range | ML Records | Calculation |
|---------|-------|------------------|--------------|------------|-------------|
| dlb_ada_kotipathi | 772 | 4 | 1-76 | 58,672 | 772 × 76 |
| dlb_jaya_sampatha | 154 | 4 | 1-10 | 1,540 | 154 × 10 |
| dlb_jayoda | 74 | 4 | 1-68 | 5,032 | 74 × 68 |
| dlb_kapruka | 122 | 5 | 1-75 | 9,150 | 122 × 75 |
| dlb_lagna_wasana | 1,627 | 4 | 1-62 | 100,874 | 1,627 × 62 |
| dlb_sasiri | 773 | 3 | 1-50 | 38,650 | 773 × 50 |
| dlb_shanida | 1,627 | 4 | 1-80 | 130,160 | 1,627 × 80 |
| dlb_super_ball | 946 | 4 | 1-80 | 75,680 | 946 × 80 |
| dlb_supiri_dhana_sampatha | 680 | 6 | 1-10 | 6,800 | 680 × 10 |
| nlb_ada_sampatha | 207 | 6 | 1-10 | 2,070 | 207 × 10 |
| nlb_dhana_nidhanaya | 81 | 5 | 1-83 | 6,723 | 81 × 83 |
| nlb_govisetha | 215 | 4 | 1-80 | 17,200 | 215 × 80 |
| nlb_handahana | 81 | 6 | 1-63 | 5,103 | 81 × 63 |
| nlb_mahajana_sampatha | 215 | 6 | 1-10 | 2,150 | 215 × 10 |
| nlb_mega_power | 215 | 5 | 1-80 | 17,200 | 215 × 80 |
| nlb_nlb_jaya | 206 | 4 | 1-10 | 2,060 | 206 × 10 |
| nlb_suba_dawasak | 90 | 5 | 1-67 | 6,030 | 90 × 67 |
| **TOTAL** | **8,085** | - | - | **485,094** | - |

### Example: How One Draw Becomes Multiple Records

**Example**: dlb_shanida draw #1234 on 2025-06-15
- Winning numbers: [12, 34, 56, 78]
- Number range: 1-80
- This single draw creates **80 ML records**:

| Number | Target (appeared) | Features |
|--------|-------------------|----------|
| 1 | 0 (not in winning) | frequency_last_10, days_since_last, ... |
| 2 | 0 (not in winning) | frequency_last_10, days_since_last, ... |
| ... | ... | ... |
| 12 | **1** (in winning) | frequency_last_10, days_since_last, ... |
| ... | ... | ... |
| 34 | **1** (in winning) | frequency_last_10, days_since_last, ... |
| ... | ... | ... |
| 56 | **1** (in winning) | frequency_last_10, days_since_last, ... |
| ... | ... | ... |
| 78 | **1** (in winning) | frequency_last_10, days_since_last, ... |
| 79 | 0 (not in winning) | frequency_last_10, days_since_last, ... |
| 80 | 0 (not in winning) | frequency_last_10, days_since_last, ... |

---

## 2. Class Distribution Explained

### Why 6.7% Positive, 93.3% Negative?

**Calculation**:
- Total Positive (appeared): 32,511
- Total Negative (not appeared): 452,583
- **Positive Ratio**: 32,511 / 485,094 = **6.70%**
- **Negative Ratio**: 452,583 / 485,094 = **93.30%**
- **Imbalance Ratio**: 452,583 / 32,511 = **13.92:1**

### Why This Makes Sense

**Mathematical Explanation**:
- Each draw has a specific number of winning numbers (typically 3-6)
- But each draw evaluates ALL possible numbers in the range (10-83)
- Therefore, most numbers do NOT appear in any given draw

**Example Calculation**:
```
Average numbers_per_draw ≈ 4.5 (varies by lottery)
Average number_range ≈ 55 (varies by lottery)
Expected positive ratio ≈ 4.5 / 55 = 8.2%
Actual positive ratio = 6.70%
```

The slight difference is due to:
1. Some lotteries have larger number ranges (e.g., 1-80)
2. Some lotteries have fewer winning numbers per draw (e.g., 3)
3. Weighted average across all lotteries

### Breakdown by Lottery

| Lottery | Total Records | Positive | Negative | Positive % | Imbalance |
|---------|---------------|----------|----------|------------|-----------|
| dlb_ada_kotipathi | 58,672 | 3,088 | 55,584 | 5.26% | 18.0:1 |
| dlb_jaya_sampatha | 1,540 | 521 | 1,019 | 33.83% | 1.96:1 |
| dlb_jayoda | 5,032 | 296 | 4,736 | 5.88% | 16.0:1 |
| dlb_kapruka | 9,150 | 606 | 8,544 | 6.62% | 14.1:1 |
| dlb_lagna_wasana | 100,874 | 6,508 | 94,366 | 6.45% | 14.5:1 |
| dlb_sasiri | 38,650 | 2,319 | 36,331 | 6.00% | 15.7:1 |
| dlb_shanida | 130,160 | 6,508 | 123,652 | 5.00% | 19.0:1 |
| dlb_super_ball | 75,680 | 3,784 | 71,896 | 5.00% | 19.0:1 |
| dlb_supiri_dhana_sampatha | 6,800 | 3,211 | 3,589 | 47.22% | 1.12:1 |
| nlb_ada_sampatha | 2,070 | 718 | 1,352 | 34.69% | 1.88:1 |
| nlb_dhana_nidhanaya | 6,723 | 401 | 6,322 | 5.96% | 15.8:1 |
| nlb_govisetha | 17,200 | 860 | 16,340 | 5.00% | 19.0:1 |
| nlb_handahana | 5,103 | 467 | 4,636 | 9.15% | 9.93:1 |
| nlb_mahajana_sampatha | 2,150 | 1,019 | 1,131 | 47.39% | 1.11:1 |
| nlb_mega_power | 17,200 | 1,062 | 16,138 | 6.17% | 15.2:1 |
| nlb_nlb_jaya | 2,060 | 711 | 1,349 | 34.51% | 1.90:1 |
| nlb_suba_dawasak | 6,030 | 432 | 5,598 | 7.16% | 13.0:1 |
| **OVERALL** | **485,094** | **32,511** | **452,583** | **6.70%** | **13.92:1** |

**Note**: Lotteries with small number ranges (1-10) have higher positive ratios because each number has a higher probability of appearing.

---

## 3. Data Sources Breakdown

### NLB (National Lotteries Board) - 8 Lotteries

| Lottery | Draws | Records | Date Range |
|---------|-------|---------|------------|
| nlb_ada_sampatha | 207 | 2,070 | 2025-06-12 to 2026-01-12 |
| nlb_dhana_nidhanaya | 81 | 6,723 | 2025-06-12 to 2025-08-31 |
| nlb_govisetha | 215 | 17,200 | 2025-06-12 to 2026-01-12 |
| nlb_handahana | 81 | 5,103 | 2025-06-12 to 2025-08-31 |
| nlb_mahajana_sampatha | 215 | 2,150 | 2025-06-12 to 2026-01-12 |
| nlb_mega_power | 215 | 17,200 | 2025-06-12 to 2026-01-12 |
| nlb_nlb_jaya | 206 | 2,060 | 2025-06-12 to 2026-01-12 |
| nlb_suba_dawasak | 90 | 6,030 | 2025-07-09 to 2026-01-12 |
| **NLB Total** | **1,310** | **58,536** | - |

### DLB (Development Lotteries Board) - 9 Lotteries

| Lottery | Draws | Records | Date Range |
|---------|-------|---------|------------|
| dlb_ada_kotipathi | 772 | 58,672 | 2023-11-16 to 2026-01-11 |
| dlb_jaya_sampatha | 154 | 1,540 | 2025-08-11 to 2026-01-11 |
| dlb_jayoda | 74 | 5,032 | 2025-02-03 to 2025-10-27 |
| dlb_kapruka | 122 | 9,150 | 2025-09-12 to 2026-01-11 |
| dlb_lagna_wasana | 1,627 | 100,874 | 2021-04-01 to 2026-01-11 |
| dlb_sasiri | 773 | 38,650 | 2021-11-10 to 2026-01-11 |
| dlb_shanida | 1,627 | 130,160 | 2021-04-01 to 2026-01-11 |
| dlb_super_ball | 946 | 75,680 | 2023-05-26 to 2026-01-11 |
| dlb_supiri_dhana_sampatha | 680 | 6,800 | 2024-02-16 to 2026-01-11 |
| **DLB Total** | **6,775** | **426,558** | - |

---

## 4. Train/Validation/Test Split

**Split Configuration**:
- Train: 70%
- Validation: 15%
- Test: 15%
- Stratified: Yes (preserves class distribution in each split)
- Random State: 42 (for reproducibility)

**Actual Split Sizes**:

| Split | Records | Positive | Negative | Positive % |
|-------|---------|----------|----------|------------|
| Train | 339,555 | 22,758 | 316,797 | 6.70% |
| Validation | 72,770 | 4,878 | 67,892 | 6.70% |
| Test | 72,769 | 4,875 | 67,894 | 6.70% |
| **Total** | **485,094** | **32,511** | **452,583** | **6.70%** |

---

## 5. Verification Commands

To verify these statistics yourself, you can run:

```python
import json

# Load split stats
with open('outputs/statistics/split_stats.json', 'r') as f:
    split_stats = json.load(f)

# Verify totals
total_records = split_stats['overall']['total_records']
total_positive = split_stats['overall']['total_positive']
total_negative = split_stats['overall']['total_negative']

print(f"Total Records: {total_records:,}")
print(f"Positive: {total_positive:,} ({total_positive/total_records*100:.2f}%)")
print(f"Negative: {total_negative:,} ({total_negative/total_records*100:.2f}%)")
print(f"Imbalance Ratio: 1:{total_negative/total_positive:.2f}")
```

**Expected Output**:
```
Total Records: 485,094
Positive: 32,511 (6.70%)
Negative: 452,583 (93.30%)
Imbalance Ratio: 1:13.92
```

---

## 6. Key Takeaways

1. **8,085 draws become 485,094 ML records** through number-wise expansion (each number in each draw becomes a separate classification task)

2. **6.7% positive class** is mathematically expected because each draw only has 3-6 winning numbers out of 10-80 possible numbers

3. **13.92:1 imbalance ratio** represents a significant class imbalance challenge, addressed using CatBoost's `auto_class_weights='Balanced'` parameter

4. **Data is authentic** - all statistics are directly from the output JSON files generated during preprocessing

---

**Source Files**:
- `outputs/statistics/data_quality_stats.json` - Draw-level statistics
- `outputs/statistics/split_stats.json` - ML record-level statistics with train/val/test splits

**Last Updated**: January 2026

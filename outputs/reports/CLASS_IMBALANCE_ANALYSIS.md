# Class Imbalance Analysis and Strategy

## Executive Summary

After data splitting, we have identified significant class imbalance across all 17 lottery datasets. This document details the imbalance ratios and recommends strategies for handling them during model training.

## Overall Statistics

- **Total Records**: 485,094
- **Positive Class (appeared=1)**: 32,511 (6.70%)
- **Negative Class (appeared=0)**: 452,583 (93.30%)
- **Overall Imbalance Ratio**: 1:13.92

## Imbalance by Lottery

### Highly Imbalanced (Ratio ≥ 15:1)

| Lottery | Imbalance Ratio | Positive % | Total Records |
|---------|----------------|------------|---------------|
| dlb_shanida | 1:19.00 | 5.00% | 130,160 |
| dlb_super_ball | 1:19.00 | 5.00% | 75,680 |
| nlb_govisetha | 1:19.00 | 5.00% | 17,200 |
| dlb_ada_kotipathi | 1:18.00 | 5.26% | 58,672 |
| dlb_jayoda | 1:16.00 | 5.88% | 5,032 |
| dlb_sasiri | 1:15.67 | 6.00% | 38,650 |
| nlb_dhana_nidhanaya | 1:15.77 | 5.96% | 6,723 |
| nlb_mega_power | 1:15.20 | 6.17% | 17,200 |

**8 lotteries (47.1%)** - Extremely imbalanced, requires aggressive balancing

### Moderately Imbalanced (5:1 ≤ Ratio < 15:1)

| Lottery | Imbalance Ratio | Positive % | Total Records |
|---------|----------------|------------|---------------|
| dlb_lagna_wasana | 1:14.50 | 6.45% | 100,874 |
| dlb_kapruka | 1:14.10 | 6.62% | 9,150 |
| nlb_suba_dawasak | 1:12.96 | 7.16% | 6,030 |
| nlb_handahana | 1:9.93 | 9.15% | 5,103 |

**4 lotteries (23.5%)** - Moderate imbalance, standard balancing techniques

### Balanced (Ratio < 5:1)

| Lottery | Imbalance Ratio | Positive % | Total Records |
|---------|----------------|------------|---------------|
| dlb_jaya_sampatha | 1:1.96 | 33.83% | 1,540 |
| nlb_ada_sampatha | 1:1.88 | 34.69% | 2,070 |
| nlb_nlb_jaya | 1:1.90 | 34.51% | 2,060 |
| dlb_supiri_dhana_sampatha | 1:1.12 | 47.22% | 6,800 |
| nlb_mahajana_sampatha | 1:1.11 | 47.40% | 2,150 |

**5 lotteries (29.4%)** - Nearly balanced, minimal balancing needed

## Imbalance Ratio Statistics

- **Minimum**: 1:1.11 (nlb_mahajana_sampatha)
- **Maximum**: 1:19.00 (dlb_shanida, dlb_super_ball, nlb_govisetha)
- **Mean**: 1:11.59
- **Median**: 1:14.50
- **Standard Deviation**: 6.24

## Class Distribution in Splits

All splits maintained stratification successfully:

### Example: dlb_shanida (Highly Imbalanced)
- **Training Set**: 91,112 records → 4,556 positive (5.00%)
- **Validation Set**: 19,524 records → 976 positive (5.00%)
- **Test Set**: 19,524 records → 976 positive (5.00%)
✓ Perfect stratification maintained

### Example: nlb_mahajana_sampatha (Nearly Balanced)
- **Training Set**: 1,504 records → 713 positive (47.41%)
- **Validation Set**: 323 records → 153 positive (47.37%)
- **Test Set**: 323 records → 153 positive (47.37%)
✓ Perfect stratification maintained

## Recommended Balancing Strategy

### 1. XGBoost scale_pos_weight Parameter

**Primary Strategy**: Use XGBoost's built-in `scale_pos_weight` parameter to handle class imbalance.

#### Lottery-Specific Recommendations:

**Highly Imbalanced Lotteries (8 lotteries)**:
```python
scale_pos_weight = 19  # For dlb_shanida, dlb_super_ball, nlb_govisetha
scale_pos_weight = 18  # For dlb_ada_kotipathi
scale_pos_weight = 16  # For dlb_jayoda, dlb_sasiri, nlb_dhana_nidhanaya
scale_pos_weight = 15  # For nlb_mega_power
```

**Moderately Imbalanced Lotteries (4 lotteries)**:
```python
scale_pos_weight = 14  # For dlb_lagna_wasana, dlb_kapruka
scale_pos_weight = 13  # For nlb_suba_dawasak
scale_pos_weight = 10  # For nlb_handahana
```

**Balanced Lotteries (5 lotteries)**:
```python
scale_pos_weight = 2   # For dlb_jaya_sampatha, nlb_ada_sampatha, nlb_nlb_jaya
scale_pos_weight = 1   # For dlb_supiri_dhana_sampatha, nlb_mahajana_sampatha
```

#### Global Recommendations:
- **Conservative (all lotteries)**: `scale_pos_weight = 11` (mean)
- **Median approach**: `scale_pos_weight = 14` (median)
- **Aggressive (highly imbalanced)**: `scale_pos_weight = 19` (maximum)

### 2. Alternative Strategies (For Experimentation)

#### A. SMOTE (Synthetic Minority Over-sampling)
```python
from imblearn.over_sampling import SMOTE

smote = SMOTE(sampling_strategy='auto', random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)
```

**Pros**:
- Creates synthetic samples for minority class
- Works well with continuous features

**Cons**:
- Increases training data size significantly
- May overfit on small datasets
- Not recommended for lotteries with < 1,000 records

#### B. Class Weight Balancing
```python
from sklearn.utils.class_weight import compute_class_weight

class_weights = compute_class_weight(
    'balanced',
    classes=np.unique(y_train),
    y=y_train
)
```

**Pros**:
- Automatic calculation
- No data augmentation

**Cons**:
- Less flexible than scale_pos_weight
- Not directly available in XGBoost (use scale_pos_weight instead)

#### C. Ensemble of Under-sampled Models
```python
# Train multiple models on different under-sampled subsets
# Average predictions
```

**Pros**:
- Reduces training time
- Can improve generalization

**Cons**:
- Loses data information
- Requires ensemble infrastructure

### 3. Recommended Approach for Phase 3

**Model Training Pipeline**:

1. **Baseline Models** (Session 3.1):
   - Train without balancing to establish baseline
   - Train with `scale_pos_weight = median (14)`
   - Compare performance

2. **XGBoost Training** (Session 3.2):
   - Use lottery-specific `scale_pos_weight` values
   - Monitor precision-recall trade-off
   - Tune threshold for optimal F1-score

3. **Hyperparameter Tuning** (Session 3.3):
   - Include `scale_pos_weight` in hyperparameter search space
   - Search range: [1, 20]
   - Use stratified cross-validation

4. **Evaluation Metrics**:
   - **Primary**: F1-Score (balances precision and recall)
   - **Secondary**: Precision, Recall, AUC-ROC
   - **Avoid**: Accuracy (misleading with imbalanced data)

## Implementation Notes

### Code Template for XGBoost with scale_pos_weight

```python
import xgboost as xgb
from sklearn.metrics import f1_score, precision_score, recall_score

# Calculate scale_pos_weight from training data
neg_count = (y_train == 0).sum()
pos_count = (y_train == 1).sum()
scale_pos_weight = neg_count / pos_count

# Train XGBoost with balancing
xgb_model = xgb.XGBClassifier(
    objective='binary:logistic',
    scale_pos_weight=scale_pos_weight,  # Key parameter for imbalance
    max_depth=6,
    learning_rate=0.1,
    n_estimators=100,
    random_state=42
)

xgb_model.fit(X_train, y_train)

# Evaluate with appropriate metrics
y_pred = xgb_model.predict(X_val)
f1 = f1_score(y_val, y_pred)
precision = precision_score(y_val, y_pred)
recall = recall_score(y_val, y_pred)

print(f"F1-Score: {f1:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
```

### Threshold Tuning (Post-training)

```python
from sklearn.metrics import precision_recall_curve

# Get prediction probabilities
y_pred_proba = xgb_model.predict_proba(X_val)[:, 1]

# Find optimal threshold
precision, recall, thresholds = precision_recall_curve(y_val, y_pred_proba)
f1_scores = 2 * (precision * recall) / (precision + recall)
optimal_idx = np.argmax(f1_scores)
optimal_threshold = thresholds[optimal_idx]

print(f"Optimal threshold: {optimal_threshold:.4f}")

# Apply optimal threshold
y_pred_tuned = (y_pred_proba >= optimal_threshold).astype(int)
```

## Risks and Mitigation

### Risk 1: Overfitting on Minority Class
**Symptom**: High training F1, low validation F1
**Mitigation**:
- Use early stopping with validation set
- Apply regularization (max_depth, min_child_weight)
- Monitor validation metrics closely

### Risk 2: Poor Generalization on Imbalanced Test Set
**Symptom**: Model predicts too many positives
**Mitigation**:
- Tune decision threshold on validation set
- Use stratified evaluation
- Report confusion matrix

### Risk 3: Inconsistent Performance Across Lotteries
**Symptom**: Good performance on balanced lotteries, poor on imbalanced
**Mitigation**:
- Train lottery-specific models if needed
- Use lottery-specific scale_pos_weight values
- Consider ensemble of specialized models

## Next Steps

1. ✅ **COMPLETED**: Split all datasets with stratification
2. ✅ **COMPLETED**: Document class imbalance ratios
3. **TODO**: Implement XGBoost training pipeline with scale_pos_weight
4. **TODO**: Evaluate multiple scale_pos_weight values per lottery
5. **TODO**: Compare performance across imbalance categories
6. **TODO**: Document optimal scale_pos_weight values in final model

## References

- XGBoost Documentation: https://xgboost.readthedocs.io/en/latest/parameter.html#learning-task-parameters
- Imbalanced-learn: https://imbalanced-learn.org/stable/
- "Learning from Imbalanced Data" - He & Garcia (2009)

---

**Document Version**: 1.0
**Last Updated**: 2026-01-15
**Author**: Phase 1 Data Preprocessing Pipeline

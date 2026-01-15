# Explainability Analysis Guide - Phase 4

**Purpose**: Explain CatBoost model predictions using SHAP (global) and LIME (local)

**Assignment Requirement**: Apply at least one explainability method (we use TWO: SHAP + LIME)

---

## Quick Start (Google Colab - Recommended)

### 1. Setup

1. Open [Google Colab](https://colab.research.google.com)
2. Upload notebooks:
   - `notebooks/04_shap_analysis_colab.ipynb` (Global explanations)
   - `notebooks/05_lime_analysis_colab.ipynb` (Local explanations)
3. Enable GPU:
   - Menu: **Runtime → Change runtime type**
   - Hardware accelerator: **GPU**
   - Click **Save**
4. Verify GPU: Run first cell (`!nvidia-smi`)

### 2. Upload Data to Google Drive

**Option A: Use Existing Files** (If you already ran training notebooks)

Your Google Drive should already have:
```
/MyDrive/lottery_analyzer/
├── data/splits/          # Test data (17 lotteries × 3 files)
├── models/
│   └── best_model.cbm   # Best tuned model
└── outputs/results/
    └── catboost_feature_importance.csv
```

**Option B: Upload Fresh** (If starting new)

1. Download from local:
   - `data/splits/` (all `*_test.csv` files)
   - `models/best_model.cbm`
   - `outputs/results/catboost_feature_importance.csv`

2. Upload to Google Drive:
   ```
   /MyDrive/lottery_analyzer/
   ├── data/splits/
   ├── models/
   └── outputs/results/
   ```

### 3. Run Notebooks

**A. SHAP Notebook (04_shap_analysis_colab.ipynb)** - Runtime: 5-10 min

1. Mount Google Drive
2. Run all cells in order
3. Wait for "SHAP values calculated successfully"
4. Check outputs in `/MyDrive/lottery_analyzer/outputs/explainability/shap/`

**B. LIME Notebook (05_lime_analysis_colab.ipynb)** - Runtime: 3-5 min

1. Mount Google Drive (if not already)
2. Run all cells in order
3. Wait for "LIME explanations generated"
4. Check outputs in `/MyDrive/lottery_analyzer/outputs/explainability/lime/`

### 4. Download Results

**SHAP Outputs** (12 files):
```
/MyDrive/lottery_analyzer/outputs/explainability/shap/
├── shap_values.npy
├── shap_sample_data.csv
├── shap_feature_importance.csv
├── shap_summary_plot.png
├── shap_bar_plot.png
├── shap_dependence_plots.png
├── shap_force_plot_positive.png
├── shap_force_plot_negative.png
├── shap_waterfall_plot_positive.png
├── importance_comparison.csv
├── importance_comparison_plot.png
└── shap_analysis_report.json
```

**LIME Outputs** (9 files):
```
/MyDrive/lottery_analyzer/outputs/explainability/lime/
├── lime_positive_1.png
├── lime_positive_2.png
├── lime_positive_3.png
├── lime_negative_1.png
├── lime_negative_2.png
├── lime_negative_3.png
├── lime_feature_importance.csv
├── lime_shap_comparison.csv
├── lime_shap_comparison.png
└── lime_analysis_report.json
```

**Place in Local Codebase:**
```
D:\Temp\lottery_analyzer\outputs\explainability\shap\
D:\Temp\lottery_analyzer\outputs\explainability\lime\
```

---

## What Each Plot Shows

### 1. SHAP Summary Plot (Beeswarm)
**File**: `shap_summary_plot.png`

**Shows**:
- Global feature importance (Y-axis ranked top to bottom)
- Distribution of SHAP values for each feature
- Feature values (red = high, blue = low)
- Impact direction (right = increases "Appear", left = decreases)

**How to Read**:
- Top features have highest impact on predictions
- Color + position shows feature value effect
- Wide spread = feature impacts vary across instances

### 2. SHAP Bar Plot
**File**: `shap_bar_plot.png`

**Shows**:
- Mean absolute SHAP value for each feature
- Pure magnitude-based importance ranking
- No direction or value information

**How to Read**:
- Taller bar = more important feature
- Simpler than beeswarm, focuses on magnitude

### 3. SHAP Dependence Plots (Top 5)
**File**: `shap_dependence_plots.png`

**Shows**:
- X-axis: Feature value
- Y-axis: SHAP value (impact on prediction)
- Color: Interaction feature (auto-selected)

**How to Read**:
- Slope shows relationship (positive/negative)
- Color gradient reveals interactions
- Scatter shows variability

### 4. SHAP Force Plots
**Files**: `shap_force_plot_positive.png`, `shap_force_plot_negative.png`

**Shows**:
- Individual prediction explanation
- Base value (average prediction)
- Features pushing toward "Appear" (red)
- Features pushing toward "Not Appear" (blue)
- Final prediction value

**How to Read**:
- Start at base value, features push left/right
- Red arrows increase appearance probability
- Blue arrows decrease appearance probability

### 5. SHAP Waterfall Plot
**File**: `shap_waterfall_plot_positive.png`

**Shows**:
- Same as force plot but vertical format
- Shows cumulative effect of features
- Easier to see exact contribution values

**How to Read**:
- Start at E[f(x)] (expected value)
- Each bar adds/subtracts from prediction
- End at f(x) (actual prediction)

### 6. Importance Comparison
**Files**: `importance_comparison.csv`, `importance_comparison_plot.png`

**Shows**:
- Side-by-side comparison: CatBoost vs SHAP importance
- Both normalized to 0-100 scale

**How to Read**:
- High agreement = reliable feature
- SHAP high, CatBoost low = high impact per use
- CatBoost high, SHAP low = used often, low impact

---

## Expected Runtime

**Google Colab (Tesla T4 GPU)**:
- Total: 5-10 minutes
- SHAP calculation: 2-5 minutes
- Visualizations: 2-3 minutes
- Report generation: <1 minute

**Local (CPU)**:
- Total: 15-30 minutes
- SHAP calculation: 10-20 minutes
- Visualizations: 3-5 minutes
- Report generation: <1 minute

---

## Troubleshooting

### Issue: "best_model.cbm not found"
**Solution**:
- Verify file exists in `/content/drive/MyDrive/lottery_analyzer/models/`
- Re-run hyperparameter tuning notebook (03) if missing

### Issue: "SHAP calculation taking too long"
**Solution**:
- Reduce `SAMPLE_SIZE` in cell 7 (default: 10,000)
- Try 5,000 or 2,000 for faster computation
- Quality slightly decreases but acceptable for assignment

### Issue: "Out of memory"
**Solution**:
- Restart runtime: Runtime → Restart runtime
- Reduce `SAMPLE_SIZE` to 5,000
- Clear outputs: Edit → Clear all outputs

### Issue: "Drive mount failed"
**Solution**:
- Check Google account permissions
- Try re-mounting: `drive.mount('/content/drive', force_remount=True)`
- Verify files uploaded to correct Drive location

### Issue: "Plots not rendering"
**Solution**:
- Check `plt.show()` is called after each plot
- Try restarting runtime
- Download PNG files directly from Drive

---

## Key Insights to Document

After running the notebook, document these findings for your assignment:

### 1. Top 5 Most Important Features
Example:
1. `draw_sequence` - Position in lottery history
2. `current_gap` - Draws since last appearance
3. `days_since_last` - Calendar time since appearance
4. `appearance_rate` - Historical frequency
5. `draw_id` - Specific draw identifier

### 2. Feature Relationships
From dependence plots:
- How does `current_gap` affect predictions?
- Is relationship linear or non-linear?
- Are there interaction effects?

### 3. Individual Predictions
From force plots:
- Why did model predict number would appear?
- Which features contributed most?
- Were predictions correct?

### 4. Model Interpretability
- Do SHAP explanations make intuitive sense?
- Do they align with domain knowledge (lottery theory)?
- Are there any surprising findings?

### 5. SHAP vs CatBoost Comparison
- Which features rank high in both methods?
- Are there discrepancies? Why?
- What does this tell us about the model?

---

## Integration with Assignment Report

### Section: Model Explainability (Phase 4)

**Include**:

1. **Methodology**:
   - "SHAP (SHapley Additive exPlanations) was used to interpret model predictions"
   - "TreeExplainer optimized for CatBoost gradient boosting trees"
   - "10,000 test instances sampled for SHAP value calculation"

2. **Global Importance** (Figure: Summary Plot):
   - "Top 5 features account for XX% of prediction impact"
   - "Temporal features dominate: draw_sequence, current_gap, days_since_last"
   - "Frequency features secondary: appearance_rate, frequency_last_30"

3. **Feature Relationships** (Figure: Dependence Plots):
   - "Current gap shows negative correlation: longer gap → lower probability"
   - "Appearance rate shows positive correlation: higher rate → higher probability"
   - "Interaction effects detected between [feature X] and [feature Y]"

4. **Individual Explanations** (Figure: Force/Waterfall Plots):
   - "Model predictions are explainable at instance level"
   - "Example: Number predicted to appear due to low current_gap and high appearance_rate"
   - "Demonstrates model transparency and interpretability"

5. **Validation** (Figure: Comparison Plot):
   - "SHAP importance aligns with CatBoost native importance (correlation: X.XX)"
   - "Confirms feature engineering choices were appropriate"
   - "No evidence of model relying on spurious correlations"

---

## Next Steps After SHAP Analysis

1. Review all plots and understand insights
2. Document findings in assignment report
3. Prepare Phase 5: Web Application (optional)
4. Write critical discussion (Phase 6)
5. Compile final report (Phase 7)

---

## Additional Resources

**SHAP Documentation**: https://shap.readthedocs.io/
**Paper**: Lundberg & Lee (2017) - "A Unified Approach to Interpreting Model Predictions"
**Tutorial**: https://christophm.github.io/interpretable-ml-book/shap.html

**Assignment Document**: [docs/MODEL_INTERPRETATION.md](docs/MODEL_INTERPRETATION.md)

---

**For detailed SHAP theory and interpretation, see [MODEL_INTERPRETATION.md](docs/MODEL_INTERPRETATION.md)**

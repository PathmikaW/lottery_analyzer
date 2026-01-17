# Sri Lankan Lottery ML Analyzer

**MSc AI - Applied Machine Learning Assignment**

A machine learning system for predicting Sri Lankan lottery number appearances using CatBoost with SHAP and LIME explainability.

**GitHub Repository**: https://github.com/PathmikaW/lottery_analyzer

---

## Project Summary

| Metric | Value |
|--------|-------|
| Algorithm | CatBoost (Gradient Boosting) |
| F1-Score | 25.92% (3.87x better than random) |
| Lotteries | 17 (8 NLB + 9 DLB) |
| Total Draws | 8,085 |
| ML Records | 485,094 |
| Features | 21 |
| Date Range | 2021-04-01 to 2026-01-12 |
| Explainability | SHAP + LIME (65% agreement) |

---

## Quick Start

### Backend
```bash
cd lottery_analyzer
lottery_env\Scripts\activate          # Windows
python backend/main.py
# API runs at http://localhost:8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
# App runs at http://localhost:5173
```

---

## Project Structure

```
lottery_analyzer/
├── backend/main.py              # FastAPI backend
├── frontend/                    # React + TypeScript + TailwindCSS
│   └── src/
│       ├── pages/              # Home, Predict, Results, Explain, About
│       └── components/         # UI components
├── src/
│   ├── scrapers/               # NLB and DLB web scrapers
│   └── preprocessing/          # Data pipeline (validation, cleaning, features, splitting)
├── notebooks/                   # Jupyter notebooks (run on Google Colab)
│   ├── 01_baseline_models_colab.ipynb
│   ├── 02_catboost_training_colab.ipynb
│   ├── 03_hyperparameter_tuning_colab.ipynb
│   ├── 04_shap_analysis_colab.ipynb
│   └── 05_lime_analysis_colab.ipynb
├── data/
│   ├── raw/                    # Original scraped CSV files (17 lotteries)
│   ├── processed/              # Feature-engineered data
│   └── splits/                 # Train/val/test splits (stratified)
├── models/best_model.cbm        # Trained CatBoost model
├── outputs/
│   ├── statistics/             # data_quality_stats.json, split_stats.json
│   ├── results/                # Model results, baseline comparison
│   └── explainability/         # SHAP and LIME outputs
└── docs/                        # Documentation
```

---

## Assignment Requirements

| Section | Marks | Status | Evidence |
|---------|-------|--------|----------|
| 1. Problem Definition & Dataset | 15 | COMPLETED | 17 lotteries, 8,085 draws, 485K records, 21 features |
| 2. Algorithm Selection | 15 | COMPLETED | CatBoost (not taught in lectures) |
| 3. Model Training & Evaluation | 20 | COMPLETED | 25.92% F1-Score, baseline comparison, hyperparameter tuning |
| 4. Explainability & Interpretation | 20 | COMPLETED | SHAP + LIME analysis, feature importance |
| 5. Critical Discussion | 10 | COMPLETED | Limitations, ethics, bias discussed |
| 6. Report Quality | 10 | COMPLETED | Professional documentation |
| 7. BONUS: Front-End Integration | 10 | COMPLETED | React + FastAPI web application |

**Total: 90 + 10 Bonus = 100 marks**

---

## Dataset Details

### Data Sources
- **NLB** (National Lotteries Board): 8 lotteries, 1,310 draws
- **DLB** (Development Lotteries Board): 9 lotteries, 6,775 draws

### Class Distribution
- **Positive (appeared)**: 32,511 (6.70%)
- **Negative (not appeared)**: 452,583 (93.30%)
- **Imbalance Ratio**: 1:13.92

### 21 Engineered Features
1. **Frequency Features (6)**: frequency_last_10/30/50, frequency_all_time, appearance_rate, days_since_last
2. **Temporal Features (5)**: day_of_week, is_weekend, month, week_of_year, draw_sequence
3. **Statistical Features (6)**: mean_gap, std_gap, min_gap, max_gap, current_gap, draw_id
4. **Hot/Cold Features (4)**: is_hot, is_cold, temperature_score, trend

---

## Model Results

| Model | F1-Score | Precision | Recall | ROC-AUC |
|-------|----------|-----------|--------|---------|
| Random Baseline | 6.70% | 6.70% | 6.70% | 50.00% |
| Logistic Regression | 18.01% | 12.32% | 33.50% | 60.48% |
| Random Forest | 25.95% | 35.09% | 20.58% | 59.81% |
| CatBoost (Default) | 25.53% | 30.04% | 22.20% | 61.01% |
| **CatBoost (Tuned)** | **25.92%** | **32.66%** | **21.48%** | **60.92%** |

### Best Configuration
- iterations: 500 (early stopped at 13)
- learning_rate: 0.01
- depth: 6
- l2_leaf_reg: 3

---

## Explainability Results

### Top 5 Features (SHAP)
| Rank | Feature | Mean |SHAP| |
|------|---------|---------------|
| 1 | appearance_rate | 0.0114 |
| 2 | days_since_last | 0.0074 |
| 3 | draw_sequence | 0.0043 |
| 4 | frequency_last_10 | 0.0030 |
| 5 | draw_id | 0.0027 |

### SHAP vs LIME Agreement
- Top 2 features: Perfect agreement
- Overall: 65%+ agreement on important features

---

## Technology Stack

| Layer | Technology |
|-------|------------|
| ML Algorithm | CatBoost |
| Explainability | SHAP, LIME |
| Backend | FastAPI (Python) |
| Frontend | React + TypeScript + TailwindCSS |
| Data Processing | pandas, numpy, scikit-learn |
| Visualization | matplotlib, seaborn, Recharts |
| Build Tool | Vite |

---

## Installation

### Prerequisites
- Python 3.9+
- Node.js 18+

### Setup

```bash
# Clone repository
git clone https://github.com/PathmikaW/lottery_analyzer.git
cd lottery_analyzer

# Create and activate virtual environment
python -m venv lottery_env
lottery_env\Scripts\activate          # Windows
source lottery_env/bin/activate       # Linux/Mac

# Install Python dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd frontend
npm install
```

---

## Important Disclaimer

**Educational Purpose Only**
- This is an academic machine learning assignment
- NOT intended for commercial gambling or betting
- Lottery outcomes are inherently random
- No prediction system can guarantee wins
- Use responsibly for learning purposes only

---

## References

1. Prokhorenkova, L., et al. (2018). "CatBoost: unbiased boosting with categorical features." NeurIPS 2018.
2. Lundberg, S. M., & Lee, S. I. (2017). "A Unified Approach to Interpreting Model Predictions." NeurIPS 2017.
3. Ribeiro, M. T., et al. (2016). "Why Should I Trust You?: Explaining the Predictions of Any Classifier." KDD 2016.
4. National Lotteries Board Sri Lanka: https://www.nlb.lk
5. Development Lotteries Board Sri Lanka: https://www.dlb.lk

---

**Author**: MSc AI Student
**Date**: January 2026
**Course**: Applied Machine Learning Assignment

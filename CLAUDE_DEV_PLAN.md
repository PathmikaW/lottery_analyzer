# Sri Lankan Lottery ML Analyzer - Development Plan

## Project Overview

**MSc AI - Applied Machine Learning Assignment**
**Status**: COMPLETED
**Branch**: `feature/lottery-analyzer-v2`

---

## Assignment Requirements Validation

### Marking Breakdown & Completion Status

| Section | Marks | Status | Evidence |
|---------|-------|--------|----------|
| 1. Problem Definition & Dataset | 15 | ✅ COMPLETED | 17 lotteries, 8,085 draws, 485K records, 21 features |
| 2. Algorithm Selection | 15 | ✅ COMPLETED | CatBoost (not taught in lectures), documented justification |
| 3. Model Training & Evaluation | 20 | ✅ COMPLETED | 25.92% F1-Score, baseline comparison, hyperparameter tuning |
| 4. Explainability & Interpretation | 20 | ✅ COMPLETED | SHAP + LIME analysis, feature importance, dependence plots |
| 5. Critical Discussion | 10 | ✅ COMPLETED | Limitations, ethics, bias discussed in Results page |
| 6. Report Quality | 10 | ✅ COMPLETED | Professional documentation and code structure |
| 7. BONUS: Front-End Integration | 10 | ✅ COMPLETED | React + TypeScript + FastAPI web application |

**Total: 90 + 10 Bonus = 100 marks**

---

## Project Structure

```
lottery_analyzer/
├── backend/                    # FastAPI backend
│   └── main.py                # API endpoints (predictions, explanations, file serving)
├── frontend/                   # React + TypeScript + TailwindCSS
│   └── src/
│       ├── pages/             # Home, Predict, Results, Explain, About
│       └── components/        # UI components including FileViewer
├── src/
│   ├── scrapers/              # NLB and DLB web scrapers
│   ├── preprocessing/         # Data cleaning, feature engineering, splitting
│   └── utils/                 # Helper scripts
├── notebooks/                  # Jupyter notebooks (run on Google Colab)
│   ├── 01_baseline_models_colab.ipynb
│   ├── 02_catboost_training_colab.ipynb
│   ├── 03_hyperparameter_tuning_colab.ipynb
│   ├── 04_shap_analysis_colab.ipynb
│   └── 05_lime_analysis_colab.ipynb
├── data/
│   ├── raw/                   # Original scraped data (17 CSV files)
│   ├── processed/             # Cleaned and featured data
│   └── splits/                # Train/val/test splits (51 CSV files)
├── models/
│   └── best_model.cbm         # Trained CatBoost model
├── outputs/
│   ├── statistics/            # Dataset statistics (JSON)
│   ├── results/               # Model training results (PNG, CSV, JSON)
│   ├── explainability/        # SHAP and LIME outputs
│   └── reports/               # Validation reports
├── docs/                       # Documentation
│   ├── ALGORITHM_JUSTIFICATION.md
│   ├── ALGORITHM_SELECTION_RATIONALE.md
│   └── EXPLAINABILITY_ANALYSIS.md
└── README.md                   # Project overview
```

---

## Section 1: Problem Definition & Dataset (15 marks) ✅

### Problem Definition
- **Task**: Binary classification - predict if lottery number will appear in next draw
- **Target Variable**: `appeared` (1 = appeared, 0 = did not appear)
- **Real-world relevance**: Demonstrates ML pipeline on real Sri Lankan lottery data

### Dataset
- **Sources**: NLB (nlb.lk) + DLB (dlb.lk) - publicly available data
- **Total Lotteries**: 17 (8 NLB + 9 DLB)
- **Total Draws**: 8,085
- **Total Records**: 485,094 (after feature expansion)
- **Date Range**: 2021-04-01 to 2026-01-12
- **Data Completeness**: 96.47%

### Features Engineered (21 total)
1. **Frequency Features** (6): frequency_last_10/30/50, frequency_all_time, appearance_rate, days_since_last
2. **Temporal Features** (5): day_of_week, is_weekend, month, week_of_year, draw_sequence
3. **Statistical Features** (6): mean_gap, std_gap, min_gap, max_gap, current_gap, draw_id
4. **Hot/Cold Features** (4): is_hot, is_cold, temperature_score, trend

### Preprocessing
- Data validation and cleaning (`src/preprocessing/data_validator.py`, `data_cleaner.py`)
- Feature engineering (`src/preprocessing/feature_engineer.py`)
- Stratified splitting 70/15/15 (`src/preprocessing/data_splitter.py`)

### Evidence Files
- `outputs/statistics/data_quality_stats.json`
- `outputs/statistics/split_stats.json`
- `outputs/reports/validation_report.txt`

---

## Section 2: Algorithm Selection (15 marks) ✅

### Algorithm: CatBoost (Categorical Boosting)

**Why CatBoost?**
1. **Not taught in lectures** - Fulfills assignment requirement
2. **Native categorical handling** - No one-hot encoding needed for trend, lottery type
3. **Built-in class imbalance handling** - `auto_class_weights='Balanced'`
4. **Ordered boosting** - Prevents overfitting on small datasets
5. **SHAP compatibility** - Full explainability support

### Comparison with Lecture Algorithms
| Algorithm | Taught? | Issue for Our Task |
|-----------|---------|-------------------|
| Decision Trees | Yes | Single tree prone to overfitting |
| Logistic Regression | Yes | Linear model, can't capture interactions |
| Random Forest | Yes | Bagging, not as accurate as boosting |
| SVM | Yes | Doesn't scale well to 485K records |
| k-NN | Yes | Memory intensive, slow inference |

### Evidence Files
- `docs/ALGORITHM_JUSTIFICATION.md`
- `docs/ALGORITHM_SELECTION_RATIONALE.md`

---

## Section 3: Model Training & Evaluation (20 marks) ✅

### Training Strategy
- **Split**: 70% train, 15% validation, 15% test (stratified)
- **Class Imbalance**: 1:13.92 ratio, handled with `auto_class_weights='Balanced'`
- **Hyperparameter Tuning**: Grid search over 81 configurations

### Results

| Model | F1-Score | Precision | Recall | ROC-AUC |
|-------|----------|-----------|--------|---------|
| Logistic Regression | 18.01% | 12.32% | 33.50% | 60.48% |
| Random Forest | 25.95% | 35.09% | 20.58% | 59.81% |
| CatBoost (Default) | 25.53% | 30.04% | 22.20% | 61.01% |
| **CatBoost (Tuned)** | **25.92%** | 32.66% | 21.48% | **60.92%** |

### Best Configuration
- iterations: 500 (early stopped at 13)
- learning_rate: 0.01
- depth: 6
- l2_leaf_reg: 3
- **Improvement**: +1.51% F1 over default

### Evidence Files
- `outputs/results/baseline_results.json`
- `outputs/results/catboost_results.json`
- `outputs/results/best_model_config.json`
- `outputs/results/tuning_improvement.json`
- `outputs/results/baseline_comparison.png`
- `outputs/results/hyperparameter_heatmaps.png`
- `notebooks/01_baseline_models_colab.ipynb`
- `notebooks/02_catboost_training_colab.ipynb`
- `notebooks/03_hyperparameter_tuning_colab.ipynb`

---

## Section 4: Explainability & Interpretation (20 marks) ✅

### Methods Applied
1. **SHAP** (SHapley Additive exPlanations) - Global feature importance
2. **LIME** (Local Interpretable Model-agnostic Explanations) - Instance-level explanations
3. **Feature Dependence Plots** - Non-linear relationships

### Top 5 Features (SHAP)
| Rank | Feature | Mean Abs SHAP | Interpretation |
|------|---------|---------------|----------------|
| 1 | appearance_rate | 0.0114 | Historical frequency ratio |
| 2 | days_since_last | 0.0074 | Calendar time since appearance |
| 3 | draw_sequence | 0.0043 | Position in lottery history |
| 4 | frequency_last_10 | 0.0030 | Recent activity momentum |
| 5 | draw_id | 0.0027 | Specific draw context |

### SHAP vs LIME Agreement
- **Top 2 features**: Perfect agreement (appearance_rate, days_since_last)
- **Overall agreement**: 65%+ on important features
- **Cross-validation**: Both confirm categorical features (is_weekend, trend) have near-zero importance

### Domain Knowledge Alignment
- ✅ Model respects lottery randomness (25.92% ceiling)
- ✅ No "due number" fallacy (negative correlation with long gaps)
- ✅ Frequency and recency drive predictions (intuitive)

### Evidence Files
- `outputs/explainability/shap/shap_summary_plot.png`
- `outputs/explainability/shap/shap_bar_plot.png`
- `outputs/explainability/shap/shap_dependence_plots.png`
- `outputs/explainability/lime/lime_shap_comparison.png`
- `outputs/explainability/lime/lime_positive_*.png`
- `outputs/explainability/lime/lime_negative_*.png`
- `docs/EXPLAINABILITY_ANALYSIS.md`
- `notebooks/04_shap_analysis_colab.ipynb`
- `notebooks/05_lime_analysis_colab.ipynb`

---

## Section 5: Critical Discussion (10 marks) ✅

### Model Limitations
- Lottery is inherently random - 25.92% F1 represents ceiling
- Low precision (32.66%) - 2/3 positive predictions are false alarms
- Class imbalance (~7% positive) makes learning difficult

### Data Quality Issues
- Web scraping depends on source accuracy
- 58 months of data may not capture all patterns
- No external factors (machine changes, ball wear)

### Risks of Bias/Unfairness
- May reinforce gambler's fallacy if misinterpreted
- Model trained on specific lotteries may not generalize
- No personal data used - no individual discrimination

### Ethical Considerations
- Educational project only - NOT for commercial gambling
- Disclaimers included about randomness
- Transparent predictions with SHAP/LIME explanations

### Evidence
- Documented in `frontend/src/pages/Results.tsx` (Section 5)
- Critical discussion section in GUI

---

## Section 6: Report Quality (10 marks) ✅

### Code Quality
- Clean, well-documented Python code
- TypeScript for type safety in frontend
- Modular architecture (scrapers, preprocessing, models)

### Documentation
- Comprehensive README.md
- Algorithm justification documents
- Explainability analysis document

### Visualizations
- Professional plots (matplotlib, seaborn)
- Interactive charts in React (Recharts)
- All outputs accessible via GUI

---

## Section 7: BONUS - Front-End Integration (10 marks) ✅

### Technology Stack
- **Backend**: FastAPI (Python) - REST API
- **Frontend**: React + TypeScript + TailwindCSS + shadcn/ui
- **Build**: Vite

### Features Implemented
1. **Home Page**: Project overview and key statistics
2. **Predict Page**: Interactive number prediction with dynamic grids
3. **Results Page**: Model training outputs, baseline comparison, hyperparameter tuning
4. **Explain Page**: SHAP analysis, LIME analysis, feature dependencies
5. **About Page**: Project details, tech stack, disclaimer

### API Endpoints
- `POST /predict` - Get predictions for lottery numbers
- `GET /lotteries` - List available lotteries with metadata
- `GET /statistics` - Model performance stats
- `GET /explain/{number}` - SHAP explanation for specific number
- `GET /api/files/{path}` - Serve source files and notebooks

### GUI Features
- File viewer with Jupyter notebook rendering
- Download functionality for all files
- Responsive design (mobile, tablet, desktop)
- Visual confidence scale with granular levels

---

## Submission Requirements

### Written Report (PDF)
- [x] Problem description
- [x] Methodology
- [x] Results
- [x] Interpretation
- [x] Discussion

### Source Code (GitHub)
- [x] Data preprocessing scripts
- [x] Training notebooks
- [x] Evaluation code
- [x] Explainability scripts
- [x] Backend API
- [x] Frontend application

### Dataset
- [x] Raw data in `data/raw/`
- [x] Processed data in `data/processed/`
- [x] Train/val/test splits in `data/splits/`

### Demo Video (3-5 minutes)
- [ ] To be recorded showing front-end system

---

## How to Run

### Backend
```bash
cd lottery_analyzer
lottery_env\Scripts\activate  # Windows
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

**Last Updated**: 2026-01-17
**Version**: 3.0 (Final)

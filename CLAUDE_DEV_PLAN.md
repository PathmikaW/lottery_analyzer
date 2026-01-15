# Sri Lankan Lottery ML Analyzer - Claude Development Plan

## Project Overview

**MSc AI - Applied Machine Learning Assignment**
**Timeline**: Multi-session development with Claude Code
**Current Branch**: `feature/lottery-analyzer-v2`

---

## Assignment Requirements (90 marks + 10 bonus)

### Marking Breakdown

1. **Problem Definition & Dataset** (15 marks)
2. **New Algorithm Selection** (15 marks) - **CatBoost**
3. **Model Training & Evaluation** (20 marks)
4. **Explainability & Interpretation** (20 marks) - SHAP + Feature Importance
5. **Critical Discussion** (10 marks)
6. **Report Quality** (10 marks)
7. **BONUS: Front-End Integration** (10 marks) - Streamlit

### Key Constraints

- **Algorithm**: Must NOT be taught in lectures (Random Forests, SVM, Bayesian Learning are taught)
- **NO Deep Learning**
- **NO Image Processing**
- **Local Dataset**: Sri Lankan lotteries (NLB + DLB)
- **XAI Required**: At least one explainability method

---

## Data Sources & Current Status

### National Lotteries Board (NLB) - 8 Lotteries

- URL: https://www.nlb.lk
- **Status**: ✅ Both draws and prizes scraped
- Mahajana Sampatha, Govisetha, Dhana Nidhanaya, Handahana, Mega Power, Ada Sampatha, Suba-dawasak, NLB Jaya

### Development Lotteries Board (DLB) - 9 Lotteries

- URL: https://www.dlb.lk
- **Status**: ✅ Draws scraped, ❌ No prize data available
- Ada Kotipathi, Shanida, Lagna Wasana, Supiri Dhana Sampatha, Super Ball, Kapruka, Jayoda, Sasiri, Jaya Sampatha

### Current Dataset

- **Total Lotteries**: 17 (NLB: 8, DLB: 9)
- **Total Draws**: 8,085
- **Total Records After Feature Engineering**: 485,094
- **Date Range**: 2021-04-01 to 2026-01-12 (58.2 months)
- **Splits**: 70% train, 15% val, 15% test (stratified)
- **Class Imbalance**: 1:13.92 overall (range: 1:1.11 to 1:19.00)

---

## Technical Stack (Keep Simple & Clean)

### Machine Learning

```
Primary Algorithm: CatBoost (not taught in lectures)
  - Handles categorical features natively
  - Built-in class imbalance handling
  - Better than XGBoost for lottery data

Baseline Comparisons: Logistic Regression, Random Forest
Explainability: SHAP values, Feature Importance
Data Processing: pandas, numpy, scikit-learn
Visualization: matplotlib, seaborn (minimal)
```

### Front-End (BONUS - After Phase 4)

```
Backend: FastAPI (Python)
  - RESTful API endpoints
  - Load trained CatBoost model
  - Serve predictions + SHAP explanations

Frontend: React + Vite
  - Simple, clean UI
  - Lottery selector, date picker
  - Display predictions with probabilities
  - Show SHAP explanations
  - No complex state management needed
```

---

## Feature Engineering (20 Features) ✅ COMPLETED

### Category 1: Frequency Features (6)

1. `frequency_last_10` - Appearances in last 10 draws
2. `frequency_last_30` - Appearances in last 30 draws
3. `frequency_last_50` - Appearances in last 50 draws
4. `frequency_all_time` - Total appearances so far
5. `appearance_rate` - Percentage of all draws
6. `days_since_last` - Days since last appearance

### Category 2: Temporal Features (5)

7. `day_of_week` - Monday(0) to Sunday(6)
8. `is_weekend` - Binary (Saturday/Sunday = 1)
9. `month` - 1-12
10. `week_of_year` - 1-52
11. `draw_sequence` - Sequential draw number

### Category 3: Statistical Features (5)

12. `mean_gap` - Average days between appearances
13. `std_gap` - Standard deviation of gaps
14. `min_gap` - Minimum gap between appearances
15. `max_gap` - Maximum gap
16. `current_gap` - Same as days_since_last

### Category 4: Hot/Cold Features (4)

17. `is_hot` - Binary (top 20% frequency in last 30 draws)
18. `is_cold` - Binary (bottom 20% frequency)
19. `temperature_score` - Normalized 0-100 score
20. `trend` - Categorical (heating_up/cooling_down/stable)

**Target Variable**: `appeared` (binary: 1=appeared in draw, 0=did not appear)

---

## Development Phases

## ✅ PHASE 1: Data Collection & Preprocessing (COMPLETED)

### Session 1.1: Scraper Development ✅

- [X] NLB lottery scraper (draws + prizes)
- [X] DLB lottery scraper (draws only)
- [X] Automated data collection for 17 lotteries
- [X] Commit: `feat: add prize data scraping script for NLB lotteries`

### Session 1.2: Data Validation & Cleaning ✅

- [X] Data validator (checks missing values, duplicates, ranges, date gaps)
- [X] Data cleaner (standardizes dates, parses numbers, removes duplicates)
- [X] Data quality report (96.47% completeness)
- [X] Commit: `feat(preprocessing): implement data validation and cleaning pipeline`

### Session 1.3: Feature Engineering ✅

- [X] 20 features engineered across 4 categories
- [X] Expanded 8,085 draws → 485,094 records
- [X] Each record represents: "Will number X appear in draw Y?"
- [X] Commit: `feat(preprocessing): implement comprehensive feature engineering`

### Session 1.4: Data Splitting & Balancing ✅

- [X] Stratified train/val/test split (70/15/15)
- [X] 51 CSV files generated (17 lotteries × 3 splits)
- [X] Class imbalance analysis and strategy
- [X] Commit: `feat(preprocessing): implement stratified data splitting`

---

## PHASE 2: Algorithm Selection & Justification (15 MARKS)

**Goal**: Brief justification for CatBoost (1-2 pages max)

### Session 2.1: Algorithm Selection Document

**Tasks**:

- [X] Document why CatBoost was chosen
- [X] Compare with lecture-taught algorithms (Random Forest, SVM, Bayesian)
- [X] Explain advantages for lottery prediction
- [X] Keep it short and clear (no lengthy comparisons)

**Key Points to Cover**:

1. **Why CatBoost**:

   - Not taught in lectures (unlike XGBoost which might be covered)
   - Native categorical feature handling (trend, day_of_week, lottery)
   - Built-in class imbalance handling
   - Faster training than XGBoost
   - Better for small-to-medium datasets
2. **Differs from Standard Models**:

   - vs Decision Trees: Gradient boosting ensemble (stronger)
   - vs Logistic Regression: Non-linear, handles interactions
   - vs Random Forest: Ordered boosting (better accuracy)
   - vs SVM: Scales better, handles categorical features

**Deliverable**: `docs/ALGORITHM_JUSTIFICATION.md` (concise)

---

## PHASE 3: Model Training & Evaluation (20 MARKS)

**Goal**: Train models, evaluate performance, generate results

### Session 3.1: Baseline Models

**Tasks**:

- [ ] Train Logistic Regression (baseline)
- [ ] Train Random Forest (baseline)
- [ ] Evaluate both on validation set
- [ ] Save metrics (F1, Precision, Recall, AUC-ROC)
- [ ] Quick comparison table

**Deliverable**: `src/models/baseline_models.py`

### Session 3.2: CatBoost Training

**Tasks**:

- [ ] Install CatBoost: `pip install catboost`
- [ ] Train CatBoost with class imbalance handling
- [ ] Use categorical features directly (no one-hot encoding)
- [ ] Evaluate on validation set
- [ ] Compare with baselines

**Key Parameters**:

```python
from catboost import CatBoostClassifier

model = CatBoostClassifier(
    iterations=1000,
    learning_rate=0.05,
    depth=6,
    loss_function='Logloss',
    auto_class_weights='Balanced',  # Handles imbalance
    cat_features=['trend', 'lottery'],  # Specify categorical
    random_seed=42,
    verbose=100
)
```

**Deliverable**: `src/models/catboost_model.py`

### Session 3.3: Hyperparameter Tuning

**Tasks**:

- [ ] Grid search on key parameters:
  - `iterations`: [500, 1000, 1500]
  - `learning_rate`: [0.01, 0.05, 0.1]
  - `depth`: [4, 6, 8]
- [ ] Use validation set for selection
- [ ] Save best model
- [ ] Final evaluation on test set

**Deliverable**: `src/models/hyperparameter_tuning.py`

### Session 3.4: Results & Metrics

**Tasks**:

- [ ] Generate confusion matrix
- [ ] Plot ROC curves
- [ ] F1-Score, Precision, Recall table
- [ ] Per-lottery performance breakdown
- [ ] Save all results to `outputs/results/`

**Metrics to Report**:

- F1-Score (primary metric for imbalanced data)
- Precision (minimize false positives)
- Recall (maximize true positives)
- AUC-ROC
- Confusion matrix

**Deliverable**: Results tables + plots in `outputs/results/`

---

## PHASE 4: Explainability & Interpretation (20 MARKS)

**Goal**: Apply XAI techniques to understand the model

### Session 4.1: SHAP Analysis

**Tasks**:

- [ ] Install SHAP: `pip install shap`
- [ ] Generate SHAP values for test set
- [ ] Create SHAP summary plot (top 20 features)
- [ ] SHAP dependence plots for top 5 features
- [ ] Interpret: Which features drive predictions?

**Deliverable**: `src/explainability/shap_analysis.py`

### Session 4.2: Feature Importance

**Tasks**:

- [ ] Extract CatBoost native feature importance
- [ ] Plot importance bar chart
- [ ] Compare with SHAP values
- [ ] Document top 10 most important features

**Deliverable**: Feature importance plots in `outputs/explainability/`

### Session 4.3: Interpretation Document

**Tasks**:

- [ ] What did the model learn?
- [ ] Which features matter most?
- [ ] Does it align with domain knowledge?
- [ ] Any surprising findings?

**Keep it concise**: 2-3 pages max

**Deliverable**: `docs/MODEL_INTERPRETATION.md`

---

## PHASE 5: Front-End Integration (10 BONUS MARKS)

**Goal**: Create simple React + FastAPI web app for demo

### Session 5.1: FastAPI Backend

**Tasks**:

- [ ] Install FastAPI: `pip install fastapi uvicorn`
- [ ] Create `backend/main.py` with endpoints:
  - `POST /predict` - Get predictions for lottery + date
  - `GET /lotteries` - List available lotteries
  - `POST /explain` - Get SHAP explanation for prediction
- [ ] Load trained CatBoost model on startup
- [ ] CORS middleware for React frontend

**API Structure**:

```python
from fastapi import FastAPI
from catboost import CatBoostClassifier
import shap

app = FastAPI()

# Load model once at startup
model = CatBoostClassifier()
model.load_model('models/catboost_model.cbm')

@app.post("/predict")
def predict(lottery: str, date: str):
    # Return top 6 numbers with probabilities
    pass

@app.post("/explain")
def explain(lottery: str, number: int):
    # Return SHAP values for this number
    pass
```

**Deliverable**: `backend/main.py`

### Session 5.2: React Frontend

**Tasks**:

- [ ] Create React app: `npm create vite@latest frontend -- --template react`
- [ ] Simple UI with:
  - Lottery selector dropdown
  - Date picker
  - "Predict" button
  - Results table showing top 6 numbers with probabilities
  - SHAP explanation panel (optional toggle)
  - Disclaimer about randomness
- [ ] Use `fetch` or `axios` to call FastAPI backend
- [ ] Basic CSS styling (no TailwindCSS needed, keep simple)

**UI Layout**:

```
┌─────────────────────────────────────┐
│   Sri Lankan Lottery Predictor      │
├─────────────────────────────────────┤
│ Select Lottery: [Dropdown]          │
│ Select Date: [Date Picker]          │
│ [Predict Numbers]                   │
├─────────────────────────────────────┤
│ Top 6 Predicted Numbers:            │
│  1. 23 (12.5%)                      │
│  2. 45 (11.2%)                      │
│  ...                                │
├─────────────────────────────────────┤
│ [Show SHAP Explanation] (optional)  │
│ Disclaimer: Lottery is random...    │
└─────────────────────────────────────┘
```

**Deliverable**: `frontend/` (React app)

### Session 5.3: Demo Video

**Tasks**:

- [ ] Start FastAPI backend: `uvicorn backend.main:app`
- [ ] Start React frontend: `npm run dev`
- [ ] Record 3-5 minute demo showing:
  - Data collection summary
  - Model training results
  - Web app interface (React)
  - Prediction examples for different lotteries
  - SHAP explanations (if implemented)
- [ ] Use OBS or built-in screen recorder
- [ ] Add simple narration

**Deliverable**: `demo_video.mp4`

---

## PHASE 6: Critical Discussion (10 MARKS)

**Goal**: Brief critical analysis (2-3 pages)

### Session 6.1: Discussion Document

**Topics to Cover** (keep concise):

1. **Model Limitations**:

   - Lottery is inherently random
   - Historical patterns may not predict future
   - High imbalance affects minority class recall
2. **Data Quality Issues**:

   - Only 58 months of data
   - Some lotteries have limited draws
   - No prize data for DLB lotteries
3. **Bias & Fairness**:

   - No personal data involved (public lottery draws)
   - Predictions should not encourage gambling addiction
   - Disclaimer needed about randomness
4. **Real-World Impact**:

   - Educational ML project
   - Not for commercial gambling use
   - Demonstrates ML capabilities on real data

**Deliverable**: `docs/CRITICAL_DISCUSSION.md` (2-3 pages)

---

## PHASE 7: Report Writing (10 MARKS)

**Goal**: Compile final report (PDF, 10-15 pages)

### Session 7.1: Report Compilation

**Structure**:

1. **Problem Definition & Dataset** (2 pages)

   - Lottery prediction problem
   - 17 lotteries, 485K records
   - Feature engineering approach
2. **Algorithm Selection** (1-2 pages)

   - Why CatBoost
   - Comparison with taught algorithms
3. **Model Training & Evaluation** (3-4 pages)

   - Train/val/test split
   - Hyperparameters
   - Results tables and plots
   - Performance metrics
4. **Explainability** (2-3 pages)

   - SHAP analysis
   - Feature importance
   - Model interpretation
5. **Critical Discussion** (2 pages)

   - Limitations, bias, ethics
6. **Conclusion** (1 page)

**Deliverable**: `report.pdf`

---

## Submission Checklist

### Required Files:

- [ ] **Report (PDF)**: Complete assignment report
- [ ] **Source Code (ZIP/GitHub)**:
  - `src/scrapers/` - Data collection scripts
  - `src/preprocessing/` - Cleaning, feature engineering, splitting
  - `src/models/` - Baseline and CatBoost training
  - `src/explainability/` - SHAP and feature importance
  - `backend/` - FastAPI backend with model serving
  - `frontend/` - React web app
  - `requirements.txt` - Python dependencies
  - `frontend/package.json` - Node.js dependencies
- [ ] **Dataset**:
  - `data/raw/` - Original scraped data (17 CSV files)
  - `data/processed/` - Cleaned and featured data
  - `data/splits/` - Train/val/test splits (51 CSV files)
- [ ] **Demo Video (MP4)**: 3-5 minutes showing the React web app

### Documentation:

- [ ] `docs/ALGORITHM_JUSTIFICATION.md`
- [ ] `docs/MODEL_INTERPRETATION.md`
- [ ] `docs/CRITICAL_DISCUSSION.md`
- [ ] `outputs/results/` - Performance metrics and plots
- [ ] `outputs/explainability/` - SHAP and feature importance plots

---

## Git Commit Strategy

Follow Conventional Commits:

```
feat: New feature
fix: Bug fix
docs: Documentation
refactor: Code refactoring
test: Tests
chore: Maintenance
```

**Examples**:

```bash
feat(models): implement CatBoost classifier with class balancing
feat(explainability): add SHAP analysis for top features
feat(backend): create FastAPI endpoints for predictions
feat(frontend): create React prediction dashboard
docs: add algorithm justification document
docs: compile final assignment report
```

---

## Timeline (Realistic Estimate)

- **Phase 1**: ✅ COMPLETED (4 sessions)
- **Phase 2**: 1 session (algorithm justification)
- **Phase 3**: 4 sessions (baselines, CatBoost, tuning, results)
- **Phase 4**: 3 sessions (SHAP, feature importance, interpretation)
- **Phase 5**: 3 sessions (FastAPI backend, React frontend, demo video)
- **Phase 6**: 1 session (critical discussion)
- **Phase 7**: 1 session (report compilation)

**Total**: ~13 more sessions to complete

---

## Key Principles

1. **Keep It Simple**: No over-engineering, focus on assignment requirements
2. **Clean Code**: Readable, well-documented, no unnecessary complexity
3. **Concise Docs**: Short, clear, to-the-point (not lengthy reports)
4. **Focus on XAI**: SHAP is primary explainability method
5. **Working Demo**: Streamlit app should be functional and simple

---

---

**Updated**: 2026-01-15
**Version**: 2.0 (Simplified & Focused)

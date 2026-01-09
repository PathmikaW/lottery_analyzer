# Sri Lankan Lottery ML Analyzer V2 - Claude Development Plan

## Project Overview
**MSc AI - Applied Machine Learning Assignment**
**Target**: 100/100 + 10 Bonus = 110 Marks Total
**Timeline**: Multi-session development with Claude Code
**Current Branch**: `feature/lottery-analyzer-v2`

---

## Assignment Requirements Summary

### Marking Breakdown
1. **Problem Definition & Dataset** (15 marks)
2. **New Algorithm Selection** (15 marks) - XGBoost
3. **Model Training & Evaluation** (20 marks)
4. **Explainability & Interpretation** (20 marks) - SHAP, LIME, FI, PDP
5. **Critical Discussion** (10 marks)
6. **Report Quality** (10 marks)
7. **BONUS: Front-End Integration** (10 marks) - React + FastAPI

### Key Constraints
- **NO Deep Learning** - Must use XGBoost (not taught in lectures)
- **NO Image Processing**
- **Must collect local dataset** - 18 Sri Lankan lotteries
- **Time Period**: 7 months (June 2025 - Jan 2026)
- **Target Dataset Size**: 3,500-4,000 draws (~150,000 records after feature engineering)

---

## Git Workflow & Conventional Commits

### Simple Branch Strategy
- **Main Branch**: `main` - Final submission code
- **Working Branch**: `feature/lottery-analyzer-v2` - **All work happens here**
  - Single developer, no complexity needed
  - Commit after each logical unit of work
  - Merge to `main` when assignment is complete

### Conventional Commits Format
Use the following format for all commits:

```
<type>(<scope>): <subject>

<body>

<footer>
```

#### Commit Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `build`: Build system changes
- `ci`: CI/CD changes
- `chore`: Maintenance tasks

#### Commit Scopes (use relevant scope)
- `scrapers`: Web scraping code
- `preprocessing`: Data cleaning and feature engineering
- `models`: Model training and evaluation
- `explainability`: SHAP, LIME, PDP analysis
- `frontend`: React UI components
- `backend`: FastAPI endpoints
- `docs`: Documentation and reports
- `config`: Configuration files

#### Examples
```bash
# Feature addition
feat(scrapers): add NLB lottery scraper with error handling

Implemented scraper for all 9 NLB lotteries with:
- Pagination support
- Retry logic with exponential backoff
- Data validation

# Bug fix
fix(preprocessing): handle missing dates in feature engineering

Added forward fill for missing draw dates to prevent NaN values
in temporal features

# Documentation
docs(plan): add git workflow and conventional commits section

# Refactoring
refactor(models): extract common training logic to base class

# Performance improvement
perf(scrapers): optimize batch processing for multiple lotteries
```

### Simple Git Workflow

#### Start of Session
```bash
git checkout feature/lottery-analyzer-v2
git pull origin feature/lottery-analyzer-v2
```

#### During Session (Commit After Each Task)
```bash
# Example commits:
git add .
git commit -m "feat(scrapers): add NLB scraper for 9 lotteries"
git commit -m "feat(preprocessing): implement feature engineering"
git commit -m "feat(models): train XGBoost with hyperparameter tuning"
git commit -m "fix(scrapers): handle connection timeout"
git commit -m "docs(readme): add setup instructions"
```

#### End of Session
```bash
git push origin feature/lottery-analyzer-v2
```

### When to Commit
- After completing a file/module
- After fixing a bug
- After adding a feature
- End of each work session

### Git Ignore Updates
Ensure `.gitignore` includes:
```
# Data files
data/raw/*.csv
data/processed/*.csv
data/splits/*.pkl

# Models (too large for git)
models/*.pkl
models/*.joblib

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/

# Jupyter
.ipynb_checkpoints/

# IDEs
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Output files
outputs/charts/*.png
outputs/explainability/**/*.png

# Frontend
frontend/node_modules/
frontend/dist/
frontend/.env

# Backend
backend/__pycache__/
backend/.env
```

---

## Data Sources

### National Lotteries Board (NLB) - 9 Lotteries
- URL: https://www.nlb.lk
- Mahajana Sampatha
- Govisetha
- Dhana Nidhanaya
- Handahana
- Mega Power
- Ada Sampatha
- Suba-dawasak
- NLB Jaya
- Lucky 7

### Development Lotteries Board (DLB) - 9 Lotteries
- URL: https://www.dlb.lk
- Ada Kotipathi
- Shanida
- Lagna Wasana
- Supiri Dhana Sampatha
- Super Ball
- Kapruka
- Jayoda
- Sasiri
- Jaya Sampatha

---

## Technical Architecture

### Machine Learning Stack
```
Algorithm: XGBoost (Extreme Gradient Boosting)
Baselines: Logistic Regression, Random Forest, Naive Bayes
Explainability: SHAP, LIME, Feature Importance, Partial Dependence Plots
Data: pandas, numpy
Visualization: matplotlib, seaborn
Scraping: BeautifulSoup, Selenium (if needed)
```

### Full Stack (BONUS - 10 marks)
```
Backend: FastAPI (Python)
Frontend: React + TypeScript + Vite
Styling: TailwindCSS + shadcn/ui
Charts: Recharts
State: Zustand
API: REST + Axios
```

---

## Feature Engineering Plan (20-25 Features)

### Category 1: Frequency Features (6)
1. `frequency_last_10` - Appearances in last 10 draws
2. `frequency_last_30` - Appearances in last 30 draws
3. `frequency_last_50` - Appearances in last 50 draws
4. `frequency_all_time` - Total appearances
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
14. `min_gap` - Minimum gap
15. `max_gap` - Maximum gap
16. `current_gap` - Current days without appearance

### Category 4: Hot/Cold Features (4)
17. `is_hot` - Binary (top 20% frequency)
18. `is_cold` - Binary (bottom 20% frequency)
19. `temperature_score` - Normalized 0-100
20. `trend` - Categorical (heating_up/cooling_down/stable)

### Category 5: Pattern Features (3) - OPTIONAL
21. `odd_even` - Binary
22. `is_prime` - Binary
23. `number_range` - Categorical (low/mid/high)

### Target Variable
- **Binary Classification**: Will number X appear in next draw?
  - 1 = Number appears
  - 0 = Number doesn't appear

---

## Development Phases

## PHASE 1: Data Collection & Preprocessing (15 MARKS)
**Estimated Sessions**: 2-3 sessions
**Priority**: HIGH - Foundation for everything

### Session 1.1: Scraper Development
**Git Branch**: `feature/scrapers`

**Tasks**:
- [ ] Setup project structure in `ProjectV2/`
  - **Commit**: `chore(config): initialize ProjectV2 directory structure`
- [ ] Create `src/scrapers/nlb_scraper.py`
  - [ ] Scrape all 9 NLB lotteries
  - [ ] Handle pagination/date ranges
  - [ ] Bot protection bypass if needed
  - **Commit**: `feat(scrapers): implement NLB lottery scraper for 9 lotteries`
- [ ] Create `src/scrapers/dlb_scraper.py`
  - [ ] Scrape all 9 DLB lotteries
  - [ ] Handle different HTML structures
  - **Commit**: `feat(scrapers): implement DLB lottery scraper for 9 lotteries`
- [ ] Create `src/scrapers/scraper_manager.py`
  - [ ] Orchestrate all 18 scrapers
  - [ ] Error handling and retry logic
  - [ ] Progress tracking
  - **Commit**: `feat(scrapers): add scraper manager with error handling and retry logic`
- [ ] Save raw data to `data/raw/`
  - [ ] Format: CSV per lottery
  - [ ] Columns: date, draw_number, winning_numbers, [prizes]
  - **Commit**: `feat(scrapers): save raw lottery data to CSV format`
- [ ] Add requirements.txt
  - **Commit**: `build(deps): add scraping dependencies to requirements.txt`
- [ ] Create README for scrapers
  - **Commit**: `docs(scrapers): add scraper usage documentation`

**End of Session**:
```bash
git add .
git commit -m "feat(scrapers): complete web scraping implementation for 18 lotteries

- Implemented NLB scraper for 9 lotteries
- Implemented DLB scraper for 9 lotteries
- Added scraper manager with retry logic
- Saved raw data to CSV format"

git push origin feature/scrapers
git checkout feature/lottery-analyzer-v2
git merge feature/scrapers --no-ff
git push origin feature/lottery-analyzer-v2
```

### Session 1.2: Data Validation & Cleaning
**Git Branch**: `feature/preprocessing`

**Tasks**:
- [ ] Create `src/preprocessing/data_validator.py`
  - [ ] Check for missing draws
  - [ ] Validate number ranges per lottery
  - [ ] Remove duplicates
  - [ ] Handle outliers
  - **Commit**: `feat(preprocessing): add data validation module`
- [ ] Create `src/preprocessing/data_cleaner.py`
  - [ ] Standardize date formats
  - [ ] Parse winning numbers consistently
  - [ ] Handle missing values (forward fill for gaps)
  - **Commit**: `feat(preprocessing): implement data cleaning pipeline`
- [ ] Generate data quality report
  - [ ] Total draws per lottery
  - [ ] Date range coverage
  - [ ] Missing data summary
  - **Commit**: `feat(preprocessing): add data quality reporting`

**End of Session**:
```bash
git commit -m "feat(preprocessing): complete data validation and cleaning pipeline"
git push origin feature/preprocessing
```

### Session 1.3: Feature Engineering
**Git Branch**: `feature/preprocessing` (continue)

**Tasks**:
- [ ] Create `src/preprocessing/feature_engineer.py`
  - [ ] Implement frequency features (6 features)
  - **Commit**: `feat(preprocessing): add frequency-based features`
  - [ ] Implement temporal features (5 features)
  - **Commit**: `feat(preprocessing): add temporal features`
  - [ ] Implement statistical features (5 features)
  - **Commit**: `feat(preprocessing): add statistical gap features`
  - [ ] Implement hot/cold features (4 features)
  - **Commit**: `feat(preprocessing): add hot/cold temperature features`
  - [ ] Handle cold start (first 50 draws)
  - **Commit**: `fix(preprocessing): handle cold start for new lotteries`
- [ ] Generate processed datasets
  - [ ] Save to `data/processed/`
  - [ ] One file per lottery with all features
  - [ ] ~150,000 total records
  - **Commit**: `feat(preprocessing): generate processed datasets with all features`

**End of Session**:
```bash
git commit -m "feat(preprocessing): complete feature engineering for 20-25 features"
git push origin feature/preprocessing
```

### Session 1.4: Data Splitting & Balancing
**Git Branch**: `feature/preprocessing` (continue)

**Tasks**:
- [ ] Create `src/preprocessing/data_splitter.py`
  - [ ] 70% train / 15% validation / 15% test
  - [ ] Stratified split (maintain class balance)
  - [ ] Save splits to `data/splits/`
  - **Commit**: `feat(preprocessing): implement stratified data splitting`
- [ ] Document class imbalance ratios
  - **Commit**: `docs(preprocessing): document class imbalance statistics`
- [ ] Plan class balancing strategy (scale_pos_weight)
  - **Commit**: `docs(preprocessing): add class balancing strategy documentation`

**End of Session**:
```bash
git commit -m "feat(preprocessing): complete data preprocessing pipeline

- Implemented data validation and cleaning
- Created 20-25 engineered features
- Generated stratified train/val/test splits
- Documented class imbalance handling strategy"

git push origin feature/preprocessing
git checkout feature/lottery-analyzer-v2
git merge feature/preprocessing --no-ff
git push origin feature/lottery-analyzer-v2
```

**Deliverables for Report**:
- Problem statement (1 page)
- Data collection methodology (1 page)
- Feature descriptions table (1 page)
- Dataset statistics (1 page)
- Ethical considerations (0.5 page)

---

## PHASE 2: Algorithm Selection & Justification (15 MARKS)
**Estimated Sessions**: 1 session
**Priority**: MEDIUM - Mostly documentation

### Session 2.1: Documentation & Comparison
- [ ] Document XGBoost algorithm
  - [ ] Objective function with regularization
  - [ ] Gradient boosting explanation
  - [ ] Key hyperparameters
- [ ] Create comparison table
  - [ ] XGBoost vs Decision Trees
  - [ ] XGBoost vs Random Forest
  - [ ] XGBoost vs Logistic Regression
  - [ ] XGBoost vs SVM
  - [ ] XGBoost vs Naive Bayes
- [ ] Write justification (why XGBoost?)
  - [ ] Best for tabular data
  - [ ] Handles small-medium datasets well
  - [ ] Built-in regularization
  - [ ] Works with SHAP/LIME

**Deliverables for Report**:
- XGBoost overview (2 pages)
- Comparison table (1 page)
- Justification (1-2 pages)

---

## PHASE 3: Model Training & Evaluation (20 MARKS)
**Estimated Sessions**: 3-4 sessions
**Priority**: HIGH - Core ML work

### Session 3.1: Baseline Models
- [ ] Create `src/models/baseline_models.py`
  - [ ] Implement Logistic Regression
    - [ ] L1 (Lasso): C=0.5
    - [ ] L2 (Ridge): C=1.0
    - [ ] 5-fold CV
  - [ ] Implement Random Forest
    - [ ] n_estimators: 500
    - [ ] max_depth: 15
    - [ ] 5-fold CV
  - [ ] Implement Naive Bayes
    - [ ] GaussianNB (default)
- [ ] Train all baselines on one lottery first (Mahajana Sampatha)
- [ ] Document baseline results

### Session 3.2: XGBoost Training
- [ ] Create `src/models/xgboost_trainer.py`
  - [ ] Implement baseline XGBoost config
  ```python
  baseline_xgb = {
      'objective': 'binary:logistic',
      'eval_metric': 'auc',
      'n_estimators': 500,
      'max_depth': 6,
      'learning_rate': 0.1,
      'subsample': 0.8,
      'colsample_bytree': 0.8,
      'reg_alpha': 0.1,
      'reg_lambda': 1.0,
      'scale_pos_weight': 10,  # Handle imbalance
      'random_state': 42
  }
  ```
  - [ ] Early stopping (50 rounds)
  - [ ] Monitor validation AUC

### Session 3.3: Hyperparameter Tuning
- [ ] Implement Grid Search with 5-fold CV
  ```python
  param_grid = {
      'n_estimators': [300, 500, 1000],
      'max_depth': [4, 6, 8],
      'learning_rate': [0.01, 0.05, 0.1],
      'subsample': [0.7, 0.8, 0.9],
      'reg_lambda': [0.5, 1.0, 2.0]
  }
  # Total: 243 combinations
  ```
- [ ] Find best hyperparameters
- [ ] Retrain with best config on train+validation
- [ ] Save best model

### Session 3.4: Comprehensive Evaluation
- [ ] Create `src/models/evaluator.py`
  - [ ] Calculate all metrics:
    - Accuracy, Precision, Recall, F1-Score
    - AUC-ROC
    - Confusion Matrix
  - [ ] Generate visualizations:
    - Confusion matrices (4 models)
    - ROC curves (overlay all models)
    - Precision-Recall curves
    - Learning curves (XGBoost)
    - Feature importance comparison (RF vs XGBoost)
- [ ] Create comparison table (all 4 models)
- [ ] Document results

### Session 3.5: Multi-Lottery Training
- [ ] Train all 4 models on all 18 lotteries
- [ ] Save all trained models to `models/`
- [ ] Aggregate results across lotteries

**Expected Results**:
| Model | Accuracy | Precision | Recall | F1 | AUC-ROC |
|-------|----------|-----------|--------|-----|---------|
| Naive Bayes | 58-62% | 55-60% | 62-68% | 58-63% | 0.62-0.68 |
| Logistic Reg | 64-68% | 62-67% | 65-70% | 63-68% | 0.68-0.74 |
| Random Forest | 70-75% | 68-73% | 70-75% | 69-74% | 0.74-0.80 |
| **XGBoost** | **74-80%** | **72-78%** | **72-77%** | **72-77%** | **0.78-0.85** |

**Deliverables for Report**:
- Training methodology (2 pages)
- Hyperparameter tuning details (1 page)
- Results tables (1 page)
- Visualizations (6-8 plots) (2 pages)

---

## PHASE 4: Explainability & Interpretation (20 MARKS)
**Estimated Sessions**: 3-4 sessions
**Priority**: HIGH - 20% of grade

### Session 4.1: SHAP Analysis
- [ ] Install `shap` library
- [ ] Create `src/explainability/shap_analyzer.py`
  - [ ] Generate SHAP Summary Plot (global)
  - [ ] Generate 5 Waterfall Plots (local explanations)
  - [ ] Generate 5 Dependence Plots (top features)
  - [ ] Save all plots to `outputs/explainability/shap/`
- [ ] Write interpretation for each plot
  - [ ] Which features most important?
  - [ ] How do features interact?
  - [ ] Does it match domain knowledge?

### Session 4.2: LIME Analysis
- [ ] Install `lime` library
- [ ] Create `src/explainability/lime_analyzer.py`
  - [ ] Generate 5 LIME explanations (different predictions)
  - [ ] Compare with SHAP (do they agree?)
  - [ ] Save plots to `outputs/explainability/lime/`
- [ ] Write interpretation

### Session 4.3: Feature Importance Analysis
- [ ] Create `src/explainability/feature_importance.py`
  - [ ] XGBoost Importance (3 types):
    - Gain (primary)
    - Cover
    - Frequency
  - [ ] Permutation Importance
  - [ ] Random Forest Importance (comparison)
  - [ ] Save all plots
- [ ] Identify top 5-8 features

**Expected Top Features**:
1. frequency_last_30
2. days_since_last
3. is_hot
4. temperature_score
5. frequency_last_10
6. mean_gap
7. std_gap
8. is_weekend

### Session 4.4: Partial Dependence Plots
- [ ] Create `src/explainability/pdp_analyzer.py`
  - [ ] Generate 5 1-way PDPs (top features)
  - [ ] Generate 2 2-way PDPs (interactions)
    - Example: frequency_last_30 × days_since_last
  - [ ] Save all plots
- [ ] Write interpretation
  - [ ] Marginal effects
  - [ ] Non-linear patterns
  - [ ] Interaction effects

### Session 4.5: Comprehensive Interpretation
- [ ] Answer key questions:
  1. What has the model learned?
  2. Which features are most influential?
  3. Does behavior align with domain knowledge?
  4. How does XGBoost differ from Random Forest?
- [ ] Write interpretation summary (2-3 pages)

**Deliverables for Report**:
- SHAP analysis (2-3 pages with plots)
- LIME analysis (1-2 pages)
- Feature importance (1-2 pages)
- PDP analysis (1-2 pages)
- Interpretation summary (1-2 pages)

---

## PHASE 5: Critical Discussion (10 MARKS)
**Estimated Sessions**: 1 session
**Priority**: MEDIUM - Important for marks

### Session 5.1: Write Critical Analysis
- [ ] Model Limitations (3 paragraphs)
  - Data constraints (only 7 months)
  - Predictability limits (~80% max)
  - Per-lottery models (no cross-learning)
- [ ] Data Quality Issues (2 paragraphs)
  - Collection challenges
  - Class imbalance (1:10 to 1:15)
  - Cold start problem
- [ ] Bias & Fairness (2 paragraphs)
  - Temporal bias (7-month window)
  - Feature selection bias
  - Prediction shouldn't encourage gambling
- [ ] Ethical Considerations (3 paragraphs)
  - Responsible gambling warnings
  - Transparency via XAI
  - Data privacy (public data)
  - Societal impact
- [ ] Real-World Deployment (2 paragraphs)
  - Technical challenges (daily retraining)
  - Legal compliance
  - User experience (managing expectations)
- [ ] Future Improvements (1 paragraph)
  - Extend to 2-3 years data
  - Ensemble methods
  - Cross-lottery learning

**Deliverables for Report**:
- Critical discussion section (3-4 pages)

---

## PHASE 6: Report Writing (10 MARKS)
**Estimated Sessions**: 2 sessions
**Priority**: HIGH - Final deliverable

### Session 6.1: Report Compilation
- [ ] Create `report/` directory
- [ ] Compile all sections (25-35 pages):
  1. Title Page
  2. Abstract (200-250 words)
  3. Table of Contents
  4. Introduction (2 pages)
  5. Problem Definition & Dataset (3-4 pages)
  6. Algorithm Selection (3-4 pages)
  7. Training & Evaluation (5-6 pages)
  8. Explainability (6-8 pages)
  9. Critical Discussion (3-4 pages)
  10. Conclusion (1-2 pages)
  11. References (APA style)
  12. Appendices (code snippets, extra plots)
- [ ] Ensure all figures numbered and referenced
- [ ] Ensure all tables formatted properly
- [ ] Proofread entire document

### Session 6.2: Final Formatting
- [ ] Check visualization quality (300 DPI)
- [ ] Consistent color scheme
- [ ] No typos/grammar errors
- [ ] Export to PDF: `ML_Assignment_Report.pdf`

**Deliverables**:
- Final PDF report (25-35 pages)

---

## PHASE 7: BONUS - Front-End Integration (10 MARKS)
**Estimated Sessions**: 4-5 sessions
**Priority**: LOW - Bonus marks only

### Session 7.1: Backend API (FastAPI)
- [ ] Create `backend/` directory
- [ ] Setup FastAPI project structure
- [ ] Implement API endpoints:
  - `GET /api/datasets/{lottery}` - Historical data
  - `GET /api/datasets/stats` - Dataset statistics
  - `GET /api/models` - List trained models
  - `POST /api/predict` - Generate predictions
  - `GET /api/explain/shap/{prediction_id}` - SHAP data
  - `GET /api/explain/importance/{model_id}` - Feature importance
  - `GET /api/analytics/confusion/{model_id}` - Confusion matrix
  - `GET /api/analytics/roc/{model_id}` - ROC curve data
- [ ] Load all 18 trained models
- [ ] Add CORS middleware
- [ ] Test all endpoints

### Session 7.2: Frontend Setup (React)
- [ ] Create `frontend/` directory
- [ ] Setup Vite + React + TypeScript
- [ ] Install dependencies:
  - TailwindCSS
  - shadcn/ui
  - Recharts
  - Zustand
  - Axios
- [ ] Create project structure

### Session 7.3: Frontend Pages
- [ ] Page 1: Home
  - Project overview
  - Dataset statistics cards
  - Model performance table
  - Navigation
- [ ] Page 2: Data Explorer
  - Lottery selector dropdown
  - Date range filter
  - Data table (last 50 draws)
  - Download CSV button
- [ ] Page 3: Predictions (MAIN PAGE)
  - Input: Lottery, Model, Date
  - Output: Top 4-6 predicted numbers + confidences
  - Probability heatmap
  - **PROMINENT DISCLAIMER**:
    - "Predictions based on historical patterns"
    - "Lottery draws are random"
    - "No guarantee of winning"
    - "Educational purposes only"
- [ ] Page 4: Explanations
  - Select prediction
  - SHAP waterfall plot
  - Feature importance bar chart
  - Interpretation text
- [ ] Page 5: Model Comparison
  - Performance metrics table
  - Confusion matrices (4 models)
  - ROC curves (overlay)
  - Training time comparison

### Session 7.4: Frontend-Backend Integration
- [ ] Create API service (`src/services/api.ts`)
- [ ] Connect all pages to backend
- [ ] Handle loading states
- [ ] Error handling
- [ ] Test end-to-end

### Session 7.5: Demo Video
- [ ] Record 3-5 minute demo video
  - Intro (30 sec): Project overview
  - Data (30 sec): Show dataset
  - Predictions (1 min): Generate prediction
  - Explanations (1.5 min): SHAP + feature importance
  - Comparison (45 sec): Model performance
  - Conclusion (15 sec): Summary
- [ ] Use OBS Studio or Loom
- [ ] Export to `demo_video.mp4`

**Deliverables**:
- Working frontend + backend
- Demo video (3-5 minutes)

---

## Project Structure (Final)

```
lottery_analyzer/
├── data/
│   ├── raw/                   # Scraped data (18 CSVs)
│   ├── processed/             # Featured data (18 CSVs)
│   └── splits/                # train/val/test splits
│
├── models/
│   ├── xgboost_*.pkl          # 18 XGBoost models
│   ├── rf_*.pkl               # 18 Random Forest models
│   ├── lr_*.pkl               # 18 Logistic Regression
│   ├── nb_*.pkl               # 18 Naive Bayes
│   └── scaler.pkl             # StandardScaler
│
├── outputs/
│   ├── charts/                # All plots
│   ├── explainability/        # SHAP, LIME, PDP plots
│   │   ├── shap/
│   │   ├── lime/
│   │   ├── importance/
│   │   └── pdp/
│   └── statistics/            # JSON/CSV stats
│
├── src/
│   ├── scrapers/
│   │   ├── nlb_scraper.py
│   │   ├── dlb_scraper.py
│   │   └── scraper_manager.py
│   ├── preprocessing/
│   │   ├── data_validator.py
│   │   ├── data_cleaner.py
│   │   ├── feature_engineer.py
│   │   └── data_splitter.py
│   ├── models/
│   │   ├── baseline_models.py
│   │   ├── xgboost_trainer.py
│   │   └── evaluator.py
│   ├── explainability/
│   │   ├── shap_analyzer.py
│   │   ├── lime_analyzer.py
│   │   ├── feature_importance.py
│   │   └── pdp_analyzer.py
│   └── utils/
│       └── config.py
│
├── backend/                   # BONUS - FastAPI
│   ├── app/
│   │   ├── main.py
│   │   ├── routes/
│   │   └── services/
│   └── requirements.txt
│
├── frontend/                  # BONUS - React
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   └── App.tsx
│   └── package.json
│
├── report/
│   └── ML_Assignment_Report.pdf
│
├── notebooks/                 # Jupyter notebooks for exploration
│   ├── 1_data_collection.ipynb
│   ├── 2_exploratory_analysis.ipynb
│   ├── 3_feature_engineering.ipynb
│   ├── 4_model_training.ipynb
│   ├── 5_evaluation.ipynb
│   └── 6_explainability.ipynb
│
├── demo_video.mp4             # BONUS
├── requirements.txt
├── README.md
└── CLAUDE_DEV_PLAN.md         # This file
```

---

## Session Execution Strategy

### Recommended Session Order

**Week 1: Foundation**
1. Session: Scraper development (NLB + DLB)
2. Session: Data validation & cleaning
3. Session: Feature engineering

**Week 2: Data & Baselines**
4. Session: Data splitting & EDA
5. Session: Baseline model training
6. Session: XGBoost baseline training

**Week 3: Model Optimization**
7. Session: Hyperparameter tuning
8. Session: Multi-lottery training
9. Session: Comprehensive evaluation

**Week 4: Explainability**
10. Session: SHAP analysis
11. Session: LIME + Feature Importance
12. Session: Partial Dependence Plots

**Week 5: Report & Bonus**
13. Session: Critical discussion + Report compilation
14. Session: Report finalization
15. Session: Backend API (if doing bonus)
16. Session: Frontend pages (if doing bonus)
17. Session: Demo video (if doing bonus)

---

## Key Reminders for Each Session

### Before Starting Any Session
```bash
# 1. Ensure you're on the development branch
git checkout feature/lottery-analyzer-v2

# 2. Pull latest changes
git pull origin feature/lottery-analyzer-v2

# 3. Check git status
git status

# 4. Create feature branch for this session
git checkout -b feature/<phase-name>
```

- [ ] Pull latest changes from `feature/lottery-analyzer-v2`
- [ ] Review previous session's output
- [ ] Check TODO list for current phase
- [ ] Create feature branch for focused work

### During Session
- [ ] Follow the checklist for current phase
- [ ] **Commit early and often** (after each logical unit)
- [ ] Use conventional commit format
- [ ] Write clean, documented code
- [ ] Save intermediate results
- [ ] Document any issues/decisions

**Example commit flow during session**:
```bash
# After creating a module
git add src/scrapers/nlb_scraper.py
git commit -m "feat(scrapers): add base NLB scraper class"

# After adding a feature
git add src/scrapers/nlb_scraper.py
git commit -m "feat(scrapers): implement pagination for NLB scraper"

# After fixing a bug
git add src/scrapers/nlb_scraper.py
git commit -m "fix(scrapers): handle connection timeout in NLB scraper"

# After adding tests
git add tests/test_nlb_scraper.py
git commit -m "test(scrapers): add unit tests for NLB scraper validation"

# After updating documentation
git add src/scrapers/README.md
git commit -m "docs(scrapers): add usage examples for NLB scraper"
```

### End of Session
```bash
# 1. Make final commit if needed
git add .
git commit -m "feat(scrapers): complete scraper implementation for session 1.1

- Implemented NLB scraper for 9 lotteries
- Implemented DLB scraper for 9 lotteries
- Added error handling and retry logic
- Generated raw CSV datasets"

# 2. Push feature branch to remote
git push origin feature/scrapers

# 3. Switch to development branch
git checkout feature/lottery-analyzer-v2

# 4. Merge feature branch (no fast-forward to preserve history)
git merge feature/scrapers --no-ff

# 5. Push to development branch
git push origin feature/lottery-analyzer-v2

# 6. Optional: Delete feature branch if complete
git branch -d feature/scrapers
git push origin --delete feature/scrapers
```

- [ ] Commit all changes with descriptive message
- [ ] Push to remote
- [ ] Merge to development branch
- [ ] Update progress in this document
- [ ] Note any blockers for next session
- [ ] Tag important milestones (optional)

**Optional: Create Git Tags for Major Milestones**
```bash
# After completing Phase 1
git tag -a v0.1-data-collection -m "Phase 1: Data collection and preprocessing complete"
git push origin v0.1-data-collection

# After completing Phase 3
git tag -a v0.2-model-training -m "Phase 3: Model training and evaluation complete"
git push origin v0.2-model-training

# After completing Phase 4
git tag -a v0.3-explainability -m "Phase 4: Explainability analysis complete"
git push origin v0.3-explainability

# Final submission
git tag -a v1.0-submission -m "Final submission: All phases complete"
git push origin v1.0-submission
```

---

## Success Criteria Reminder

### Minimum (Pass 50-59%)
- Dataset collected (3,000+ draws)
- XGBoost trained and evaluated
- 2+ explainability methods
- Basic critical discussion
- Report submitted (20+ pages)

### Target (Excellent 80-89%)
- Comprehensive dataset (4,000+ draws)
- Detailed model comparison
- Deep explainability analysis
- Insightful discussion
- Professional report (30-35 pages)
- Front-end attempted

### Stretch Goal (Outstanding 90-100%)
- Exemplary dataset and preprocessing
- XGBoost achieves 78%+ accuracy
- Publication-quality explainability
- Critical, nuanced discussion
- Exceptional report
- Fully functional front-end + demo

---

## Technical Debt & Risks

### Known Risks
1. **Website Changes**: NLB/DLB websites may change structure
   - Mitigation: Build flexible scrapers, save raw HTML
2. **Data Insufficiency**: May not get 7 months for all lotteries
   - Mitigation: Accept what's available, document limitations
3. **Class Imbalance**: Severe imbalance (1:10 to 1:15)
   - Mitigation: Use scale_pos_weight, focus on AUC-ROC
4. **Time Constraints**: Frontend is time-consuming
   - Mitigation: Frontend is bonus only, prioritize core work

### Technical Decisions to Make
- [ ] Use Selenium or BeautifulSoup? (BeautifulSoup first, Selenium if needed)
- [ ] Train one model per lottery or combined? (Per lottery - different number ranges)
- [ ] Use GPU for XGBoost? (Optional, CPU is fine for this dataset size)
- [ ] Deploy frontend? (Optional, local demo is sufficient)

---

## Next Session Preparation

### Session 1: Scraper Development (Start Here!)
**Goal**: Get raw data from all 18 lotteries

**Pre-work**:
- [ ] Visit https://www.nlb.lk and inspect HTML structure
- [ ] Visit https://www.dlb.lk and inspect HTML structure
- [ ] Check if sites have public APIs
- [ ] Note any anti-scraping measures

**Deliverables**:
- [ ] `src/scrapers/nlb_scraper.py`
- [ ] `src/scrapers/dlb_scraper.py`
- [ ] `data/raw/` with 18 CSVs
- [ ] Scraping documentation

**Estimated Time**: 3-4 hours

---

## Questions to Clarify Before Starting

1. **Data Period**: Assignment says June 2025 - Jan 2026, but we're in Jan 2026. Should we scrape historical data from June 2024 - Jan 2025?
   - **Decision**: Yes, scrape last 7 months of available historical data

2. **Prize Data**: Should we scrape prize information?
   - **Decision**: Optional, focus on winning numbers first

3. **V1 Code**: Should we reuse any code from V1?
   - **Decision**: Keep V1 as reference, start fresh in ProjectV2/

---

## Final Submission Checklist

### Required Files
- [ ] `ML_Assignment_Report.pdf` (25-35 pages)
- [ ] `source_code.zip` or GitHub link
  - [ ] Data collection scripts
  - [ ] Preprocessing code
  - [ ] Model training scripts
  - [ ] Evaluation scripts
  - [ ] Explainability scripts
  - [ ] Trained models (.pkl files)
  - [ ] requirements.txt
  - [ ] README with setup instructions
  - [ ] Dataset or data collection documentation

### Bonus Files
- [ ] `frontend/` folder (React code)
- [ ] `backend/` folder (FastAPI code)
- [ ] `demo_video.mp4` (3-5 minutes)

### Final Checks
- [ ] All code runs without errors
- [ ] All visualizations render correctly
- [ ] Report has no typos
- [ ] All references cited (APA style)
- [ ] Demo video has clear audio (if included)
- [ ] Submitted before deadline

---

## Contact & Collaboration

This plan is designed for multi-session development with Claude Code.

Each session should:
1. Reference this plan
2. Focus on one phase/section
3. Update progress markers
4. Document any deviations

**Ready to start with Session 1: Scraper Development!**

---

**END OF CLAUDE DEVELOPMENT PLAN**

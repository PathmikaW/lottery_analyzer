# Sri Lankan Lottery ML Analyzer

**MSc AI - Applied Machine Learning Assignment**

A machine learning system for analyzing Sri Lankan lottery draws using CatBoost with SHAP explainability.

---

## Project Overview

This project demonstrates:
- ✅ Local dataset collection (17 Sri Lankan lotteries)
- ✅ Feature engineering (20 features across 4 categories)
- ✅ Novel ML algorithm (CatBoost - not taught in lectures)
- 🔄 Model training & evaluation with XAI (SHAP)
- 🔄 React + FastAPI web application

**Educational Purpose**: This is an academic project to demonstrate ML and XAI skills. It is NOT intended for commercial gambling use.

---

## Project Structure

```
lottery_analyzer/
├── V1/                              # Legacy version (reference)
├── Applied ML Lec slides/           # Course materials
│
├── data/                            # Datasets
│   ├── raw/                        # Original scraped data (17 lotteries)
│   ├── processed/                  # Cleaned + featured data
│   └── splits/                     # Train/val/test splits (51 files)
│
├── src/                             # Source code
│   ├── scrapers/                   # Data collection scripts
│   ├── preprocessing/              # Data pipeline
│   ├── models/                     # ML models (Phase 3)
│   ├── explainability/             # XAI analysis (Phase 4)
│   └── utils/                      # Utility scripts
│
├── docs/                            # Documentation
│   ├── ALGORITHM_JUSTIFICATION.md  # Why CatBoost
│   └── ALGORITHM_SELECTION_RATIONALE.md
│
├── outputs/                         # Generated outputs
│   ├── statistics/                 # Data stats
│   ├── reports/                    # Analysis reports
│   ├── results/                    # Model results (Phase 3)
│   └── explainability/             # SHAP plots (Phase 4)
│
├── models/                          # Saved trained models (Phase 3)
├── notebooks/                       # Jupyter notebooks (exploration)
├── backend/                         # FastAPI backend (Phase 5)
├── frontend/                        # React frontend (Phase 5)
│
├── CLAUDE_DEV_PLAN.md              # Development plan
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

---

## Dataset Summary

- **Total Lotteries**: 17 (NLB: 8, DLB: 9)
- **Total Draws**: 8,085
- **Date Range**: 2021-04-01 to 2026-01-12 (58.2 months)
- **Records After Feature Engineering**: 485,094
- **Features**: 20 (frequency, temporal, statistical, hot/cold)
- **Target Variable**: `appeared` (binary classification)
- **Class Imbalance**: 1:13.92 overall (range: 1:1.11 to 1:19.00)

---

## Installation

### Prerequisites
- Python 3.8+
- Node.js 16+ (for frontend)
- Git

### Setup

#### Option 1: Automated Setup with Virtual Environment (Recommended)

**Windows:**
```bash
# Run setup script
setup_env.bat
```

**Linux/Mac:**
```bash
# Run setup script
bash setup_env.sh
```

This will:
- Create a virtual environment (`lottery_env/`)
- Install all Python dependencies from `requirements.txt`
- Activate the environment automatically

#### Option 2: Manual Setup

```bash
# Clone repository
git clone <repository-url>
cd lottery_analyzer

# Create virtual environment (recommended)
python -m venv lottery_env

# Activate virtual environment
# Windows:
lottery_env\Scripts\activate
# Linux/Mac:
source lottery_env/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# (Optional) Install frontend dependencies
cd frontend
npm install
```

### Activating the Environment Later

After initial setup, activate the virtual environment:

**Windows:**
```bash
lottery_env\Scripts\activate
```

**Linux/Mac:**
```bash
source lottery_env/bin/activate
```

To deactivate:
```bash
deactivate
```

---

## Usage

### 1. Data Collection (✅ Completed)

```bash
# Run all scrapers
python src/utils/run_scrapers.py

# Generate data quality report
python src/utils/generate_reports.py
```

### 2. Data Preprocessing (✅ Completed)

```bash
# Validate data
python src/preprocessing/data_validator.py

# Clean data
python src/preprocessing/data_cleaner.py

# Engineer features
python src/preprocessing/feature_engineer.py

# Split data
python src/preprocessing/data_splitter.py
```

### 3. Model Training (Phase 3 - ✅ Completed)

#### Option A: Google Colab (Recommended - 4.6x Faster)

**Why Colab?**
- Free Tesla T4 GPU (5-10x faster training)
- No local setup required
- Hyperparameter tuning: 8 min vs 45 min locally

**Quick Start:**
1. Open [Google Colab](https://colab.research.google.com)
2. Upload notebooks from `notebooks/` folder:
   - `01_baseline_models_colab.ipynb`
   - `02_catboost_training_colab.ipynb`
   - `03_hyperparameter_tuning_colab.ipynb`
3. Enable GPU: Runtime → Change runtime type → GPU
4. Run cells in order

**See [COLAB_GUIDE.md](COLAB_GUIDE.md) for detailed instructions.**

**Results:**
- Random Forest: 25.95% F1-Score (best baseline)
- CatBoost (Tuned): 25.92% F1-Score
- 3.87x improvement over random baseline
- All results saved in `outputs/results/`

#### Option B: Local Training (CPU)

```bash
# Activate virtual environment
lottery_env\Scripts\activate  # Windows
source lottery_env/bin/activate  # Linux/Mac

# Start Jupyter
jupyter notebook

# Open and run in order:
# - notebooks/01_baseline_models.ipynb
# - notebooks/02_catboost_training.ipynb
# - notebooks/03_hyperparameter_tuning.ipynb
```


### 4. Explainability Analysis (Phase 4 - 🔄 In Progress)

#### Option A: Google Colab (Recommended)

**Quick Start:**
1. Open [Google Colab](https://colab.research.google.com)
2. Upload notebooks:
   - `notebooks/04_shap_analysis_colab.ipynb` (Global importance)
   - `notebooks/05_lime_analysis_colab.ipynb` (Local explanations)
3. Enable GPU: Runtime → Change runtime type → GPU
4. Run both notebooks in order

**SHAP Outputs** (saved to `outputs/explainability/shap/`):
- Summary plots (global feature importance)
- Dependence plots (feature relationships)
- Force plots (individual predictions)
- Feature importance comparison

**LIME Outputs** (saved to `outputs/explainability/lime/`):
- Instance-level explanations (6 examples)
- Feature importance aggregation
- LIME vs SHAP comparison

#### Option B: Local Analysis (CPU)

```bash
# Activate virtual environment
lottery_env\Scripts\activate  # Windows
source lottery_env/bin/activate  # Linux/Mac

# Start Jupyter
jupyter notebook

# Run both notebooks
```

**Documentation:**
- See [docs/EXPLAINABILITY_ANALYSIS.md](docs/EXPLAINABILITY_ANALYSIS.md) for SHAP + LIME results

### 5. Web Application (🔄 Phase 5 - Planned)

```bash
# Start backend (Terminal 1)
cd backend
uvicorn main:app --reload

# Start frontend (Terminal 2)
cd frontend
npm run dev
```

---

## Development Progress

### ✅ Phase 1: Data Collection & Preprocessing (Completed)
- [x] Session 1.1: Scraper Development
- [x] Session 1.2: Data Validation & Cleaning
- [x] Session 1.3: Feature Engineering
- [x] Session 1.4: Data Splitting & Balancing

### ✅ Phase 2: Algorithm Selection (Completed)
- [x] Session 2.1: CatBoost Justification Document

### ✅ Phase 3: Model Training & Evaluation (Completed)
- [x] Session 3.1: Baseline Models (Logistic Regression, Random Forest)
- [x] Session 3.2: CatBoost Training
- [x] Session 3.3: Hyperparameter Tuning (Grid Search)
- [x] Session 3.4: Results & Metrics (25.92% F1-Score)

### ✅ Phase 4: Explainability (Completed)
- [x] Session 4.1: SHAP Analysis Notebook
- [x] Session 4.2: LIME Analysis Notebook
- [x] Session 4.3: Feature Importance Comparison (SHAP vs LIME)
- [x] Session 4.4: Explainability Documentation
- [x] Session 4.5: Run notebooks in Colab (21 outputs generated)

### 🔄 Phase 5: Frontend (Planned)
- [ ] Session 5.1: FastAPI Backend
- [ ] Session 5.2: React Frontend
- [ ] Session 5.3: Demo Video

### 🔄 Phase 6: Critical Discussion (Planned)
- [ ] Session 6.1: Discussion Document

### 🔄 Phase 7: Report Writing (Planned)
- [ ] Session 7.1: Final Report Compilation

---

## Key Technologies

- **Data Collection**: BeautifulSoup, Selenium
- **Data Processing**: pandas, numpy, scikit-learn
- **ML Algorithm**: CatBoost (gradient boosting)
- **Explainability**: SHAP, LIME
- **Visualization**: matplotlib, seaborn
- **Backend**: FastAPI
- **Frontend**: React + Vite
- **Version Control**: Git

---

## Assignment Compliance

### Marking Breakdown
1. ✅ **Problem Definition & Dataset** (15 marks) - Completed
2. ✅ **Algorithm Selection** (15 marks) - CatBoost (not taught in lectures)
3. ✅ **Model Training & Evaluation** (20 marks) - Completed (25.92% F1-Score)
4. ✅ **Explainability** (20 marks) - Completed (SHAP + LIME with 21 outputs)
5. 🔄 **Critical Discussion** (10 marks) - Planned
6. 🔄 **Report Quality** (10 marks) - Planned
7. 🔄 **BONUS: Frontend** (10 marks) - Planned (React + FastAPI)

**Total**: 90 marks + 10 bonus = 100 marks

---

## Important Disclaimers

⚠️ **Educational Purpose Only**
- This is an academic machine learning assignment
- NOT intended for commercial gambling or betting
- Lottery outcomes are inherently random
- Historical patterns do not predict future results
- No guarantee of winning

⚠️ **Ethical Considerations**
- All data is publicly available from official lottery websites
- No personal or sensitive data is collected
- Predictions should not encourage gambling addiction
- Model limitations are thoroughly discussed in Phase 6

---

## License

This project is for educational purposes only. All lottery data is sourced from official Sri Lankan lottery websites (NLB and DLB).

---

## Author

MSc AI Student - Applied Machine Learning Assignment
Date: January 2026

---

## References

- National Lotteries Board (NLB): https://www.nlb.lk
- Development Lotteries Board (DLB): https://www.dlb.lk
- CatBoost Documentation: https://catboost.ai/
- SHAP Documentation: https://shap.readthedocs.io/
- LIME Documentation: https://github.com/marcotcr/lime

---

**For detailed development plan, see [CLAUDE_DEV_PLAN.md](CLAUDE_DEV_PLAN.md)**

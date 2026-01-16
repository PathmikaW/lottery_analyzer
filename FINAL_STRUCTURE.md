# Final Codebase & Folder Structure

## Complete Project Structure

```
lottery_analyzer/
│
├── 📚 REFERENCE MATERIALS (Keep as-is)
│   ├── V1/                                    # Legacy version
│   └── Applied ML Lec slides/                 # Course materials & guidelines
│
├── 📄 ROOT DOCUMENTATION
│   ├── README.md                              # Project overview ✅
│   ├── CLAUDE_DEV_PLAN.md                    # Development plan ✅
│   ├── requirements.txt                       # Python dependencies
│   └── .gitignore                            # Git ignore rules ✅
│
├── 📊 DATA (485,094 records)
│   ├── raw/                                   # Original scraped data
│   │   ├── nlb_mahajana_sampatha.csv         # 8 NLB lotteries
│   │   ├── dlb_shanida.csv                   # 9 DLB lotteries
│   │   └── ... (17 CSV files total)
│   │
│   ├── processed/                             # Cleaned & featured data
│   │   ├── nlb_mahajana_sampatha_cleaned.csv  # Step 1: Cleaned
│   │   ├── nlb_mahajana_sampatha_featured.csv # Step 2: Featured (20 cols)
│   │   └── ... (17 cleaned + 17 featured = 34 files)
│   │
│   └── splits/                                # Train/val/test splits (70/15/15)
│       ├── nlb_mahajana_sampatha_train.csv   # Training set
│       ├── nlb_mahajana_sampatha_val.csv     # Validation set
│       ├── nlb_mahajana_sampatha_test.csv    # Test set
│       └── ... (17 × 3 = 51 CSV files)
│
├── 💻 SOURCE CODE
│   ├── scrapers/                              ✅ Phase 1.1
│   │   ├── __init__.py
│   │   ├── base_scraper.py                   # Base scraper class
│   │   ├── nlb_scraper.py                    # NLB scraper
│   │   ├── dlb_scraper.py                    # DLB scraper
│   │   ├── scraper_manager.py                # Manages all scrapers
│   │   └── README.md                         # Scraper documentation
│   │
│   ├── preprocessing/                         ✅ Phase 1.2-1.4
│   │   ├── __init__.py
│   │   ├── data_validator.py                 # Data validation
│   │   ├── data_cleaner.py                   # Data cleaning
│   │   ├── feature_engineer.py               # Feature engineering (20 features)
│   │   └── data_splitter.py                  # Train/val/test splitting
│   │
│   ├── models/                                🔄 Phase 3 (TO CREATE)
│   │   ├── __init__.py
│   │   ├── baseline_models.py                # Logistic Regression, Random Forest
│   │   ├── catboost_model.py                 # CatBoost classifier
│   │   ├── hyperparameter_tuning.py          # Grid search
│   │   └── model_evaluator.py                # Evaluation utilities
│   │
│   ├── explainability/                        🔄 Phase 4 (TO CREATE)
│   │   ├── __init__.py
│   │   ├── shap_analysis.py                  # SHAP values & plots
│   │   └── feature_importance.py             # Feature importance analysis
│   │
│   └── utils/                                 ✅ Utilities
│       ├── run_scrapers.py                   # Run all scrapers
│       └── generate_reports.py               # Generate data quality reports
│
├── 📓 NOTEBOOKS (Interactive Analysis & Demo)
│   ├── 00_data_exploration.ipynb             # 🔄 Data exploration (optional)
│   ├── 01_baseline_models.ipynb              # 🔄 Phase 3.1: Train baselines
│   ├── 02_catboost_training.ipynb            # 🔄 Phase 3.2: Train CatBoost
│   ├── 03_hyperparameter_tuning.ipynb        # 🔄 Phase 3.3: Tune hyperparameters
│   ├── 04_model_evaluation.ipynb             # 🔄 Phase 3.4: Evaluate & compare
│   ├── 05_shap_analysis.ipynb                # 🔄 Phase 4.1: SHAP visualizations
│   └── 06_feature_importance.ipynb           # 🔄 Phase 4.2: Feature importance
│
├── 📚 DOCUMENTATION
│   ├── ALGORITHM_JUSTIFICATION.md            # ✅ Phase 2: Why CatBoost
│   ├── ALGORITHM_SELECTION_RATIONALE.md      # ✅ Internal notes
│   ├── MODEL_INTERPRETATION.md               # 🔄 Phase 4.3: Model insights
│   └── CRITICAL_DISCUSSION.md                # 🔄 Phase 6: Limitations & ethics
│
├── 📈 OUTPUTS (Generated Results)
│   ├── statistics/                            ✅ Data statistics
│   │   ├── data_quality_stats.json           # Data quality metrics
│   │   └── split_stats.json                  # Train/val/test split stats
│   │
│   ├── reports/                               ✅ Analysis reports
│   │   ├── CLASS_IMBALANCE_ANALYSIS.md       # Imbalance analysis
│   │   └── validation_report.txt             # Validation results
│   │
│   ├── results/                               🔄 Phase 3 (TO CREATE)
│   │   ├── baseline_results.json             # Baseline metrics
│   │   ├── catboost_results.json             # CatBoost metrics
│   │   ├── confusion_matrix.png              # Confusion matrix plot
│   │   ├── roc_curves.png                    # ROC curves
│   │   └── model_comparison.csv              # Comparison table
│   │
│   └── explainability/                        🔄 Phase 4 (TO CREATE)
│       ├── shap_summary.png                  # SHAP summary plot
│       ├── shap_dependence_*.png             # Dependence plots (top 5)
│       ├── feature_importance.png            # Feature importance bar chart
│       └── shap_values.pkl                   # Saved SHAP values
│
├── 🤖 TRAINED MODELS
│   ├── logistic_regression.pkl               # 🔄 Phase 3.1: LR baseline
│   ├── random_forest.pkl                     # 🔄 Phase 3.1: RF baseline
│   ├── catboost_model.cbm                    # 🔄 Phase 3.2: CatBoost model
│   └── best_model.cbm                        # 🔄 Phase 3.3: Best tuned model
│
├── 🌐 BACKEND (FastAPI)                      🔄 Phase 5.1 (TO CREATE)
│   ├── main.py                               # FastAPI app
│   ├── models.py                             # Pydantic models
│   ├── predictor.py                          # Prediction logic
│   └── requirements.txt                      # Backend dependencies
│
├── ⚛️ FRONTEND (React + Vite)                🔄 Phase 5.2 (TO CREATE)
│   ├── src/
│   │   ├── App.jsx                           # Main app component
│   │   ├── components/
│   │   │   ├── LotterySelector.jsx          # Lottery dropdown
│   │   │   ├── DatePicker.jsx               # Date picker
│   │   │   ├── PredictionResults.jsx        # Results display
│   │   │   └── ShapExplanation.jsx          # SHAP visualizations
│   │   └── api/
│   │       └── client.js                     # API client (axios)
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
└── 🎥 DELIVERABLES                            🔄 Phase 5.3 & 7 (TO CREATE)
    ├── demo_video.mp4                        # 3-5 min demo video
    └── final_report.pdf                      # Assignment report (10-15 pages)
```

---

## File Count Summary

### ✅ COMPLETED (Phase 1 & 2)
- **Data Files**: 17 raw + 34 processed + 51 splits = **102 CSV files**
- **Source Code**: 14 Python files (scrapers + preprocessing + utils)
- **Documentation**: 4 docs (README, PLAN, 2 justifications)
- **Outputs**: 2 stats JSON + 2 reports

### 🔄 TO CREATE (Phase 3-7)
- **Phase 3**: 4 Python scripts + 4 notebooks + 5 result files + 3 model files
- **Phase 4**: 2 Python scripts + 2 notebooks + ~8 output files
- **Phase 5**: 1 backend folder + 1 frontend folder
- **Phase 6**: 1 critical discussion doc
- **Phase 7**: 1 final report PDF + 1 demo video

**Total Files Expected**: ~200+ files (including node_modules, data, models)

---

## Development Workflow (Notebooks + Scripts)

### Phase 3: Model Training
```
1. Work in notebooks (interactive):
   - 01_baseline_models.ipynb       → Experiment, visualize results
   - 02_catboost_training.ipynb     → Train, tune, compare
   - 03_hyperparameter_tuning.ipynb → Grid search with live plots

2. Extract to scripts (production):
   - src/models/baseline_models.py  → Clean, reusable code
   - src/models/catboost_model.py   → Can be imported
   - src/models/hyperparameter_tuning.py → Automated

3. Generate outputs:
   - outputs/results/               → Metrics, plots, tables
   - models/                        → Saved trained models
```

### Phase 4: Explainability
```
1. Work in notebooks (visual):
   - 05_shap_analysis.ipynb         → Interactive SHAP plots
   - 06_feature_importance.ipynb    → Visual analysis

2. Extract to scripts:
   - src/explainability/shap_analysis.py → Reusable
   - src/explainability/feature_importance.py

3. Generate outputs:
   - outputs/explainability/        → SHAP plots, importance charts
```

---

## Key Design Decisions

### ✅ What We Did Right
1. **Clean separation**: scrapers → preprocessing → models → explainability
2. **Both notebooks + scripts**: Exploration + production code
3. **Organized outputs**: statistics, reports, results, explainability
4. **Documentation alongside code**: Each phase has docs in `docs/`
5. **Version control friendly**: .gitignore for large files, notebooks

### 🎯 What Makes This Structure Good
1. **Easy to navigate**: Clear folder names, logical hierarchy
2. **Reproducible**: Scripts can be run in sequence
3. **Interactive demos**: Notebooks show step-by-step process
4. **Assignment-ready**: All deliverables in correct folders
5. **Scalable**: Can add more models/features easily

---

## How to Use This Structure

### For Development (You):
1. **Experiment in notebooks**: Quick iteration, see results immediately
2. **Refine in scripts**: Clean up code, make reusable
3. **Save outputs**: All plots/metrics go to `outputs/`
4. **Document findings**: Update `docs/` as you go

### For Assignment Submission:
1. **Code**: ZIP entire `src/` folder + `notebooks/`
2. **Data**: Include `data/raw/` and split stats
3. **Models**: Include best trained models from `models/`
4. **Outputs**: All plots/metrics from `outputs/`
5. **Docs**: All markdown files from `docs/`
6. **Report**: `final_report.pdf` in root
7. **Demo**: `demo_video.mp4` in root

### For Demo Video:
1. **Show notebooks**: Walk through training process
2. **Show web app**: React frontend with predictions
3. **Show SHAP**: Explain model decisions visually

---

## Next Steps (Phase 3)

**Recommended approach**:
1. ✅ Create `notebooks/01_baseline_models.ipynb`
2. ✅ Train Logistic Regression & Random Forest interactively
3. ✅ Visualize results in notebook
4. ✅ Extract working code to `src/models/baseline_models.py`
5. ✅ Repeat for CatBoost (notebooks/02 → src/models/catboost)

**This gives you**:
- Interactive exploration (notebooks for demo)
- Production code (scripts for reproducibility)
- Clean documentation (outputs for report)

---

**Ready to proceed with Phase 3: Model Training?**

We'll start with `notebooks/01_baseline_models.ipynb` to keep it interactive and visual! 🚀

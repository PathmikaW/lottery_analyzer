# Notebooks

Interactive Jupyter notebooks for exploratory analysis and model training.

## Notebooks Structure

### Phase 3: Model Training & Evaluation
- `01_baseline_models.ipynb` - Train Logistic Regression & Random Forest
- `02_catboost_training.ipynb` - Train CatBoost classifier
- `03_hyperparameter_tuning.ipynb` - Grid search for best parameters
- `04_model_evaluation.ipynb` - Compare models and generate metrics

### Phase 4: Explainability & Interpretation
- `05_shap_analysis.ipynb` - SHAP values and visualizations
- `06_feature_importance.ipynb` - Feature importance analysis

### Optional
- `00_data_exploration.ipynb` - Exploratory data analysis (optional)

## Workflow

1. **Experiment in notebooks** - Interactive, visual, quick iteration
2. **Extract to Python scripts** - Clean code in `src/models/` and `src/explainability/`
3. **Save outputs** - All plots and metrics go to `outputs/`

## Running Notebooks

```bash
# Install Jupyter
pip install jupyter notebook

# Launch Jupyter
jupyter notebook

# Or use VS Code with Jupyter extension
```

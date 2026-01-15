# Explainability Outputs

This folder contains XAI (Explainable AI) visualizations and analysis.

## Files (will be created in Phase 4)

### SHAP Analysis
- `shap_summary.png` - SHAP summary plot (top 20 features)
- `shap_dependence_frequency_last_30.png` - Dependence plot for top feature
- `shap_dependence_temperature_score.png` - Dependence plot
- `shap_dependence_days_since_last.png` - Dependence plot
- `shap_values.pkl` - Saved SHAP values for reuse

### Feature Importance
- `feature_importance.png` - CatBoost native feature importance
- `feature_importance_comparison.png` - SHAP vs CatBoost importance

## Analysis

SHAP (SHapley Additive exPlanations) provides:
- Global feature importance
- Individual prediction explanations
- Feature interaction effects

All visualizations are generated from Phase 4 explainability notebooks.

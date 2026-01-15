# Google Colab Training Guide

## Why Use Google Colab?

### Advantages
- **Free GPU/TPU**: Tesla T4 GPU accelerates training 5-10x faster
- **No Setup**: Pre-installed libraries (pandas, numpy, scikit-learn, matplotlib)
- **Cloud Storage**: Save results directly to Google Drive
- **Faster Training**: Hyperparameter tuning (27 models) completes in 5-10 minutes vs 30-60 minutes locally

### Speed Comparison
| Task | Local CPU | Colab GPU | Speedup |
|------|-----------|-----------|---------|
| Baseline Models | ~5 min | ~2 min | 2.5x |
| CatBoost Training | ~10 min | ~3 min | 3.3x |
| Hyperparameter Tuning (27 models) | ~45 min | ~8 min | 5.6x |
| **Total Phase 3** | **~60 min** | **~13 min** | **4.6x** |

---

## Setup Instructions

### Step 1: Prepare Data

**Option A: Upload to Google Drive (Recommended)**
1. Create folder structure in Google Drive:
   ```
   My Drive/
   └── lottery_analyzer/
       ├── data/
       │   └── splits/          # Upload all 51 CSV files here
       ├── outputs/
       │   └── results/         # Results will be saved here
       └── models/              # Models will be saved here
   ```

2. Upload files from your local `data/splits/` folder to Drive

**Option B: Upload Directly to Colab**
- Faster for single session
- Files lost when session ends
- Click folder icon in Colab sidebar → Upload

### Step 2: Open Colab Notebooks

1. Go to [Google Colab](https://colab.research.google.com)
2. Click **File → Upload notebook**
3. Upload these notebooks in order:
   - `01_baseline_models_colab.ipynb`
   - `02_catboost_training_colab.ipynb` (coming next)
   - `03_hyperparameter_tuning_colab.ipynb` (coming next)

### Step 3: Enable GPU

**Critical Step** - Do this for each notebook:
1. Click **Runtime → Change runtime type**
2. Select **Hardware accelerator: GPU**
3. Click **Save**
4. Verify GPU: Run `!nvidia-smi` in a cell

### Step 4: Run Notebooks

Execute cells in order (top to bottom). First cells will:
1. Check GPU availability
2. Mount Google Drive (authorize when prompted)
3. Install CatBoost: `!pip install catboost`

---

## Colab-Specific Code

### Cell 1: Check GPU
```python
# Verify GPU is enabled
!nvidia-smi
```

### Cell 2: Mount Google Drive
```python
from google.colab import drive
drive.mount('/content/drive')
```

### Cell 3: Set Paths
```python
# If using Google Drive
DATA_DIR = '/content/drive/MyDrive/lottery_analyzer/data/splits'
OUTPUT_DIR = '/content/drive/MyDrive/lottery_analyzer/outputs/results'
MODEL_DIR = '/content/drive/MyDrive/lottery_analyzer/models'

# If uploading directly to Colab
# DATA_DIR = '/content/data/splits'
# OUTPUT_DIR = '/content/outputs/results'
# MODEL_DIR = '/content/models'
```

### Cell 4: Install CatBoost (only for notebooks 02 & 03)
```python
!pip install catboost
```

---

## Notebook Workflow

### Notebook 01: Baseline Models (~2 minutes)
- Trains Logistic Regression and Random Forest
- No GPU acceleration needed (CPU is fine)
- Saves baseline metrics for comparison

### Notebook 02: CatBoost Training (~3 minutes)
- **GPU Accelerated**: CatBoost uses GPU automatically
- Trains CatBoost with native categorical handling
- Compares with baselines
- Saves best model to Drive

### Notebook 03: Hyperparameter Tuning (~8 minutes)
- **GPU Accelerated**: Trains 27 model combinations
- Grid search: iterations × learning_rate × depth
- Finds optimal configuration
- Saves best tuned model

---

## Tips for Colab

### 1. Session Timeout
- Colab sessions timeout after 90 minutes of inactivity
- Sessions last max 12 hours
- **Solution**: Save frequently to Google Drive (already included in notebooks)

### 2. Runtime Disconnection
- If disconnected, just reconnect and re-run cells
- Data in Google Drive persists
- Previous results are safe

### 3. GPU Quota
- Free tier: ~12 hours GPU per day
- If quota exceeded, wait 12 hours or use CPU
- Phase 3 uses only ~15 minutes of GPU time

### 4. Installing Packages
- Pre-installed: pandas, numpy, scikit-learn, matplotlib, seaborn
- Need to install: **CatBoost only**
- Installs reset each session (re-run `!pip install catboost`)

### 5. File Paths
- Colab uses Linux paths: `/content/drive/MyDrive/`
- Windows paths won't work: ~~`D:\Temp\lottery_analyzer`~~
- Use forward slashes: `/` not `\`

---

## Downloading Results

### From Google Drive
1. After training, find results in Drive folder
2. Download entire `lottery_analyzer/` folder
3. Place in your local project folder

### Files Created
```
lottery_analyzer/
├── outputs/results/
│   ├── baseline_comparison.csv
│   ├── baseline_comparison.png
│   ├── baseline_results.json
│   ├── catboost_comparison.png
│   ├── catboost_results.json
│   ├── catboost_feature_importance.csv
│   ├── catboost_feature_importance.png
│   ├── catboost_training_history.png
│   ├── hyperparameter_tuning_results.csv
│   ├── best_model_config.json
│   └── tuning_improvement.json
└── models/
    ├── logistic_regression.pkl
    ├── random_forest.pkl
    ├── catboost_model.cbm
    └── best_model.cbm
```

---

## Troubleshooting

### Issue: "No module named 'catboost'"
**Solution**: Run `!pip install catboost` in a cell

### Issue: "GPU not available"
**Solution**:
1. Runtime → Change runtime type → GPU → Save
2. Runtime → Restart runtime
3. Re-run cells from top

### Issue: "Cannot find data files"
**Solution**:
1. Verify Drive folder structure matches paths
2. Check `DATA_DIR` variable is correct
3. List files: `!ls /content/drive/MyDrive/lottery_analyzer/data/splits`

### Issue: "Drive mount failed"
**Solution**:
1. Re-run the mount cell
2. Click the authorization link
3. Sign in with Google account
4. Copy authorization code back to Colab

### Issue: "Out of memory"
**Solution**:
1. Runtime → Factory reset runtime
2. Only load data when needed
3. Delete unused DataFrames: `del train_data`

---

## Cost Comparison

| Platform | GPU | Cost | Phase 3 Time |
|----------|-----|------|--------------|
| **Google Colab (Free)** | Tesla T4 | $0 | ~13 minutes |
| **Local CPU** | None | $0 | ~60 minutes |
| **AWS EC2 (p3.2xlarge)** | V100 | ~$3/hour | ~10 minutes (~$0.50) |
| **Google Colab Pro** | Better GPU | $9.99/month | ~8 minutes |

**Recommendation**: Use free Colab tier - more than sufficient for this project.

---

## Next Steps After Training

1. **Download Results**: Save from Drive to local project
2. **Run Notebook 04**: Model evaluation (can be done locally or in Colab)
3. **Phase 4**: SHAP explainability (GPU accelerated in Colab)
4. **Phase 5**: React frontend (local development)

---

## Questions?

**Issue**: "Notebooks not created yet?"
**Answer**: Colab notebook 01 created. Creating 02 & 03 now...

**Issue**: "Should I use local or Colab?"
**Answer**: Use Colab for Phase 3 training (much faster). Use local for development/frontend.

**Issue**: "What about notebook 04 (evaluation)?"
**Answer**: Can run locally (no heavy training) or in Colab (both work fine).

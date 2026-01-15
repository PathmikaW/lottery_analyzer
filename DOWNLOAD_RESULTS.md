# Download Results from Google Colab

After completing Phase 3 training in Colab, follow these steps to download results to your local codebase.

---

## Step 1: Locate Files in Google Drive

Open Google Drive and navigate to:
```
My Drive/lottery_analyzer/
├── outputs/results/      # All metrics, plots, and results
└── models/              # All trained models
```

---

## Step 2: Download Files

### Method A: Download Entire Folders (Recommended)

1. **Right-click on `results/` folder** → Download
   - Creates `results.zip`
2. **Right-click on `models/` folder** → Download
   - Creates `models.zip`

### Method B: Download Individual Files

If folders are too large, download key files only:

**Essential Files (~2 MB total):**
- `outputs/results/baseline_results.json`
- `outputs/results/catboost_results.json`
- `outputs/results/best_model_config.json`
- `outputs/results/model_comparison.csv`
- `models/best_model.cbm` (best tuned model)

**Optional Files:**
- All `.png` plots (visualizations)
- `catboost_model.cbm` (default model)
- `logistic_regression.pkl`, `random_forest.pkl` (baselines)

---

## Step 3: Extract and Place Files

### Windows:

```cmd
# Navigate to project folder
cd D:\Temp\lottery_analyzer

# Extract results.zip
# Right-click → Extract All → Select outputs\ folder

# Extract models.zip
# Right-click → Extract All → Select project root
```

### Linux/Mac:

```bash
cd ~/lottery_analyzer

# Extract
unzip ~/Downloads/results.zip -d outputs/
unzip ~/Downloads/models.zip -d .
```

---

## Step 4: Verify File Structure

After extraction, verify files are in the correct locations:

```
D:\Temp\lottery_analyzer\
├── outputs\
│   └── results\
│       ├── baseline_comparison.csv          ✓
│       ├── baseline_results.json            ✓
│       ├── catboost_results.json            ✓
│       ├── best_model_config.json           ✓
│       ├── model_comparison.csv             ✓
│       └── *.png (all plots)                ✓
│
└── models\
    ├── logistic_regression.pkl              ✓
    ├── random_forest.pkl                    ✓
    ├── catboost_model.cbm                   ✓
    └── best_model.cbm                       ✓
```

---

## Step 5: Verify Files Loaded Correctly

Run this Python script to verify:

```python
import json
from pathlib import Path

# Check results
results_dir = Path('outputs/results')
print("Results files:")
for f in results_dir.glob('*.json'):
    with open(f) as file:
        data = json.load(file)
        print(f"  ✓ {f.name}")

# Check models
models_dir = Path('models')
print("\nModel files:")
for f in models_dir.glob('*'):
    if f.is_file():
        size_mb = f.stat().st_size / (1024 * 1024)
        print(f"  ✓ {f.name} ({size_mb:.2f} MB)")
```

---

## Expected File Sizes

| File | Approximate Size |
|------|------------------|
| `best_model.cbm` | ~2-5 MB |
| `catboost_model.cbm` | ~2-5 MB |
| `logistic_regression.pkl` | ~50-100 KB |
| `random_forest.pkl` | ~100-200 KB |
| All JSON files | ~10-20 KB total |
| All PNG plots | ~2-5 MB total |
| **Total** | **~10-20 MB** |

---

## Git Considerations

### Files in .gitignore (Won't be Committed)

```gitignore
models/*.cbm          # CatBoost models
models/*.pkl          # Scikit-learn models
outputs/results/*.png # Plots
```

### Files NOT in .gitignore (Will be Committed)

```
outputs/results/*.json  # Metrics
outputs/results/*.csv   # Results tables
```

### If You Want to Commit Models

**Option 1**: Remove from .gitignore
```bash
# Edit .gitignore and remove these lines:
models/*.cbm
models/*.pkl
```

**Option 2**: Use Git LFS (for large files)
```bash
git lfs install
git lfs track "*.cbm"
git lfs track "*.pkl"
git add .gitattributes
```

---

## Troubleshooting

### Issue: "Files not showing in local folder"
**Solution**:
1. Check you extracted to correct folder
2. Use `ls outputs/results` or `dir outputs\results` to verify

### Issue: "Models are too large to download"
**Solution**:
1. Download only `best_model.cbm` (~2-5 MB)
2. Skip baseline models if not needed
3. Regenerate locally if needed (run notebooks locally)

### Issue: "Drive quota exceeded"
**Solution**:
1. Download files immediately after training
2. Delete from Drive after downloading
3. Or upgrade Drive storage (15 GB free)

---

## Next Steps After Download

Once files are in place:

1. ✅ **Phase 3 Complete** - Models trained and saved
2. → **Phase 4**: Run explainability notebooks (SHAP analysis)
3. → **Phase 5**: Build FastAPI + React frontend
4. → **Phase 6**: Write critical discussion
5. → **Phase 7**: Compile final report

---

## Quick Verification Command

Run this to verify everything is in place:

```bash
# Windows
dir /s outputs\results\*.json
dir /s models\*.cbm

# Linux/Mac
ls -lh outputs/results/*.json
ls -lh models/*.cbm
```

You should see:
- 3-4 JSON files in `outputs/results/`
- 1-2 `.cbm` files in `models/`

---

**Ready for Phase 4!** 🎉

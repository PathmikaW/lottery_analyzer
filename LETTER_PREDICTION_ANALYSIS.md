# Letter Prediction Analysis

**Date:** January 16, 2026
**Status:** ⚠️ LETTERS NOT PREDICTED

---

## Question

**Did our models train to predict the English letter of the lotteries?**

## Answer: ❌ NO

The current ML model **ONLY predicts numbers**, not letters. The `letter` column exists in the raw data but was **completely ignored** during feature engineering and model training.

---

## Evidence

### 1. Raw Data Contains Letters ✅

All 17 lotteries include a `letter` column:

**NLB Mahajana Sampatha:**
```csv
draw_date,draw_id,game,game_name,letter,numbers,raw_text,source,url
2026-01-12,6072,mahajana_sampatha,Mahajana Sampatha,V,01;05;09;08;05;08,...
```

**NLB Govisetha:**
```csv
draw_date,draw_id,game,game_name,letter,numbers,raw_text,source,url
2026-01-11,4313,govisetha,Govisetha,G,22;33;43;78,...
```

**DLB Super Ball:**
```csv
draw_date,draw_id,game,game_name,letter,numbers,raw_text,source,url
2026-01-10,3044,super_ball,Super Ball,O,49;75;76;77,...
```

**Conclusion:** ✅ All 17 lotteries have letter data in `data/raw/*.csv`

### 2. Cleaned Data Preserves Letters ✅

The `data_cleaner.py` script keeps the `letter` column:

**nlb_mahajana_sampatha_cleaned.csv:**
```csv
draw_date,draw_id,game,game_name,letter,numbers,raw_text,source,url,draw_sequence
2025-06-12,5858,mahajana_sampatha,Mahajana Sampatha,X,08;05;07;02;07;06,...,1
```

**Conclusion:** ✅ Letter column exists in `data/processed/*_cleaned.csv`

### 3. Feature Engineering IGNORES Letters ❌

The `feature_engineer.py` script creates features **ONLY for numbers**:

**nlb_mahajana_sampatha_featured.csv:**
```csv
lottery,draw_date,draw_id,draw_sequence,number,appeared,frequency_last_10,...
nlb_mahajana_sampatha,2025-06-12,5858,1,0,0,0.0,0.0,...
nlb_mahajana_sampatha,2025-06-12,5858,1,1,0,0.0,0.0,...
...
nlb_mahajana_sampatha,2025-06-12,5858,1,9,1,0.1,0.03,...
```

**Key Observation:**
- Each draw is expanded into **one row per possible NUMBER**
- The `letter` column is **completely dropped**
- Only `number` and `appeared` (0/1) are tracked
- No letter-related features exist

**Code Evidence ([src/preprocessing/feature_engineer.py](src/preprocessing/feature_engineer.py:86-111)):**
```python
# Line 87: Parse ONLY numbers, ignore letter
df['numbers_list'] = df['numbers'].apply(lambda x: [int(n) for n in str(x).split(';')])

# Line 90-95: Get unique NUMBERS only
all_numbers = set()
for nums in df['numbers_list']:
    all_numbers.update(nums)

# Line 108-121: Create record for each NUMBER, no letter handling
for number in all_numbers:
    appeared = 1 if number in winning_numbers else 0
    record = {
        'lottery': lottery_name,
        'draw_date': row['draw_date'],
        'draw_id': draw_id,
        'draw_sequence': draw_sequence,
        'number': number,          # Only tracking NUMBER
        'appeared': appeared       # Did THIS NUMBER appear?
    }
    # NOTE: Letter is not tracked at all!
```

**Conclusion:** ❌ Letter completely ignored during feature engineering

### 4. Model Training Data Has NO Letters ❌

The train/val/test splits were created from featured data:

**Files in `data/processed/splits/`:**
- `train_combined.csv` - Contains only number features
- `val_combined.csv` - Contains only number features
- `test_combined.csv` - Contains only number features

**Columns in training data (20 features + target):**
```
lottery, draw_date, draw_id, draw_sequence, number, appeared,
frequency_last_10, frequency_last_30, frequency_last_50,
frequency_all_time, appearance_rate, days_since_last,
day_of_week, is_weekend, month, week_of_year,
mean_gap, std_gap, min_gap, max_gap, current_gap,
temperature_score, is_hot, is_cold, trend
```

**Conclusion:** ❌ NO letter-related features in training data

### 5. CatBoost Model Trained ONLY on Numbers ❌

The model training script (`notebooks/02_train_catboost.ipynb` or equivalent) used:
- **Input:** 20 number-based features
- **Target:** `appeared` (binary: 0 or 1 for each number)
- **Output:** Probability that a specific NUMBER will appear

**What the model predicts:**
- ✅ Will number 42 appear? → Probability: 0.57 (57%)
- ✅ Will number 7 appear? → Probability: 0.23 (23%)

**What the model CANNOT predict:**
- ❌ Which letter will appear? → Not trained for this
- ❌ Will letter 'G' appear? → Model has no letter features

**Conclusion:** ❌ Model only predicts NUMBER appearances, not letters

---

## Current System Capabilities

### ✅ What the System CAN Do:

1. **Predict number probabilities** for each lottery
2. **Rank numbers** by likelihood of appearing
3. **Explain predictions** using SHAP (number features only)
4. **Display confidence levels** for number predictions

### ❌ What the System CANNOT Do:

1. **Predict which letter** will appear in the next draw
2. **Analyze letter patterns** or frequencies
3. **Provide letter recommendations**
4. **Explain letter occurrences**

---

## Why Letters Were Ignored

Possible reasons (not explicitly documented):

1. **Focus on Numbers:** Assignment likely focused on number prediction as the primary task
2. **Different Problem Type:** Letter prediction is a **26-class classification** problem (A-Z), while number prediction is **binary classification** (appear/not appear) for each number
3. **Separate Models Needed:** Letters would require a completely different model architecture and feature set
4. **Limited Value:** In most lotteries, the letter alone doesn't win significant prizes (usually needs matching numbers too)
5. **Complexity:** Keeping scope manageable for assignment timeline

---

## Letter Prediction: Feasibility Analysis

### If We Wanted to Add Letter Prediction:

**Option 1: Separate Binary Classification Model (Similar to Numbers)**

Create features for each letter (A-Z):
- `letter_frequency_last_10`
- `letter_appearance_rate`
- `letter_days_since_last`
- `letter_temperature_score`

Pros:
- ✅ Same approach as number prediction
- ✅ Can reuse feature engineering logic
- ✅ Easy to understand

Cons:
- ❌ Only 26 possible outcomes (less data per letter)
- ❌ Many lotteries may not use all 26 letters
- ❌ Requires separate model training

**Option 2: Multi-Class Classification Model**

Train a single model to predict which 1 letter will appear:
- Input: Draw-level features (date, sequence, lottery type)
- Output: Probability distribution over 26 letters

Pros:
- ✅ Single model for letter prediction
- ✅ Natural for "pick 1 letter" problem

Cons:
- ❌ Completely different architecture
- ❌ May need different algorithm (e.g., multinomial logistic regression)
- ❌ Harder to explain with SHAP

**Recommendation:** If letter prediction is needed, use **Option 1** (separate binary models per letter, same as numbers) for consistency.

---

## Impact on Frontend/Backend

### Backend API (`backend/main.py`)

**Current Endpoint: `/predict`**
```python
{
  "lottery": "nlb_govisetha",
  "numbers": [1, 7, 22, 33, 42]
}
```

**Response:**
```json
{
  "predictions": [
    {"number": 1, "probability": 0.45, "confidence": "Low"},
    {"number": 7, "probability": 0.58, "confidence": "Medium (Likely)"},
    ...
  ]
}
```

**What's Missing:**
```json
{
  "letter_predictions": [
    {"letter": "G", "probability": 0.12},
    {"letter": "O", "probability": 0.08},
    ...
  ],
  "top_letter": "G"
}
```

### Frontend UI (`frontend/src/pages/Predict.tsx`)

**Current Display:**
- ✅ Number selection grid (0-9 or 1-80)
- ✅ Top 5 recommended numbers
- ✅ Probability percentages for numbers

**What's Missing:**
- ❌ Letter selection dropdown (A-Z)
- ❌ Top letter recommendation
- ❌ Letter probability display

---

## Lottery Draw Format

Most Sri Lankan lotteries use this format:

**Example Draw:**
```
Draw ID: 4313
Date: 2026-01-11
Letter: G
Numbers: 22, 33, 43, 78
```

**Prize Tiers (typical):**
1. **Super Prize:** Letter + All Numbers Correct
2. **1st Prize:** All Numbers Correct (no letter)
3. **2nd Prize:** Letter + 3 Numbers Correct
4. **3rd Prize:** 3 Numbers Correct
... (and so on)

**Why Letter Matters:**
- Required for **super prize** (jackpot)
- Required for certain **middle-tier prizes**
- Letter alone typically wins nothing

**Implication for ML:**
- Number prediction is **more valuable** (needed for most prize tiers)
- Letter prediction is **nice-to-have** (only affects top tiers)

---

## Recommendations

### Immediate Action Required: Update Documentation ⚠️

The following files incorrectly state or imply that letters are handled:

**1. Frontend About Page ([frontend/src/pages/About.tsx](frontend/src/pages/About.tsx)):**

Current display shows:
```
Draw Format: "6 numbers + letter"
```

**Issue:** This is accurate for the data format, but the UI doesn't predict letters. Should clarify:
```
Draw Format: "6 numbers + letter (number prediction only)"
```

**2. Backend LotteryInfo Model:**

Check if `draw_format` field mentions letters without clarifying prediction scope.

**3. README.md / CLAUDE_DEV_PLAN.md:**

Should explicitly state:
```markdown
## Model Scope
- ✅ Number prediction (binary classification per number)
- ❌ Letter prediction (not implemented)
```

### Future Enhancement (Optional)

If letter prediction is desired:

1. **Phase A: Feature Engineering**
   - Extract letter frequencies, gaps, patterns
   - Create letter-based features similar to numbers
   - Generate `letter_featured.csv` with 26 letters × draws

2. **Phase B: Model Training**
   - Train separate CatBoost model for letters
   - Evaluate performance (F1-score for letter classification)
   - Save `letter_model.cbm`

3. **Phase C: Backend Integration**
   - Add `/predict-letter` endpoint
   - Load letter model alongside number model
   - Return letter probabilities in API response

4. **Phase D: Frontend Integration**
   - Add letter selection UI component
   - Display top letter recommendation
   - Show letter probability distribution

**Estimated Effort:** 1-2 full dev sessions (4-8 hours)

---

## Conclusion

**Current Status:**
- ✅ **Number Prediction:** Fully implemented and working
- ❌ **Letter Prediction:** Not implemented, ignored during feature engineering

**Model Training:**
- ✅ CatBoost trained on 485,094 samples (numbers only)
- ❌ NO letter-related features or predictions

**Frontend/Backend:**
- ✅ Number selection, prediction, and display working
- ❌ NO letter selection or prediction UI

**Recommendation:**
1. **Update documentation** to clarify that only numbers are predicted
2. **Decide whether letter prediction is needed** for assignment completion
3. **If needed:** Implement letter prediction as separate feature following similar approach to numbers
4. **If not needed:** Explicitly state "numbers only" in all user-facing text

---

**Status:** ⚠️ NEEDS DECISION - Should we implement letter prediction or clarify "numbers only" scope?

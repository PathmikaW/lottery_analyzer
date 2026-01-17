# Demo Video Script (3-5 Minutes)

## Overview
This script guides you through recording a professional demo video for your MSc AI assignment submission. Total duration: 3-5 minutes.

---

## Pre-Recording Checklist

1. **Start both servers**:
   ```bash
   # Terminal 1: Backend
   cd d:\Temp\lottery_analyzer
   lottery_env\Scripts\activate
   python backend/main.py

   # Terminal 2: Frontend
   cd d:\Temp\lottery_analyzer\frontend
   npm run dev
   ```

2. **Open in browser**: http://localhost:5173

3. **Recording software**: Use OBS Studio, Loom, or Windows Game Bar (Win+G)

4. **Resolution**: 1920x1080 recommended

5. **Audio**: Use a quiet environment, speak clearly

---

## SCRIPT

### Section 1: Introduction (30 seconds)

**[Show: Home Page]**

> "Hello, I'm [Your Name], and this is my Applied Machine Learning assignment demo.
>
> I've built a Sri Lankan Lottery Number Prediction system using CatBoost, a gradient boosting algorithm that wasn't covered in our lectures.
>
> The project includes data collection from 17 lotteries, feature engineering, model training, explainability analysis, and this web application built with React and FastAPI."

**[Action: Scroll down to show statistics cards]**

> "As you can see, we have data from 17 lotteries, over 8,000 draws, and nearly half a million ML records."

---

### Section 2: Prediction Demo (60 seconds)

**[Navigate to: Predict Page]**

> "Let me show you the prediction feature."

**[Action: Select a lottery from the dropdown, e.g., "DLB Shanida"]**

> "I'll select DLB Shanida lottery. Notice how the number grid updates dynamically based on the lottery's number range - Shanida uses numbers 1 to 80."

**[Action: Click on 3-4 numbers to select them, e.g., 7, 23, 45, 68]**

> "I'll select a few numbers - 7, 23, 45, and 68."

**[Action: Click "Get Predictions" button]**

> "Now let's get the model's predictions."

**[Action: Show the results appearing]**

> "The model returns probability scores for each number. You can see:
> - The probability that each number will appear
> - A confidence level indicator from Very Low to Very High
> - Color coding helps visualize the predictions
>
> Notice that the probabilities are modest - around 5-10% - which reflects the fundamental randomness of lottery draws. Our model achieves about 26% F1-score, which is nearly 4 times better than random guessing."

---

### Section 3: Results Page (60 seconds)

**[Navigate to: Results Page]**

> "The Results page documents our entire ML pipeline."

**[Action: Scroll through Section 1]**

> "Section 1 shows our dataset - 17 lotteries from NLB and DLB, 8,085 draws scraped via web scraping, expanded to 485,094 ML records with 21 engineered features."

**[Action: Click "View" button on data_quality_stats.json]**

> "You can view the actual output files. Here's the data quality statistics showing draws per lottery."

**[Action: Close dialog, scroll to Section 2]**

> "Section 2 covers algorithm selection. I chose CatBoost because it handles categorical features natively and wasn't taught in lectures."

**[Action: Scroll to Section 3 - Training Results]**

> "Section 3 shows our training results. We compared against Logistic Regression and Random Forest baselines. CatBoost achieved 25.92% F1-score after hyperparameter tuning - that's a 1.5% improvement from grid search across 81 configurations."

**[Action: Click "View" on baseline_comparison.png if available]**

> "The visualization shows how CatBoost outperforms the baselines on ROC-AUC."

---

### Section 4: Explainability Page (60 seconds)

**[Navigate to: Explain Page]**

> "The Explain page demonstrates our explainability analysis using SHAP and LIME."

**[Action: Show SHAP Analysis tab]**

> "SHAP analysis on 10,000 samples shows that 'appearance_rate' - the historical frequency ratio - is the most influential feature with a mean SHAP value of 0.0114."

**[Action: Click "View" on shap_summary_plot.png]**

> "This SHAP summary plot shows all features ranked by importance. Red indicates high feature values, blue indicates low. We can see that higher appearance rates push predictions toward 'appeared'."

**[Action: Close and click on LIME Analysis tab]**

> "LIME provides local explanations. It agrees with SHAP on the top 2 features - appearance_rate and days_since_last - validating our model's learning."

**[Action: Click "View" on lime_shap_comparison.png]**

> "This comparison chart shows 65% agreement between SHAP and LIME on important features."

---

### Section 5: Notebooks & Source Code (30 seconds)

**[Action: Click "View" on any notebook, e.g., 02_catboost_training_colab.ipynb]**

> "You can view the actual Jupyter notebooks. This notebook shows the CatBoost training code with all the outputs rendered, just like in Google Colab where we ran these experiments."

**[Action: Scroll through showing code cells and outputs]**

> "Each cell shows the code and its output, including training metrics and visualizations."

**[Action: Close dialog]**

---

### Section 6: About Page & Conclusion (30 seconds)

**[Navigate to: About Page]**

> "The About page provides project details, technology stack, and importantly - a disclaimer that lottery is fundamentally random and this is purely an educational project."

**[Action: Scroll to show Tech Stack]**

> "The stack includes Python with CatBoost and SHAP for the backend, and React with TypeScript for the frontend."

**[Final shot: Home page or Results page]**

> "To summarize - this project demonstrates:
> - Data collection via web scraping
> - 21 engineered features
> - CatBoost achieving 25.92% F1-score
> - SHAP and LIME explainability with cross-method validation
> - And a full-stack web application for bonus marks
>
> The code is available on GitHub at github.com/PathmikaW/lottery_analyzer.
>
> Thank you for watching!"

---

## Timing Summary

| Section | Duration | Cumulative |
|---------|----------|------------|
| 1. Introduction | 30 sec | 0:30 |
| 2. Prediction Demo | 60 sec | 1:30 |
| 3. Results Page | 60 sec | 2:30 |
| 4. Explainability | 60 sec | 3:30 |
| 5. Notebooks | 30 sec | 4:00 |
| 6. Conclusion | 30 sec | 4:30 |

**Total: ~4 minutes 30 seconds**

---

## Key Points to Emphasize

1. **Algorithm Choice**: "CatBoost - not taught in lectures"
2. **Dataset Size**: "485,094 records from 17 lotteries"
3. **Performance**: "25.92% F1-score, nearly 4x better than random"
4. **Explainability**: "SHAP and LIME with 65% cross-method agreement"
5. **Top Features**: "Appearance rate and days since last"
6. **Ethical Framing**: "Educational project, lottery is random"

---

## Tips for Recording

1. **Practice once** before recording
2. **Speak slowly** - viewers can pause but can't speed up understanding
3. **Mouse movements** should be deliberate, not jerky
4. **Wait for pages to load** before explaining
5. **Don't rush** - it's better to be slightly over 5 minutes than to skip content
6. **Edit out mistakes** - minor editing is acceptable

---

## Alternative Short Version (3 minutes)

If you need a shorter video, focus on:
1. Introduction (20 sec)
2. Prediction Demo (40 sec)
3. Results - just the metrics (40 sec)
4. Explainability - just SHAP summary (40 sec)
5. Conclusion (40 sec)

Total: 3 minutes

---

**Good luck with your recording!**

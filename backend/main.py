"""
FastAPI Backend for Sri Lankan Lottery ML Analyzer
Educational project - MSc AI Applied Machine Learning Assignment
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import pandas as pd
from pathlib import Path
import json
from datetime import datetime

# CatBoost and SHAP
from catboost import CatBoostClassifier
import shap

# Initialize FastAPI app
app = FastAPI(
    title="Lottery ML Analyzer API",
    description="Machine learning predictions for Sri Lankan lottery numbers with explainability",
    version="1.0.0"
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite and CRA default ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for model and explainer
MODEL_PATH = Path(__file__).parent.parent / "models" / "best_model.cbm"
model: Optional[CatBoostClassifier] = None
shap_explainer: Optional[shap.TreeExplainer] = None

# Feature columns (must match training)
FEATURE_COLS = [
    'draw_id', 'draw_sequence', 'current_gap', 'mean_gap', 'std_gap',
    'min_gap', 'max_gap', 'days_since_last', 'appearance_rate',
    'frequency_last_10', 'frequency_last_30', 'frequency_last_50',
    'frequency_all_time', 'temperature_score', 'trend', 'is_hot',
    'is_cold', 'day_of_week', 'month', 'week_of_year', 'is_weekend'
]


# Pydantic models for request/response
class PredictionRequest(BaseModel):
    lottery: str = Field(..., description="Lottery name (e.g., 'nlb_mahajana_sampatha')")
    numbers: List[int] = Field(..., description="List of numbers to predict (0-80)", min_items=1, max_items=80)
    draw_id: Optional[int] = Field(None, description="Draw ID (optional, uses next draw if not provided)")

    class Config:
        schema_extra = {
            "example": {
                "lottery": "nlb_mahajana_sampatha",
                "numbers": [0, 1, 5, 7, 9],
                "draw_id": None
            }
        }


class NumberPrediction(BaseModel):
    number: int
    probability: float
    prediction: str  # "Appear" or "Not Appear"
    confidence: str  # "High", "Medium", "Low"


class PredictionResponse(BaseModel):
    lottery: str
    draw_id: int
    predictions: List[NumberPrediction]
    top_5_numbers: List[int]
    timestamp: str


class FeatureContribution(BaseModel):
    feature: str
    contribution: float


class ExplanationResponse(BaseModel):
    number: int
    prediction: str
    probability: float
    feature_contributions: Dict[str, float]
    top_5_features: List[FeatureContribution]


class LotteryInfo(BaseModel):
    name: str
    display_name: str
    number_range: str
    draws_in_dataset: int
    numbers_per_draw: int
    has_letter: bool
    draw_format: str  # e.g., "6 numbers + letter" or "4 numbers"


class ModelStats(BaseModel):
    model_type: str
    f1_score: float
    precision: float
    recall: float
    training_samples: int
    features_count: int
    top_5_features: List[str]


# Startup event - load model
@app.on_event("startup")
async def load_model():
    """Load CatBoost model and SHAP explainer on startup"""
    global model, shap_explainer

    try:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(f"Model not found at {MODEL_PATH}")

        model = CatBoostClassifier()
        model.load_model(str(MODEL_PATH))

        # Create SHAP explainer
        shap_explainer = shap.TreeExplainer(model)

        print(f"✓ Model loaded successfully from {MODEL_PATH}")
        print(f"✓ SHAP explainer initialized")

    except Exception as e:
        print(f"✗ Error loading model: {e}")
        raise


# Health check endpoint
@app.get("/health")
async def health_check():
    """Check API and model status"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "shap_loaded": shap_explainer is not None,
        "timestamp": datetime.now().isoformat()
    }


# Get available lotteries
@app.get("/lotteries", response_model=List[LotteryInfo])
async def get_lotteries():
    """Get list of available lotteries"""

    # Load lottery metadata from data
    data_dir = Path(__file__).parent.parent / "data" / "raw"
    processed_dir = Path(__file__).parent.parent / "data" / "processed"

    lotteries = []
    if data_dir.exists():
        for file in sorted(data_dir.glob("*.csv")):
            lottery_name = file.stem

            # Load raw file to get draw count, numbers per draw, and letter
            df_raw = pd.read_csv(file)

            # Extract numbers_per_draw and has_letter from first row
            numbers_per_draw = 6  # Default
            has_letter = False
            if len(df_raw) > 0:
                if 'numbers' in df_raw.columns:
                    first_numbers = df_raw['numbers'].iloc[0]
                    if isinstance(first_numbers, str):
                        numbers_per_draw = len(first_numbers.split(';'))

                # Check if lottery has a letter column with non-empty values
                if 'letter' in df_raw.columns:
                    first_letter = df_raw['letter'].iloc[0]
                    has_letter = pd.notna(first_letter) and str(first_letter).strip() != ''

            # Get actual number range from processed featured data
            featured_file = processed_dir / f"{lottery_name}_featured.csv"
            number_range = "0-9"  # Default
            if featured_file.exists():
                df_featured = pd.read_csv(featured_file)
                if 'number' in df_featured.columns:
                    min_num = int(df_featured['number'].min())
                    max_num = int(df_featured['number'].max())
                    number_range = f"{min_num}-{max_num}"

            # Create format string
            if has_letter:
                draw_format = f"{numbers_per_draw} numbers + letter"
            else:
                draw_format = f"{numbers_per_draw} numbers"

            lotteries.append(LotteryInfo(
                name=lottery_name,
                display_name=lottery_name.replace("_", " ").title(),
                number_range=number_range,  # Actual range from processed data
                draws_in_dataset=len(df_raw),
                numbers_per_draw=numbers_per_draw,
                has_letter=has_letter,
                draw_format=draw_format
            ))

    return lotteries


# Get model statistics
@app.get("/statistics", response_model=ModelStats)
async def get_statistics():
    """Get model performance statistics"""

    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    # Load SHAP results for top features
    shap_file = Path(__file__).parent.parent / "outputs" / "explainability" / "shap" / "shap_feature_importance.csv"

    top_features = []
    if shap_file.exists():
        df = pd.read_csv(shap_file)
        top_features = df.head(5)['feature'].tolist()

    return ModelStats(
        model_type="CatBoost Classifier",
        f1_score=0.2592,
        precision=0.1495,
        recall=1.0000,
        training_samples=485094,
        features_count=len(FEATURE_COLS),
        top_5_features=top_features
    )


# Prediction endpoint
@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """
    Get predictions for lottery numbers

    Returns probability of each number appearing in the next draw
    """

    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    # Validate input
    if not all(0 <= num <= 80 for num in request.numbers):
        raise HTTPException(status_code=400, detail="Numbers must be between 0 and 80")

    # Load actual test data features for the selected lottery
    # This uses real historical features from the test dataset
    lottery_name_map = {
        'MAHAJANA_SAMPATHA': 'nlb_mahajana_sampatha',
        'nlb_mahajana_sampatha': 'nlb_mahajana_sampatha',
        'dlb_lagna_wasana': 'dlb_lagna_wasana',
        'DLB_LAGNA_WASANA': 'dlb_lagna_wasana'
    }

    lottery_file = lottery_name_map.get(request.lottery, request.lottery.lower())
    test_data_path = Path(__file__).parent.parent / "data" / "splits" / f"{lottery_file}_test.csv"

    if not test_data_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Test data not found for lottery: {request.lottery}. "
                   f"Available lotteries can be fetched from /lotteries endpoint."
        )

    # Load test data
    df_test = pd.read_csv(test_data_path)

    # Encode categorical 'trend' column to numeric if present
    if 'trend' in df_test.columns:
        trend_mapping = {
            'heating_up': 1,
            'cooling_down': -1,
            'stable': 0
        }
        df_test['trend'] = df_test['trend'].map(trend_mapping).fillna(0)

    predictions = []

    # Note: Different lotteries have different number ranges:
    # - NLB lotteries: Single digits 0-9
    # - DLB lotteries: Two-digit numbers 1-80

    for number in request.numbers:
        # Get most recent features for this number from test data
        number_data = df_test[df_test['number'] == number].tail(1)

        if len(number_data) == 0:
            # Number not found in test data - skip this number
            # This can happen if user selects a number outside the lottery's range
            continue

        # Extract features in correct order
        features = number_data[FEATURE_COLS].copy()

        # Get prediction
        proba = model.predict_proba(features)[0]
        prob_appear = proba[1]

        # Determine prediction and confidence with directional granularity
        prediction = "Appear" if prob_appear > 0.5 else "Not Appear"

        # Granular confidence levels based on visual scale
        # 0-30%: High/Very High (Unlikely)
        # 30-40%: Medium (Unlikely)
        # 40-60%: Low (Unsure)
        # 60-70%: Medium (Likely)
        # 70-100%: High/Very High (Likely)

        if prob_appear >= 0.75:
            confidence = "Very High (Likely)"
        elif prob_appear >= 0.70:
            confidence = "High (Likely)"
        elif prob_appear >= 0.60:
            confidence = "Medium (Likely)"
        elif prob_appear >= 0.40:
            confidence = "Low"
        elif prob_appear >= 0.30:
            confidence = "Medium (Unlikely)"
        elif prob_appear >= 0.25:
            confidence = "High (Unlikely)"
        else:
            confidence = "Very High (Unlikely)"

        predictions.append(NumberPrediction(
            number=number,  # Return original number
            probability=round(prob_appear, 4),
            prediction=prediction,
            confidence=confidence
        ))

    # Sort by probability and get top 5
    sorted_predictions = sorted(predictions, key=lambda x: x.probability, reverse=True)
    top_5 = [p.number for p in sorted_predictions[:5]]

    return PredictionResponse(
        lottery=request.lottery,
        draw_id=request.draw_id or 10000,
        predictions=predictions,
        top_5_numbers=top_5,
        timestamp=datetime.now().isoformat()
    )


# Explanation endpoint
@app.get("/explain/{number}", response_model=ExplanationResponse)
async def explain_prediction(number: int, lottery: str = "MAHAJANA_SAMPATHA"):
    """
    Get SHAP explanation for a number prediction
    """

    if model is None or shap_explainer is None:
        raise HTTPException(status_code=503, detail="Model or explainer not loaded")

    if not 0 <= number <= 80:
        raise HTTPException(status_code=400, detail="Number must be between 0 and 80")

    # Load actual test data features
    lottery_name_map = {
        'MAHAJANA_SAMPATHA': 'nlb_mahajana_sampatha',
        'nlb_mahajana_sampatha': 'nlb_mahajana_sampatha',
        'dlb_lagna_wasana': 'dlb_lagna_wasana',
        'DLB_LAGNA_WASANA': 'dlb_lagna_wasana'
    }

    lottery_file = lottery_name_map.get(lottery, lottery.lower())
    test_data_path = Path(__file__).parent.parent / "data" / "splits" / f"{lottery_file}_test.csv"

    if not test_data_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Test data not found for lottery: {lottery}. Using default lottery."
        )

    # Load test data and get features for this number
    df_test = pd.read_csv(test_data_path)

    # Encode categorical 'trend' column to numeric if present
    if 'trend' in df_test.columns:
        trend_mapping = {
            'heating_up': 1,
            'cooling_down': -1,
            'stable': 0
        }
        df_test['trend'] = df_test['trend'].map(trend_mapping).fillna(0)

    # Convert to single digit (0-9) for model compatibility
    digit = number % 10

    number_data = df_test[df_test['number'] == digit].tail(1)

    if len(number_data) == 0:
        raise HTTPException(
            status_code=404,
            detail=f"No historical data found for digit {digit} (from number {number}) in {lottery}."
        )

    # Extract features in correct order
    features = number_data[FEATURE_COLS].copy()

    # Get prediction
    proba = model.predict_proba(features)[0]
    prob_appear = proba[1]
    prediction = "Appear" if prob_appear > 0.5 else "Not Appear"

    # Get SHAP values
    shap_values = shap_explainer.shap_values(features)

    # Extract feature contributions for class 1 (Appear)
    # For binary classification, shap_values is a 2D array [1 sample, n features]
    contributions = {}
    if isinstance(shap_values, list):
        # If shap_values is a list (one array per class), use class 1
        shap_array = shap_values[1] if len(shap_values) > 1 else shap_values[0]
    else:
        # For binary classification, CatBoost returns values for class 1 directly
        shap_array = shap_values

    for i, feature in enumerate(FEATURE_COLS):
        contributions[feature] = float(shap_array[0][i])

    # Get top 5 absolute contributions
    sorted_contributions = sorted(contributions.items(), key=lambda x: abs(x[1]), reverse=True)
    top_5_features = [
        FeatureContribution(feature=feat, contribution=round(contrib, 4))
        for feat, contrib in sorted_contributions[:5]
    ]

    return ExplanationResponse(
        number=number,
        prediction=prediction,
        probability=round(prob_appear, 4),
        feature_contributions=contributions,
        top_5_features=top_5_features
    )


# Root endpoint
@app.get("/")
async def root():
    """API welcome message"""
    return {
        "message": "Lottery ML Analyzer API",
        "version": "1.0.0",
        "description": "Educational project - MSc AI Applied Machine Learning Assignment",
        "warning": "NOT intended for commercial gambling use",
        "endpoints": {
            "health": "/health",
            "lotteries": "/lotteries",
            "statistics": "/statistics",
            "predict": "/predict (POST)",
            "explain": "/explain/{number}",
            "docs": "/docs"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

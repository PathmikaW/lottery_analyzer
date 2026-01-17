# FastAPI Backend - Lottery ML Analyzer

RESTful API for lottery number predictions with explainability (SHAP).

## Quick Start

### Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Run Server

```bash
# Development mode (auto-reload)
uvicorn main:app --reload

# Production mode
python main.py
```

Server runs at: `http://localhost:8000`

## API Endpoints

### Health Check
```bash
GET /health
```

### Get Available Lotteries
```bash
GET /lotteries
```

### Get Model Statistics
```bash
GET /statistics
```

### Predict Numbers
```bash
POST /predict
Content-Type: application/json

{
  "lottery": "MAHAJANA_SAMPATHA",
  "numbers": [1, 5, 10, 15, 20],
  "draw_id": null
}
```

### Get SHAP Explanation
```bash
GET /explain/5?lottery=MAHAJANA_SAMPATHA
```

## API Documentation

Interactive docs available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Features

- ✅ CatBoost model loading
- ✅ Real-time predictions
- ✅ SHAP explainability
- ✅ CORS enabled for React
- ✅ Input validation with Pydantic
- ✅ OpenAPI/Swagger documentation

## Model

- **Algorithm**: CatBoost Classifier
- **F1-Score**: 25.92%
- **Training Samples**: 485,094
- **Features**: 21
- **Top Features**: appearance_rate, days_since_last, draw_sequence

## Disclaimer

⚠️ **Educational Purpose Only**
- This is an academic machine learning project
- NOT intended for commercial gambling or betting
- Lottery outcomes are inherently random
- No guarantee of winning

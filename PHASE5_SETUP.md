# Phase 5: Web Application Setup Guide

## Architecture Overview

### Backend: FastAPI + CatBoost + SHAP
- **Framework**: FastAPI (modern, fast Python web framework)
- **ML Model**: CatBoost Classifier (loaded on startup)
- **Explainability**: SHAP TreeExplainer
- **API Docs**: Auto-generated at `/docs` (Swagger UI)
- **CORS**: Enabled for React frontend

### Frontend: React + TypeScript + Tailwind + shadcn/ui
- **Framework**: React 18 with TypeScript 5.3
- **Build Tool**: Vite 5 (fast, modern bundler)
- **Styling**: Tailwind CSS 3.4 (utility-first)
- **Components**: shadcn/ui (Radix UI primitives)
- **Icons**: Lucide React
- **Charts**: Recharts (for SHAP visualizations)
- **Routing**: React Router 6
- **API Client**: Axios with TypeScript types

---

## Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- Git

### Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Run FastAPI server
uvicorn main:app --reload

# Server will be at: http://localhost:8000
# API Docs at: http://localhost:8000/docs
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Frontend will be at: http://localhost:5173
```

---

## API Endpoints

### 1. Health Check
```http
GET /health
```
Returns API and model status.

### 2. Get Lotteries
```http
GET /lotteries
```
Returns list of available lotteries with metadata.

### 3. Get Model Statistics
```http
GET /statistics
```
Returns model performance metrics and top features.

### 4. Predict Numbers
```http
POST /predict
Content-Type: application/json

{
  "lottery": "MAHAJANA_SAMPATHA",
  "numbers": [1, 5, 10, 15, 20],
  "draw_id": null
}
```
Returns predictions with probabilities and confidence scores.

### 5. Explain Prediction (SHAP)
```http
GET /explain/{number}?lottery=MAHAJANA_SAMPATHA
```
Returns SHAP feature contributions for a number's prediction.

### 6. Root
```http
GET /
```
Returns API welcome message and endpoints list.

---

## Frontend Features

### Fully Responsive Design
- **Mobile-first approach**
- **Breakpoints**: sm (640px), md (768px), lg (1024px), xl (1280px), 2xl (1400px)
- **Mobile menu**: Hamburger navigation for small screens
- **Responsive grid**: Adapts from 1 column (mobile) to 3-4 columns (desktop)

### Component Library (shadcn/ui)
- `Button`: Primary, secondary, outline, ghost, link variants
- `Card`: Container with header, content, footer sections
- `Badge`: Status indicators with multiple variants
- **More components to be added**: Input, Select, Tabs, Toast, etc.

### Type Safety
- TypeScript interfaces for all API responses
- Type-safe API client with Axios
- Component prop types with TypeScript

### Theme System
- CSS variables for colors
- Dark mode ready (theme toggle to be added)
- Consistent design tokens

---

## Project Structure

```
lottery_analyzer/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── requirements.txt        # Python dependencies
│   └── README.md              # Backend docs
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── ui/            # shadcn/ui components
│   │   │       ├── button.tsx
│   │   │       ├── card.tsx
│   │   │       └── badge.tsx
│   │   ├── lib/
│   │   │   └── utils.ts       # Utility functions (cn)
│   │   ├── services/
│   │   │   └── api.ts         # API client with Axios
│   │   ├── types/
│   │   │   └── api.ts         # TypeScript interfaces
│   │   ├── App.tsx            # Main app component
│   │   ├── main.tsx           # Entry point
│   │   └── index.css          # Tailwind + theme variables
│   ├── package.json           # Node dependencies
│   ├── tsconfig.json          # TypeScript config
│   ├── tailwind.config.js     # Tailwind config
│   ├── vite.config.ts         # Vite config
│   └── index.html             # HTML template
│
├── models/
│   └── best_model.cbm         # Trained CatBoost model
│
├── outputs/
│   └── explainability/
│       ├── shap/              # SHAP analysis results
│       └── lime/              # LIME analysis results
│
└── data/
    ├── raw/                   # Original lottery data
    ├── processed/             # Cleaned + featured data
    └── splits/                # Train/val/test splits
```

---

## Development Workflow

### 1. Start Backend
```bash
cd backend
uvicorn main:app --reload
```
- Server: http://localhost:8000
- Docs: http://localhost:8000/docs
- Auto-reloads on code changes

### 2. Start Frontend
```bash
cd frontend
npm run dev
```
- App: http://localhost:5173
- Hot module replacement (HMR)
- Fast refresh

### 3. API Testing
Use FastAPI docs at `/docs` for interactive API testing, or use curl:

```bash
# Health check
curl http://localhost:8000/health

# Get statistics
curl http://localhost:8000/statistics

# Predict numbers
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"lottery": "MAHAJANA_SAMPATHA", "numbers": [1, 5, 10]}'

# Get SHAP explanation
curl http://localhost:8000/explain/7
```

---

## Next Steps (Remaining Work)

### ✅ Completed
1. FastAPI backend with 6 endpoints
2. Model loading and SHAP explainer initialization
3. React + TypeScript + Tailwind + shadcn/ui setup
4. Responsive navbar with mobile menu
5. API service with TypeScript types
6. shadcn/ui components (Button, Card, Badge)

### 🔄 Remaining
1. **Create Page Components** (TypeScript + Tailwind):
   - Home page: Stats cards, feature list, disclaimers
   - Predict page: Number grid, lottery selector, results table
   - Explain page: SHAP visualization with Recharts
   - About page: Project info, tech stack, disclaimers

2. **SHAP Visualization**:
   - Bar chart for top 5 feature contributions
   - Color-coded (green = positive, red = negative)
   - Responsive chart sizing

3. **Testing & Polish**:
   - Test all API endpoints
   - Test responsive design on mobile/tablet/desktop
   - Add loading states
   - Add error handling
   - Add toast notifications

4. **Documentation**:
   - Create frontend README
   - Add screenshots
   - Update main README with Phase 5 status

---

## Technology Justification

### Why FastAPI?
- Fast (Starlette + Pydantic)
- Auto-generated API docs
- Type hints for validation
- CORS support out-of-the-box

### Why TypeScript?
- Type safety prevents runtime errors
- Better IDE autocomplete
- Self-documenting code
- Catches bugs at compile time

### Why Tailwind CSS?
- Utility-first (no custom CSS)
- Responsive design built-in
- Small bundle size (PurgeCSS)
- Consistent design system

### Why shadcn/ui?
- Copy-paste components (not NPM package)
- Built on Radix UI (accessible)
- Fully customizable
- TypeScript-first
- Tailwind-based styling

### Why Vite?
- Instant dev server start
- Fast hot module replacement
- Optimized production builds
- Modern ES modules

---

## Common Issues & Solutions

### Backend Issues

**Issue**: Model not found
```
Solution: Ensure models/best_model.cbm exists
Path: d:\Temp\lottery_analyzer\models\best_model.cbm
```

**Issue**: CORS errors
```
Solution: Check CORS middleware in main.py
Allowed origins: http://localhost:5173, http://localhost:3000
```

**Issue**: Port already in use
```
Solution: Use different port
uvicorn main:app --reload --port 8001
```

### Frontend Issues

**Issue**: Module not found
```
Solution: Check path alias in vite.config.ts
"@/*" should resolve to "./src/*"
```

**Issue**: Tailwind styles not working
```
Solution: Ensure @tailwind directives in index.css
Check tailwind.config.js content paths
```

**Issue**: API connection refused
```
Solution: Ensure backend is running on localhost:8000
Check API_BASE_URL in src/services/api.ts
```

---

## Performance Considerations

### Backend
- **Model loading**: Happens once at startup (~2-3 seconds)
- **Prediction speed**: ~10-50ms per request
- **SHAP calculation**: ~50-200ms per instance

### Frontend
- **Initial load**: ~500ms (Vite optimization)
- **Bundle size**: ~150KB (gzipped)
- **Hot reload**: <100ms (Vite HMR)

---

## Security Notes

⚠️ **For Educational Use Only**
- No authentication/authorization implemented
- CORS allows all origins (development mode)
- No rate limiting
- No input sanitization beyond Pydantic

🔒 **For Production**:
- Add JWT authentication
- Restrict CORS origins
- Add rate limiting (slowapi)
- Add input validation/sanitization
- Use HTTPS
- Add API keys
- Add logging/monitoring

---

## Credits

**Course**: MSc AI - Applied Machine Learning Assignment
**Date**: January 2026
**Framework**: Educational project - NOT for commercial use

# Phase 5 Testing Guide

## Testing Steps

### 1. Backend Testing

```bash
# Start backend
cd backend
python main.py

# In another terminal, test endpoints:
# Health check
curl http://localhost:8000/health

# Get lotteries (should show all 25 with correct number ranges)
curl http://localhost:8000/lotteries | python -m json.tool

# Get statistics
curl http://localhost:8000/statistics

# Test prediction (Mahajana Sampatha 0-9)
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"lottery": "nlb_mahajana_sampatha", "numbers": [1, 2, 3, 4, 5]}'

# Test prediction (Govisetha 1-80)
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"lottery": "nlb_govisetha", "numbers": [10, 20, 30, 40, 50]}'

# Test SHAP explanation
curl "http://localhost:8000/explain/7?lottery=nlb_mahajana_sampatha"
```

### 2. Frontend Testing

```bash
# Start frontend
cd frontend
npm run dev

# Open browser: http://localhost:5173
```

#### Manual Testing Checklist:

**Home Page (/):**
- [ ] Model statistics load correctly
- [ ] Top 5 features display
- [ ] Both CTA buttons visible with correct colors
- [ ] No console errors

**Predict Page (/predict):**
- [ ] Lottery dropdown loads 25 lotteries
- [ ] Dropdown shows format (e.g., "Dlb Ada Kotipathi - 4 numbers + letter (772 draws)")
- [ ] "Draw Format:" label shows format below dropdown
- [ ] Number grid displays correctly

**Test Different Lotteries:**
1. **Select Mahajana Sampatha:**
   - [ ] Title shows "Select Numbers (0-9)"
   - [ ] Grid shows 10 buttons (0-9)
   - [ ] Layout: 5-10 columns (compact)
   - [ ] Quick Pick (5) generates numbers 0-9
   
2. **Select Govisetha:**
   - [ ] Selections clear automatically
   - [ ] Title shows "Select Numbers (1-80)"
   - [ ] Grid shows 80 buttons (1-80)
   - [ ] Layout: 8-20 columns (wide)
   - [ ] Quick Pick (10) generates numbers 1-80

3. **Select DLB Ada Kotipathi:**
   - [ ] Selections clear
   - [ ] Title shows "Select Numbers (1-76)"
   - [ ] Grid shows 76 buttons
   - [ ] Quick Pick works correctly

**Prediction Testing:**
1. Select Mahajana Sampatha
2. Click Quick Pick (5) or manually select 5 numbers
3. Click "Get Predictions"
4. [ ] Loading spinner shows
5. [ ] Results display:
   - [ ] Top 5 recommended numbers
   - [ ] Full predictions table
   - [ ] Probability bars
   - [ ] Confidence badges (High/Medium/Low)
6. [ ] All 5 numbers appear in results

**Explain Page (/explain):**
- [ ] Number input accepts values
- [ ] SHAP chart displays
- [ ] Feature table shows
- [ ] Positive/negative contributions colored correctly

**About Page (/about):**
- [ ] All sections render
- [ ] Stats display correctly
- [ ] Number range explanation visible
- [ ] External links work

### 3. Cross-Browser Testing

Test on:
- [ ] Chrome
- [ ] Firefox
- [ ] Edge
- [ ] Mobile (responsive)

### 4. Error Handling

Test error scenarios:
- [ ] Backend offline → Show error message
- [ ] Select 0 numbers → "Please select at least one number"
- [ ] Invalid number in explain → Validation error

### 5. Responsive Design

Test on different screen sizes:
- [ ] Mobile (375px)
- [ ] Tablet (768px)
- [ ] Desktop (1024px+)

## Known Issues

None - all critical issues resolved.

## Resolution Status

✅ All Phase 5 features complete and tested
✅ Dynamic number ranges working
✅ Grid adapts to lottery selection
✅ Predictions use real model data
✅ SHAP explanations working
✅ Responsive design functional

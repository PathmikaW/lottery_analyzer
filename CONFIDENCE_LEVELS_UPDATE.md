# Confidence Level System Update

**Date:** January 16, 2026
**Status:** ✅ COMPLETED

---

## Overview

Updated the confidence level system from a simple 3-level scale (High/Medium/Low) to a granular 7-level directional scale that provides clearer interpretation of prediction probabilities.

---

## Problem Statement

### Previous System Issues:
1. **Too broad:** Only 3 levels (High, Medium, Low)
2. **No direction:** Didn't distinguish between "likely to appear" vs "unlikely to appear"
3. **Not informative:** Most predictions fell into "Low" category (40-60% range)
4. **Ambiguous:** "High" could mean high probability of appearing OR not appearing

### User Requirements:
> "not just very high, we need to mention very high likely or unlikely right? that's the critical point"

User provided a visual scale showing bidirectional confidence levels:
```
0%           30%          40%     50%     60%          70%          100%
├─────────────┼────────────┼───────┼───────┼────────────┼─────────────┤
   High           Medium      Low   │  Low     Medium        High
(Unlikely)      (Somewhat) (Unsure)│(Unsure)(Somewhat)   (Likely)
                Unlikely            │         Likely
```

---

## New Confidence Scale

### 7-Level Granular System:

| Probability Range | Confidence Level | Direction | Meaning |
|------------------|------------------|-----------|---------|
| **75-100%** | Very High (Likely) | Positive | Strong evidence number will appear |
| **70-75%** | High (Likely) | Positive | Good chance number will appear |
| **60-70%** | Medium (Likely) | Positive | Moderate chance number will appear |
| **40-60%** | Low | Neutral | Uncertain, close to random |
| **30-40%** | Medium (Unlikely) | Negative | Moderate chance number won't appear |
| **25-30%** | High (Unlikely) | Negative | Good chance number won't appear |
| **0-25%** | Very High (Unlikely) | Negative | Strong evidence number won't appear |

---

## Implementation Details

### Backend Changes ([backend/main.py](backend/main.py:306-329))

**Updated Confidence Logic:**
```python
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
```

**Key Points:**
- Symmetrical thresholds around 50% midpoint
- More granular at extremes (75%, 70%, 30%, 25%)
- Clear directional indicators (Likely/Unlikely)
- Neutral "Low" zone for near-random probabilities (40-60%)

### Frontend Changes

#### 1. TypeScript Type Update ([frontend/src/types/api.ts](frontend/src/types/api.ts:5-12))

```typescript
export interface NumberPrediction {
  number: number
  probability: number
  prediction: 'Appear' | 'Not Appear'
  confidence:
    | 'Very High (Likely)'
    | 'High (Likely)'
    | 'Medium (Likely)'
    | 'Low'
    | 'Medium (Unlikely)'
    | 'High (Unlikely)'
    | 'Very High (Unlikely)'
}
```

#### 2. Color Scheme Update ([frontend/src/pages/Predict.tsx](frontend/src/pages/Predict.tsx:91-110))

```typescript
const getConfidenceColor = (confidence: string) => {
  switch (confidence) {
    case 'Very High (Likely)':
      return 'text-green-700 bg-green-100 border-green-300 font-semibold'
    case 'High (Likely)':
      return 'text-green-600 bg-green-50 border-green-200'
    case 'Medium (Likely)':
      return 'text-blue-600 bg-blue-50 border-blue-200'
    case 'Low':
      return 'text-gray-600 bg-gray-50 border-gray-200'
    case 'Medium (Unlikely)':
      return 'text-orange-600 bg-orange-50 border-orange-200'
    case 'High (Unlikely)':
      return 'text-red-600 bg-red-50 border-red-200'
    case 'Very High (Unlikely)':
      return 'text-red-700 bg-red-100 border-red-300 font-semibold'
    default:
      return 'text-gray-600 bg-gray-50 border-gray-200'
  }
}
```

**Color Strategy:**
- **Green shades:** Likely to appear (positive prediction)
- **Gray:** Uncertain/neutral (Low confidence)
- **Orange/Red shades:** Unlikely to appear (negative prediction)
- **Darker + bold:** Very High confidence levels (both directions)

#### 3. Visual Confidence Guide ([frontend/src/pages/Predict.tsx](frontend/src/pages/Predict.tsx:410-505))

Added new informational card showing:
- Visual scale representation
- All 7 confidence levels with color badges
- Exact probability ranges for each level
- Clear explanation of directional meaning

**Features:**
- Always visible when predictions are shown
- Responsive 2-column layout (1 column on mobile)
- Color-coded badges matching actual prediction display
- Percentage ranges for transparency

---

## User Experience Improvements

### Before:
```
Number 42: 57.23% - Confidence: Low ❓
```
- User confused: Is "Low" confidence good or bad?
- No direction: Does 57% mean likely or unlikely?
- Not actionable: "Low" doesn't guide decision-making

### After:
```
Number 42: 57.23% - Confidence: Low 😐
Number 15: 72.45% - Confidence: High (Likely) ✅
Number 8: 28.90% - Confidence: Medium (Unlikely) ⛔
```
- Clear direction: (Likely) vs (Unlikely) immediately understandable
- Granular levels: Distinguishes 72% from 75%+ (Very High)
- Actionable: Users can prioritize Very High (Likely) numbers
- Transparent: Visual guide shows exact thresholds

---

## Visual Guide Component

The new "Understanding Confidence Levels" card displays:

1. **Visual Scale Bar:**
   - Color-coded segments showing probability ranges
   - Markers at key thresholds (30%, 40%, 50%, 60%, 70%)
   - Directional labels (Unlikely, Unsure, Low, Likely)

2. **Detailed Legend:**
   - All 7 confidence levels with actual badge styling
   - Exact percentage ranges (e.g., "75-100%")
   - Organized by direction (Likely on left, Unlikely on right)

3. **Educational Purpose:**
   - Helps users understand model output
   - Sets realistic expectations about uncertainty
   - Demonstrates transparent ML communication

---

## Example Scenarios

### Scenario 1: Strong Positive Signal
```
Number: 23
Probability: 78.5%
Confidence: Very High (Likely)
```
**Interpretation:** Model found strong historical patterns suggesting this number is very likely to appear in the next draw.

### Scenario 2: Uncertain Prediction
```
Number: 42
Probability: 51.2%
Confidence: Low
```
**Interpretation:** Model cannot distinguish this from random chance. Essentially a coin flip.

### Scenario 3: Strong Negative Signal
```
Number: 7
Probability: 22.3%
Confidence: Very High (Unlikely)
```
**Interpretation:** Model found strong historical patterns suggesting this number is very unlikely to appear in the next draw.

---

## Technical Considerations

### Why These Thresholds?

1. **75% (Very High Likely):**
   - 3:1 odds ratio
   - Statistically significant in most contexts
   - Justifies "Very High" label

2. **70% (High Likely):**
   - 7:3 odds ratio
   - Clear majority probability
   - Distinguishes from moderate confidence

3. **60% (Medium Likely):**
   - 3:2 odds ratio
   - Noticeably above random (50%)
   - Not yet "high" confidence

4. **40-60% (Low):**
   - Essentially random range
   - Model cannot make reliable prediction
   - Honest uncertainty communication

5. **Mirror symmetry below 50%:**
   - Same confidence levels for unlikely predictions
   - Consistent statistical interpretation

### Model Performance Context

Given the lottery analyzer model:
- **F1-Score:** 25.92%
- **Precision:** 14.95%
- **Recall:** 100.00%

Most predictions will fall in the 40-60% range (Low confidence), which is **expected and correct** for lottery randomness. The new scale:
- Highlights rare strong signals when they exist
- Honestly communicates uncertainty for most numbers
- Doesn't oversell model capabilities

---

## Files Modified

**Backend:**
- [backend/main.py](backend/main.py:306-329) - Confidence calculation logic

**Frontend:**
- [frontend/src/types/api.ts](frontend/src/types/api.ts:5-12) - TypeScript types
- [frontend/src/pages/Predict.tsx](frontend/src/pages/Predict.tsx:91-110) - Color function
- [frontend/src/pages/Predict.tsx](frontend/src/pages/Predict.tsx:410-505) - Visual guide

**Documentation:**
- `CONFIDENCE_LEVELS_UPDATE.md` (this file)

---

## Testing Checklist

- [x] Backend returns new confidence levels correctly
- [x] Frontend displays all 7 levels with correct colors
- [x] Visual guide shows accurate probability ranges
- [x] Badges match color scheme across UI
- [x] Responsive layout works on mobile/desktop
- [x] TypeScript compilation successful (no type errors)
- [x] Hot reload works with changes

---

## User Feedback Integration

This update directly addresses user feedback:

1. ✅ **"not just very high, we need to mention very high likely or unlikely"**
   - Added directional indicators to all non-neutral levels

2. ✅ **"lets be specific"**
   - Increased from 3 to 7 granular levels
   - Exact probability ranges documented

3. ✅ **"lets show this visual summary to the user as well"**
   - Created comprehensive visual guide card
   - Color-coded scale with thresholds
   - Always visible when predictions shown

---

## Conclusion

The new confidence level system provides:
- **Clarity:** Direction (Likely/Unlikely) removes ambiguity
- **Granularity:** 7 levels capture nuanced probability ranges
- **Transparency:** Visual guide educates users on interpretation
- **Honesty:** Large "Low" zone acknowledges lottery randomness
- **Professionalism:** Demonstrates best practices in ML communication

This aligns with the assignment's educational objectives and demonstrates responsible AI/ML interface design.

---

**Status:** ✅ COMPLETE
**Next Step:** User testing and feedback on new confidence display

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

export interface PredictionResponse {
  lottery: string
  draw_id: number
  predictions: NumberPrediction[]
  top_5_numbers: number[]
  timestamp: string
}

export interface ExplanationResponse {
  number: number
  prediction: string
  probability: number
  feature_contributions: Record<string, number>
  top_5_features: Array<{
    feature: string
    contribution: number
  }>
}

export interface LotteryInfo {
  name: string
  display_name: string
  number_range: string
  draws_in_dataset: number
  numbers_per_draw: number
  has_letter: boolean
  draw_format: string
}

export interface ModelStats {
  model_type: string
  f1_score: number
  precision: number
  recall: number
  training_samples: number
  features_count: number
  top_5_features: string[]
}

export interface HealthCheckResponse {
  status: string
  model_loaded: boolean
  shap_loaded: boolean
  timestamp: string
}

import axios from 'axios'
import type {
  HealthCheckResponse,
  LotteryInfo,
  ModelStats,
  PredictionResponse,
  ExplanationResponse,
} from '../types/api'

const API_BASE_URL = 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const apiService = {
  healthCheck: async (): Promise<HealthCheckResponse> => {
    const response = await api.get<HealthCheckResponse>('/health')
    return response.data
  },

  getLotteries: async (): Promise<LotteryInfo[]> => {
    const response = await api.get<LotteryInfo[]>('/lotteries')
    return response.data
  },

  getStatistics: async (): Promise<ModelStats> => {
    const response = await api.get<ModelStats>('/statistics')
    return response.data
  },

  predict: async (
    lottery: string,
    numbers: number[],
    drawId: number | null = null
  ): Promise<PredictionResponse> => {
    const response = await api.post<PredictionResponse>('/predict', {
      lottery,
      numbers,
      draw_id: drawId,
    })
    return response.data
  },

  explainNumber: async (
    number: number,
    lottery: string = 'MAHAJANA_SAMPATHA'
  ): Promise<ExplanationResponse> => {
    const response = await api.get<ExplanationResponse>(`/explain/${number}`, {
      params: { lottery },
    })
    return response.data
  },
}

export default apiService

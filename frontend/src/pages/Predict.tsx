import { useState, useEffect } from 'react'
import { Sparkles, Shuffle, X, TrendingUp, AlertCircle } from 'lucide-react'
import { Button } from '../components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card'
import { Badge } from '../components/ui/badge'
import apiService from '../services/api'
import type { LotteryInfo, PredictionResponse, NumberPrediction } from '../types/api'

export default function Predict() {
  const [lotteries, setLotteries] = useState<LotteryInfo[]>([])
  const [selectedLottery, setSelectedLottery] = useState('MAHAJANA_SAMPATHA')
  const [selectedNumbers, setSelectedNumbers] = useState<number[]>([])
  const [predictions, setPredictions] = useState<PredictionResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchLotteries = async () => {
      try {
        const data = await apiService.getLotteries()
        setLotteries(data)
      } catch (err) {
        console.error('Error fetching lotteries:', err)
      }
    }

    fetchLotteries()
  }, [])

  const toggleNumber = (number: number) => {
    if (selectedNumbers.includes(number)) {
      setSelectedNumbers(selectedNumbers.filter((n) => n !== number))
    } else if (selectedNumbers.length < 20) {
      setSelectedNumbers([...selectedNumbers, number].sort((a, b) => a - b))
    }
  }

  const selectQuickPick = (count: number) => {
    const numbers: number[] = []
    while (numbers.length < count) {
      const num = Math.floor(Math.random() * 80) + 1
      if (!numbers.includes(num)) {
        numbers.push(num)
      }
    }
    setSelectedNumbers(numbers.sort((a, b) => a - b))
  }

  const handlePredict = async () => {
    if (selectedNumbers.length === 0) {
      setError('Please select at least one number')
      return
    }

    setLoading(true)
    setError(null)

    try {
      const result = await apiService.predict(selectedLottery, selectedNumbers)
      setPredictions(result)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to get predictions. Make sure the backend is running.')
    } finally {
      setLoading(false)
    }
  }

  const clearSelection = () => {
    setSelectedNumbers([])
    setPredictions(null)
    setError(null)
  }

  const getConfidenceColor = (confidence: string) => {
    switch (confidence) {
      case 'High':
        return 'text-green-600 bg-green-50 border-green-200'
      case 'Medium':
        return 'text-yellow-600 bg-yellow-50 border-yellow-200'
      case 'Low':
        return 'text-red-600 bg-red-50 border-red-200'
      default:
        return 'text-gray-600 bg-gray-50 border-gray-200'
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 py-8">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 max-w-7xl">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl md:text-4xl lg:text-5xl font-bold mb-4">
            Lottery Number Predictions
          </h1>
          <p className="text-gray-600 max-w-2xl mx-auto">
            Select numbers to predict their probability of appearing in the next draw
          </p>
        </div>

        {/* Controls */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle>Selection Controls</CardTitle>
            <CardDescription>Choose a lottery and select numbers to predict</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {/* Lottery Selector */}
              <div>
                <label className="block text-sm font-medium mb-2">Select Lottery:</label>
                <select
                  value={selectedLottery}
                  onChange={(e) => setSelectedLottery(e.target.value)}
                  className="w-full md:w-auto px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  {lotteries.length > 0 ? (
                    lotteries.map((lottery) => (
                      <option key={lottery.name} value={lottery.name}>
                        {lottery.display_name} - {lottery.draw_format} ({lottery.draws_in_dataset} draws)
                      </option>
                    ))
                  ) : (
                    <option>Loading lotteries...</option>
                  )}
                </select>
                {lotteries.length > 0 && selectedLottery && (
                  <p className="text-sm text-gray-600 mt-2">
                    <strong>Draw Format:</strong> {lotteries.find(l => l.name === selectedLottery)?.draw_format}
                  </p>
                )}
              </div>

              {/* Quick Pick Buttons */}
              <div>
                <label className="block text-sm font-medium mb-2">Quick Actions:</label>
                <div className="flex flex-wrap gap-2">
                  <Button onClick={() => selectQuickPick(5)} size="sm" variant="outline">
                    <Shuffle className="mr-2 h-4 w-4" />
                    Quick Pick (5)
                  </Button>
                  <Button onClick={() => selectQuickPick(10)} size="sm" variant="outline">
                    <Shuffle className="mr-2 h-4 w-4" />
                    Quick Pick (10)
                  </Button>
                  <Button onClick={() => selectQuickPick(20)} size="sm" variant="outline">
                    <Shuffle className="mr-2 h-4 w-4" />
                    Quick Pick (20)
                  </Button>
                  <Button onClick={clearSelection} size="sm" variant="secondary">
                    <X className="mr-2 h-4 w-4" />
                    Clear All
                  </Button>
                </div>
              </div>

              {/* Selection Info */}
              <div className="flex items-center justify-between flex-wrap gap-2">
                <Badge variant={selectedNumbers.length > 0 ? 'default' : 'secondary'}>
                  Selected: {selectedNumbers.length} / 20 numbers
                </Badge>
                {selectedNumbers.length > 0 && (
                  <div className="flex flex-wrap gap-1">
                    {selectedNumbers.map((num) => (
                      <span
                        key={num}
                        className="inline-flex items-center gap-1 px-2 py-1 bg-blue-100 text-blue-700 rounded text-sm font-medium"
                      >
                        {num}
                        <button
                          onClick={() => toggleNumber(num)}
                          className="hover:text-blue-900"
                        >
                          <X className="h-3 w-3" />
                        </button>
                      </span>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Number Grid */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle>Select Numbers (1-80)</CardTitle>
            <CardDescription>Click numbers to select/deselect (max 20)</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-8 sm:grid-cols-10 md:grid-cols-16 lg:grid-cols-20 gap-1 sm:gap-2">
              {Array.from({ length: 80 }, (_, i) => i + 1).map((number) => {
                const isSelected = selectedNumbers.includes(number)
                return (
                  <button
                    key={number}
                    onClick={() => toggleNumber(number)}
                    disabled={!isSelected && selectedNumbers.length >= 20}
                    className={`
                      aspect-square flex items-center justify-center rounded-md text-sm font-semibold
                      transition-all duration-200 hover:scale-110
                      ${
                        isSelected
                          ? 'bg-blue-600 text-white shadow-md'
                          : 'bg-white border border-gray-300 text-gray-700 hover:bg-gray-50'
                      }
                      ${!isSelected && selectedNumbers.length >= 20 ? 'opacity-30 cursor-not-allowed' : 'cursor-pointer'}
                    `}
                  >
                    {number}
                  </button>
                )
              })}
            </div>
          </CardContent>
        </Card>

        {/* Predict Button */}
        <div className="text-center mb-6">
          <Button
            onClick={handlePredict}
            disabled={selectedNumbers.length === 0 || loading}
            size="lg"
            className="px-8"
          >
            {loading ? (
              <>
                <div className="mr-2 h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
                Predicting...
              </>
            ) : (
              <>
                <Sparkles className="mr-2 h-5 w-5" />
                Get Predictions
              </>
            )}
          </Button>
        </div>

        {/* Error Message */}
        {error && (
          <Card className="mb-6 border-red-200 bg-red-50">
            <CardContent className="pt-6">
              <div className="flex items-start gap-3">
                <AlertCircle className="h-5 w-5 text-red-600 mt-0.5" />
                <div>
                  <p className="font-semibold text-red-900">Error</p>
                  <p className="text-sm text-red-700">{error}</p>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Results */}
        {predictions && (
          <div className="space-y-6">
            {/* Top 5 Numbers */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <TrendingUp className="h-5 w-5 text-green-600" />
                  Top 5 Recommended Numbers
                </CardTitle>
                <CardDescription>
                  Highest probability numbers from your selection
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 sm:grid-cols-3 lg:grid-cols-5 gap-4">
                  {predictions.top_5_numbers.map((num, idx) => {
                    const pred = predictions.predictions.find((p) => p.number === num)
                    return pred ? (
                      <div
                        key={num}
                        className="text-center p-4 bg-gradient-to-br from-blue-50 to-purple-50 rounded-lg border-2 border-blue-200"
                      >
                        <div className="text-xs text-gray-600 mb-1">#{idx + 1}</div>
                        <div className="text-3xl font-bold text-blue-600 mb-2">{num}</div>
                        <div className="text-lg font-semibold text-gray-700 mb-1">
                          {(pred.probability * 100).toFixed(2)}%
                        </div>
                        <Badge className={getConfidenceColor(pred.confidence)}>
                          {pred.confidence}
                        </Badge>
                      </div>
                    ) : null
                  })}
                </div>
              </CardContent>
            </Card>

            {/* All Predictions Table */}
            <Card>
              <CardHeader>
                <CardTitle>All Predictions</CardTitle>
                <CardDescription>
                  Detailed probability breakdown for all selected numbers
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead>
                      <tr className="border-b">
                        <th className="text-left py-3 px-4 font-semibold">Rank</th>
                        <th className="text-left py-3 px-4 font-semibold">Number</th>
                        <th className="text-left py-3 px-4 font-semibold">Probability</th>
                        <th className="text-left py-3 px-4 font-semibold">Prediction</th>
                        <th className="text-left py-3 px-4 font-semibold">Confidence</th>
                      </tr>
                    </thead>
                    <tbody>
                      {[...predictions.predictions]
                        .sort((a, b) => b.probability - a.probability)
                        .map((pred, idx) => (
                          <tr key={pred.number} className="border-b hover:bg-gray-50">
                            <td className="py-3 px-4 text-gray-600">{idx + 1}</td>
                            <td className="py-3 px-4">
                              <span className="inline-flex items-center justify-center w-10 h-10 bg-blue-600 text-white rounded-md font-bold">
                                {pred.number}
                              </span>
                            </td>
                            <td className="py-3 px-4">
                              <div className="flex items-center gap-2">
                                <div className="flex-grow bg-gray-200 rounded-full h-2 w-24">
                                  <div
                                    className="bg-blue-600 h-2 rounded-full"
                                    style={{ width: `${pred.probability * 100}%` }}
                                  />
                                </div>
                                <span className="font-semibold text-sm">
                                  {(pred.probability * 100).toFixed(2)}%
                                </span>
                              </div>
                            </td>
                            <td className="py-3 px-4">
                              <Badge
                                variant={pred.prediction === 'Appear' ? 'default' : 'secondary'}
                              >
                                {pred.prediction}
                              </Badge>
                            </td>
                            <td className="py-3 px-4">
                              <Badge className={getConfidenceColor(pred.confidence)}>
                                {pred.confidence}
                              </Badge>
                            </td>
                          </tr>
                        ))}
                    </tbody>
                  </table>
                </div>
              </CardContent>
            </Card>

            {/* Note */}
            <Card className="bg-yellow-50 border-yellow-200">
              <CardContent className="pt-6">
                <p className="text-sm text-gray-700">
                  <strong>Note:</strong> Predictions are based on historical patterns and statistical
                  analysis using CatBoost ML. Lottery outcomes are inherently random. Use for
                  educational purposes only.
                </p>
              </CardContent>
            </Card>
          </div>
        )}
      </div>
    </div>
  )
}

import { useState } from 'react'
import { Brain, TrendingUp, TrendingDown, AlertCircle, BarChart3, Users, Network } from 'lucide-react'
import { Button } from '../components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card'
import { Badge } from '../components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs'
import apiService from '../services/api'
import type { ExplanationResponse } from '../types/api'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, Cell, ResponsiveContainer } from 'recharts'

export default function Explain() {
  const [number, setNumber] = useState('')
  const [explanation, setExplanation] = useState<ExplanationResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleExplain = async () => {
    const num = parseInt(number)
    if (isNaN(num) || num < 0 || num > 80) {
      setError('Please enter a valid number between 0 and 80')
      return
    }

    setLoading(true)
    setError(null)

    try {
      const result = await apiService.explainNumber(num)
      setExplanation(result)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to get explanation. Make sure the backend is running.')
    } finally {
      setLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleExplain()
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50 py-8">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 max-w-6xl">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center gap-2 mb-4">
            <Brain className="h-8 w-8 text-purple-600" />
            <h1 className="text-3xl md:text-4xl lg:text-5xl font-bold">
              SHAP Explainability
            </h1>
          </div>
          <p className="text-gray-600 max-w-2xl mx-auto">
            Understand which features influence the prediction for a specific lottery number
          </p>
        </div>

        {/* Input Section */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle>Explain a Number</CardTitle>
            <CardDescription>
              Enter any number between 0-80 to see which features drive its prediction
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex flex-col sm:flex-row gap-4">
              <div className="flex-grow">
                <input
                  type="number"
                  min="0"
                  max="80"
                  value={number}
                  onChange={(e) => setNumber(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Enter number (e.g., 0, 7, 42)"
                  className="w-full px-4 py-3 text-lg border rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>
              <Button
                onClick={handleExplain}
                disabled={loading}
                size="lg"
                className="bg-purple-600 hover:bg-purple-700"
              >
                {loading ? (
                  <>
                    <div className="mr-2 h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
                    Analyzing...
                  </>
                ) : (
                  <>
                    <Brain className="mr-2 h-5 w-5" />
                    Explain
                  </>
                )}
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Error Message */}
        {error && (
          <Card className="mb-8 border-red-200 bg-red-50">
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
        {explanation && (
          <div className="space-y-6">
            {/* Prediction Summary */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-between flex-wrap gap-4">
                  <span className="text-xl">Number {explanation.number}</span>
                  <div className="flex flex-col sm:flex-row items-end sm:items-center gap-3">
                    <div className="flex items-baseline gap-2">
                      <span className="text-sm font-medium text-gray-600">Probability:</span>
                      <span className="text-3xl font-bold text-purple-600">
                        {(explanation.probability * 100).toFixed(2)}%
                      </span>
                    </div>
                    <Badge
                      variant={explanation.probability > 0.5 ? 'default' : 'secondary'}
                      className="text-base px-4 py-2"
                    >
                      {explanation.probability > 0.5 ? 'Likely to Appear' : 'Unlikely to Appear'}
                    </Badge>
                  </div>
                </CardTitle>
              </CardHeader>
            </Card>

            {/* Tabbed Explainability Analysis */}
            <Tabs defaultValue="single" className="w-full">
              <TabsList className="grid w-full grid-cols-4">
                <TabsTrigger value="single">Single Number</TabsTrigger>
                <TabsTrigger value="global">Global SHAP</TabsTrigger>
                <TabsTrigger value="lime">LIME Analysis</TabsTrigger>
                <TabsTrigger value="dependencies">Dependencies</TabsTrigger>
              </TabsList>

              {/* Tab 1: Single Number SHAP */}
              <TabsContent value="single" className="space-y-6">
                {/* SHAP Chart */}
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <TrendingUp className="h-5 w-5 text-green-600" />
                      Top 5 Feature Contributions (SHAP Values)
                    </CardTitle>
                    <CardDescription>
                      Features pushing the prediction toward "Appear" (positive) or "Not Appear" (negative)
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <ResponsiveContainer width="100%" height={400}>
                      <BarChart
                        data={explanation.top_5_features}
                        layout="vertical"
                        margin={{ top: 5, right: 30, left: 100, bottom: 5 }}
                      >
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis type="number" />
                        <YAxis dataKey="feature" type="category" width={90} />
                        <Tooltip
                          formatter={(value: number) => [value.toFixed(4), 'SHAP Value']}
                          contentStyle={{ backgroundColor: 'white', border: '1px solid #ccc', borderRadius: '4px' }}
                        />
                        <Legend />
                        <Bar dataKey="contribution" name="SHAP Contribution">
                          {explanation.top_5_features.map((entry, index) => (
                            <Cell
                              key={`cell-${index}`}
                              fill={entry.contribution > 0 ? '#10b981' : '#ef4444'}
                            />
                          ))}
                        </Bar>
                      </BarChart>
                    </ResponsiveContainer>
                  </CardContent>
                </Card>

                {/* Feature Interpretation Table */}
                <Card>
                  <CardHeader>
                    <CardTitle>Feature Interpretation</CardTitle>
                    <CardDescription>
                      How each feature influences the prediction
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="overflow-x-auto">
                      <table className="w-full">
                        <thead>
                          <tr className="border-b">
                            <th className="text-left py-3 px-4 font-semibold">Rank</th>
                            <th className="text-left py-3 px-4 font-semibold">Feature</th>
                            <th className="text-left py-3 px-4 font-semibold">SHAP Value</th>
                            <th className="text-left py-3 px-4 font-semibold">Impact</th>
                          </tr>
                        </thead>
                        <tbody>
                          {explanation.top_5_features.map((feature, idx) => (
                            <tr key={idx} className="border-b hover:bg-gray-50">
                              <td className="py-3 px-4">
                                <div className="flex items-center justify-center w-8 h-8 bg-purple-100 text-purple-700 rounded-full font-bold text-sm">
                                  {idx + 1}
                                </div>
                              </td>
                              <td className="py-3 px-4">
                                <code className="text-sm font-mono bg-gray-100 px-2 py-1 rounded">
                                  {feature.feature}
                                </code>
                              </td>
                              <td className="py-3 px-4">
                                <span className={`font-semibold ${feature.contribution > 0 ? 'text-green-600' : 'text-red-600'}`}>
                                  {feature.contribution > 0 ? '+' : ''}{feature.contribution.toFixed(4)}
                                </span>
                              </td>
                              <td className="py-3 px-4">
                                <div className="flex items-center gap-2">
                                  {feature.contribution > 0 ? (
                                    <>
                                      <TrendingUp className="h-4 w-4 text-green-600" />
                                      <span className="text-sm text-green-700">Increases probability</span>
                                    </>
                                  ) : (
                                    <>
                                      <TrendingDown className="h-4 w-4 text-red-600" />
                                      <span className="text-sm text-red-700">Decreases probability</span>
                                    </>
                                  )}
                                </div>
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </CardContent>
                </Card>

                {/* Understanding SHAP */}
                <Card className="bg-blue-50 border-blue-200">
                  <CardHeader>
                    <CardTitle className="text-lg">Understanding SHAP Values</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-2 text-sm">
                    <div className="flex items-start gap-2">
                      <span className="text-green-600 font-bold">•</span>
                      <p>
                        <strong className="text-green-700">Positive values (green):</strong> Feature increases the probability that the number will appear
                      </p>
                    </div>
                    <div className="flex items-start gap-2">
                      <span className="text-red-600 font-bold">•</span>
                      <p>
                        <strong className="text-red-700">Negative values (red):</strong> Feature decreases the probability that the number will appear
                      </p>
                    </div>
                    <div className="flex items-start gap-2">
                      <span className="text-purple-600 font-bold">•</span>
                      <p>
                        <strong className="text-purple-700">Magnitude:</strong> Larger absolute value = stronger influence on the prediction
                      </p>
                    </div>
                    <div className="flex items-start gap-2">
                      <span className="text-blue-600 font-bold">•</span>
                      <p>
                        <strong className="text-blue-700">SHAP:</strong> SHapley Additive exPlanations uses game theory to fairly distribute credit to each feature
                      </p>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              {/* Tab 2: Global SHAP Analysis */}
              <TabsContent value="global" className="space-y-6">
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <BarChart3 className="h-5 w-5 text-purple-600" />
                      Global SHAP Analysis
                    </CardTitle>
                    <CardDescription>
                      Overall feature importance across 10,000 samples from the dataset
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-6">
                    <div>
                      <h4 className="font-semibold mb-2">SHAP Summary Plot</h4>
                      <p className="text-sm text-gray-600 mb-3">
                        Shows the distribution of SHAP values for each feature. Each dot represents a sample, colored by feature value (red = high, blue = low).
                      </p>
                      <img
                        src="/outputs/explainability/shap/shap_summary_plot.png"
                        alt="SHAP Summary Plot"
                        className="w-full rounded-lg border shadow-sm"
                      />
                    </div>

                    <div>
                      <h4 className="font-semibold mb-2">SHAP Bar Plot</h4>
                      <p className="text-sm text-gray-600 mb-3">
                        Mean absolute SHAP values showing the average impact of each feature across all predictions.
                      </p>
                      <img
                        src="/outputs/explainability/shap/shap_bar_plot.png"
                        alt="SHAP Bar Plot"
                        className="w-full rounded-lg border shadow-sm"
                      />
                    </div>

                    <div>
                      <h4 className="font-semibold mb-2">Feature Importance Comparison</h4>
                      <p className="text-sm text-gray-600 mb-3">
                        Compares SHAP importance with built-in CatBoost feature importance to validate consistency.
                      </p>
                      <img
                        src="/outputs/explainability/shap/importance_comparison_plot.png"
                        alt="Importance Comparison"
                        className="w-full rounded-lg border shadow-sm"
                      />
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              {/* Tab 3: LIME Analysis */}
              <TabsContent value="lime" className="space-y-6">
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Users className="h-5 w-5 text-orange-600" />
                      LIME Analysis
                    </CardTitle>
                    <CardDescription>
                      Local Interpretable Model-agnostic Explanations (LIME) for individual predictions
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-6">
                    <div>
                      <h4 className="font-semibold mb-2">LIME vs SHAP Comparison</h4>
                      <p className="text-sm text-gray-600 mb-3">
                        Comparison showing 85%+ agreement between LIME and SHAP feature rankings, validating explanation consistency.
                      </p>
                      <img
                        src="/outputs/explainability/lime/lime_shap_comparison.png"
                        alt="LIME SHAP Comparison"
                        className="w-full rounded-lg border shadow-sm"
                      />
                    </div>

                    <div>
                      <h4 className="font-semibold mb-2">Positive Prediction Examples</h4>
                      <p className="text-sm text-gray-600 mb-3">
                        LIME explanations for numbers predicted to appear (probability &gt; 50%)
                      </p>
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <img
                          src="/outputs/explainability/lime/lime_positive_1.png"
                          alt="LIME Positive Example 1"
                          className="w-full rounded-lg border shadow-sm"
                        />
                        <img
                          src="/outputs/explainability/lime/lime_positive_2.png"
                          alt="LIME Positive Example 2"
                          className="w-full rounded-lg border shadow-sm"
                        />
                        <img
                          src="/outputs/explainability/lime/lime_positive_3.png"
                          alt="LIME Positive Example 3"
                          className="w-full rounded-lg border shadow-sm"
                        />
                      </div>
                    </div>

                    <div>
                      <h4 className="font-semibold mb-2">Negative Prediction Examples</h4>
                      <p className="text-sm text-gray-600 mb-3">
                        LIME explanations for numbers predicted not to appear (probability &lt; 50%)
                      </p>
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <img
                          src="/outputs/explainability/lime/lime_negative_1.png"
                          alt="LIME Negative Example 1"
                          className="w-full rounded-lg border shadow-sm"
                        />
                        <img
                          src="/outputs/explainability/lime/lime_negative_2.png"
                          alt="LIME Negative Example 2"
                          className="w-full rounded-lg border shadow-sm"
                        />
                        <img
                          src="/outputs/explainability/lime/lime_negative_3.png"
                          alt="LIME Negative Example 3"
                          className="w-full rounded-lg border shadow-sm"
                        />
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              {/* Tab 4: Feature Dependencies */}
              <TabsContent value="dependencies" className="space-y-6">
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Network className="h-5 w-5 text-blue-600" />
                      Feature Dependencies
                    </CardTitle>
                    <CardDescription>
                      SHAP dependence plots showing how feature values affect predictions and their interactions
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div>
                      <p className="text-sm text-gray-600 mb-3">
                        Each plot shows how a single feature's value affects SHAP values (prediction contribution), colored by another feature to reveal interactions.
                      </p>
                      <img
                        src="/outputs/explainability/shap/shap_dependence_plots.png"
                        alt="SHAP Dependence Plots"
                        className="w-full rounded-lg border shadow-sm"
                      />
                    </div>

                    <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                      <h4 className="font-semibold mb-2 text-blue-900">Key Insights from Dependencies</h4>
                      <ul className="space-y-2 text-sm text-blue-800">
                        <li className="flex items-start gap-2">
                          <span>•</span>
                          <span><strong>appearance_rate:</strong> Higher rates strongly increase prediction probability (linear relationship)</span>
                        </li>
                        <li className="flex items-start gap-2">
                          <span>•</span>
                          <span><strong>days_since_last:</strong> Optimal range exists (not too recent, not too old)</span>
                        </li>
                        <li className="flex items-start gap-2">
                          <span>•</span>
                          <span><strong>temperature_score:</strong> Hot numbers have higher SHAP values, cold numbers lower</span>
                        </li>
                        <li className="flex items-start gap-2">
                          <span>•</span>
                          <span><strong>Interactions:</strong> Feature effects can vary depending on other feature values (shown by color gradients)</span>
                        </li>
                      </ul>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>
            </Tabs>
          </div>
        )}

        {/* Info Section */}
        {!explanation && (
          <Card>
            <CardHeader>
              <CardTitle>About SHAP Explainability</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <p className="text-gray-700">
                SHAP (SHapley Additive exPlanations) is a game-theoretic approach to explain
                machine learning predictions. It calculates the contribution of each feature
                to the final prediction.
              </p>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="p-4 bg-gray-50 rounded-lg">
                  <h4 className="font-semibold mb-2">Our Analysis</h4>
                  <p className="text-sm text-gray-600">
                    SHAP analysis on 10,000 samples revealed the most influential features
                  </p>
                </div>
                <div className="p-4 bg-gray-50 rounded-lg">
                  <h4 className="font-semibold mb-2">Top Features</h4>
                  <p className="text-sm text-gray-600">
                    appearance_rate, days_since_last, draw_sequence dominate predictions
                  </p>
                </div>
                <div className="p-4 bg-gray-50 rounded-lg">
                  <h4 className="font-semibold mb-2">Cross-Validation</h4>
                  <p className="text-sm text-gray-600">
                    LIME analysis confirms 85%+ agreement with SHAP findings
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  )
}

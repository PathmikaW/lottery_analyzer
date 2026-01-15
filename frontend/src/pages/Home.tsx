import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { Sparkles, TrendingUp, Brain, BarChart3, AlertCircle } from 'lucide-react'
import { Button } from '../components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card'
import { Badge } from '../components/ui/badge'
import apiService from '../services/api'
import type { ModelStats } from '../types/api'

export default function Home() {
  const [stats, setStats] = useState<ModelStats | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const data = await apiService.getStatistics()
        setStats(data)
      } catch (err) {
        setError('Failed to load statistics. Make sure the backend is running.')
        console.error('Error:', err)
      } finally {
        setLoading(false)
      }
    }

    fetchStats()
  }, [])

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-br from-blue-600 via-purple-600 to-pink-600 text-white">
        <div className="absolute inset-0 bg-black/10"></div>
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-16 md:py-24 relative z-10">
          <div className="max-w-4xl mx-auto text-center">
            <Badge className="mb-4 bg-white/20 text-white border-white/30">
              MSc AI - Applied Machine Learning Assignment
            </Badge>
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold mb-6 leading-tight">
              Sri Lankan Lottery ML Analyzer
            </h1>
            <p className="text-lg md:text-xl mb-8 text-blue-100">
              Machine learning predictions with explainability (SHAP + LIME) for educational purposes
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button asChild size="lg" className="bg-white text-blue-600 hover:bg-blue-50">
                <Link to="/predict">
                  <Sparkles className="mr-2 h-5 w-5" />
                  Try Predictions
                </Link>
              </Button>
              <Button asChild size="lg" variant="outline" className="border-white text-white hover:bg-white/10">
                <Link to="/explain">
                  <Brain className="mr-2 h-5 w-5" />
                  View Explainability
                </Link>
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-12 md:py-16 bg-white">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          {loading ? (
            <div className="text-center py-12">
              <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
              <p className="mt-4 text-gray-600">Loading model statistics...</p>
            </div>
          ) : error ? (
            <Card className="border-red-200 bg-red-50">
              <CardContent className="pt-6">
                <div className="flex items-start gap-3">
                  <AlertCircle className="h-5 w-5 text-red-600 mt-0.5" />
                  <div>
                    <p className="font-semibold text-red-900">Backend Connection Error</p>
                    <p className="text-sm text-red-700 mt-1">{error}</p>
                    <p className="text-sm text-red-600 mt-2">Make sure the backend is running at http://localhost:8000</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          ) : stats ? (
            <>
              <div className="text-center mb-12">
                <h2 className="text-3xl md:text-4xl font-bold mb-4">Model Performance</h2>
                <p className="text-gray-600 max-w-2xl mx-auto">
                  Trained on 485,094 samples across 17 Sri Lankan lotteries
                </p>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                <Card className="hover:shadow-lg transition-shadow">
                  <CardHeader className="pb-3">
                    <CardDescription>Model Type</CardDescription>
                    <CardTitle className="text-2xl">{stats.model_type}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-gray-600">Gradient boosting classifier</p>
                  </CardContent>
                </Card>

                <Card className="hover:shadow-lg transition-shadow">
                  <CardHeader className="pb-3">
                    <CardDescription>F1-Score</CardDescription>
                    <CardTitle className="text-2xl text-blue-600">
                      {(stats.f1_score * 100).toFixed(2)}%
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <Badge variant="secondary">3.87x better than random</Badge>
                  </CardContent>
                </Card>

                <Card className="hover:shadow-lg transition-shadow">
                  <CardHeader className="pb-3">
                    <CardDescription>Training Samples</CardDescription>
                    <CardTitle className="text-2xl">
                      {stats.training_samples.toLocaleString()}
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-gray-600">485K lottery outcomes</p>
                  </CardContent>
                </Card>

                <Card className="hover:shadow-lg transition-shadow">
                  <CardHeader className="pb-3">
                    <CardDescription>Features</CardDescription>
                    <CardTitle className="text-2xl">{stats.features_count}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-gray-600">Engineered features</p>
                  </CardContent>
                </Card>
              </div>
            </>
          ) : null}
        </div>
      </section>

      {/* Features Section */}
      <section className="py-12 md:py-16 bg-gray-50">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">Key Features</h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
              Advanced machine learning with explainability for educational research
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <Card className="text-center hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="mx-auto w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mb-4">
                  <Brain className="h-6 w-6 text-blue-600" />
                </div>
                <CardTitle className="text-xl">CatBoost ML</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-gray-600">
                  Gradient boosting algorithm optimized for tabular data with categorical features
                </p>
              </CardContent>
            </Card>

            <Card className="text-center hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="mx-auto w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mb-4">
                  <BarChart3 className="h-6 w-6 text-purple-600" />
                </div>
                <CardTitle className="text-xl">SHAP Explainability</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-gray-600">
                  Understand which features influence predictions with game-theoretic approach
                </p>
              </CardContent>
            </Card>

            <Card className="text-center hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="mx-auto w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mb-4">
                  <TrendingUp className="h-6 w-6 text-green-600" />
                </div>
                <CardTitle className="text-xl">17 Lotteries</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-gray-600">
                  8,085 draws analyzed from 2021-2026 across NLB and DLB lotteries
                </p>
              </CardContent>
            </Card>

            <Card className="text-center hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="mx-auto w-12 h-12 bg-pink-100 rounded-full flex items-center justify-center mb-4">
                  <Sparkles className="h-6 w-6 text-pink-600" />
                </div>
                <CardTitle className="text-xl">Real-time API</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-gray-600">
                  Instant probability calculations via FastAPI with TypeScript frontend
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Top Features Section */}
      {stats && stats.top_5_features.length > 0 && (
        <section className="py-12 md:py-16 bg-white">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8 max-w-4xl">
            <Card>
              <CardHeader className="text-center">
                <CardTitle className="text-2xl md:text-3xl">Most Influential Features</CardTitle>
                <CardDescription>
                  SHAP analysis reveals the top predictive factors
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ol className="space-y-3">
                  {stats.top_5_features.map((feature, idx) => (
                    <li key={idx} className="flex items-center gap-4 p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                      <div className="flex-shrink-0 w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center font-bold">
                        {idx + 1}
                      </div>
                      <div className="flex-grow">
                        <code className="text-sm font-mono bg-white px-2 py-1 rounded border">
                          {feature}
                        </code>
                      </div>
                    </li>
                  ))}
                </ol>
                <div className="mt-6 text-center">
                  <Button asChild variant="outline">
                    <Link to="/explain">
                      View Full Explainability Analysis →
                    </Link>
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        </section>
      )}

      {/* Disclaimer Section */}
      <section className="py-12 md:py-16 bg-yellow-50 border-t border-yellow-200">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 max-w-4xl">
          <Card className="border-yellow-300 bg-white">
            <CardHeader>
              <div className="flex items-center gap-2">
                <AlertCircle className="h-5 w-5 text-yellow-600" />
                <CardTitle className="text-xl">⚠️ Important Disclaimer</CardTitle>
              </div>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-gray-700">
                <li className="flex items-start gap-2">
                  <span className="text-yellow-600 font-bold">•</span>
                  <span>This is an educational machine learning project for MSc AI coursework</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-yellow-600 font-bold">•</span>
                  <span>NOT intended for commercial gambling or betting purposes</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-yellow-600 font-bold">•</span>
                  <span>Lottery outcomes are inherently random - no system can predict them perfectly</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-yellow-600 font-bold">•</span>
                  <span>Model F1-Score of 25.92% reflects the fundamental randomness ceiling</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-yellow-600 font-bold">•</span>
                  <span>Use responsibly for learning and research purposes only</span>
                </li>
              </ul>
            </CardContent>
          </Card>
        </div>
      </section>
    </div>
  )
}

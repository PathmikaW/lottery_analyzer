import { Book, Code, Database, Zap, Shield, AlertTriangle } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card'
import { Badge } from '../components/ui/badge'

export default function About() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-blue-50 py-8">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 max-w-6xl">
        {/* Header */}
        <div className="text-center mb-12">
          <Badge className="mb-4">MSc AI - Applied Machine Learning Assignment</Badge>
          <h1 className="text-3xl md:text-4xl lg:text-5xl font-bold mb-4">
            About This Project
          </h1>
          <p className="text-gray-600 max-w-2xl mx-auto">
            An educational machine learning system demonstrating gradient boosting with explainability
          </p>
        </div>

        {/* Project Overview */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Book className="h-5 w-5" />
              Project Overview
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <p className="text-gray-700">
              This project demonstrates the application of CatBoost (gradient boosting) with SHAP and LIME
              explainability for analyzing Sri Lankan lottery draw patterns. It showcases advanced ML
              techniques on a real-world dataset while maintaining ethical considerations.
            </p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="p-4 bg-blue-50 rounded-lg">
                <h4 className="font-semibold mb-2">Purpose</h4>
                <p className="text-sm text-gray-700">
                  Educational demonstration of ML and explainability techniques for academic coursework
                </p>
              </div>
              <div className="p-4 bg-purple-50 rounded-lg">
                <h4 className="font-semibold mb-2">Date</h4>
                <p className="text-sm text-gray-700">January 2026</p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Dataset */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Database className="h-5 w-5" />
              Dataset
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
              <div className="text-center p-4 bg-gray-50 rounded-lg">
                <div className="text-2xl font-bold text-blue-600 mb-1">17</div>
                <div className="text-sm text-gray-600">Lotteries</div>
              </div>
              <div className="text-center p-4 bg-gray-50 rounded-lg">
                <div className="text-2xl font-bold text-purple-600 mb-1">8,085</div>
                <div className="text-sm text-gray-600">Draws</div>
              </div>
              <div className="text-center p-4 bg-gray-50 rounded-lg">
                <div className="text-2xl font-bold text-green-600 mb-1">485K</div>
                <div className="text-sm text-gray-600">Samples</div>
              </div>
              <div className="text-center p-4 bg-gray-50 rounded-lg">
                <div className="text-2xl font-bold text-pink-600 mb-1">20</div>
                <div className="text-sm text-gray-600">Features</div>
              </div>
            </div>
            <p className="text-sm text-gray-700">
              <strong>Date Range:</strong> 2021-04-01 to 2026-01-12 (58.2 months)<br />
              <strong>Sources:</strong> National Lotteries Board (NLB) and Development Lotteries Board (DLB)<br />
              <strong>Number Ranges:</strong> Each lottery preserves its original number range (0-9 for some NLB, 1-80 for others)
            </p>
          </CardContent>
        </Card>

        {/* ML Approach */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle>Machine Learning Approach</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <h4 className="font-semibold mb-2">Algorithm: CatBoost Classifier</h4>
              <p className="text-sm text-gray-700 mb-2">
                Gradient boosting algorithm optimized for categorical features and tabular data
              </p>
              <ul className="space-y-1 text-sm text-gray-700">
                <li className="flex items-start gap-2">
                  <span className="text-blue-600">•</span>
                  Not taught in lectures (assignment requirement ✓)
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-blue-600">•</span>
                  Handles categorical features natively
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-blue-600">•</span>
                  Fast training with GPU support
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-blue-600">•</span>
                  Built-in overfitting protection
                </li>
              </ul>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="p-4 bg-green-50 rounded-lg border border-green-200">
                <h4 className="font-semibold text-green-900 mb-1">F1-Score</h4>
                <div className="text-2xl font-bold text-green-600">25.92%</div>
                <p className="text-xs text-green-700 mt-1">3.87x better than random</p>
              </div>
              <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
                <h4 className="font-semibold text-blue-900 mb-1">Precision</h4>
                <div className="text-2xl font-bold text-blue-600">14.95%</div>
              </div>
              <div className="p-4 bg-purple-50 rounded-lg border border-purple-200">
                <h4 className="font-semibold text-purple-900 mb-1">Recall</h4>
                <div className="text-2xl font-bold text-purple-600">100.00%</div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Feature Engineering */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle>Feature Engineering (20 Features)</CardTitle>
            <CardDescription>Across 4 categories</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="p-4 bg-gray-50 rounded-lg">
                <h4 className="font-semibold mb-2">1. Frequency Features (5)</h4>
                <ul className="text-sm text-gray-700 space-y-1">
                  <li>• frequency_last_10, frequency_last_30, frequency_last_50</li>
                  <li>• frequency_all_time, appearance_rate</li>
                </ul>
              </div>
              <div className="p-4 bg-gray-50 rounded-lg">
                <h4 className="font-semibold mb-2">2. Temporal Features (7)</h4>
                <ul className="text-sm text-gray-700 space-y-1">
                  <li>• draw_id, draw_sequence, days_since_last</li>
                  <li>• day_of_week, month, week_of_year, is_weekend</li>
                </ul>
              </div>
              <div className="p-4 bg-gray-50 rounded-lg">
                <h4 className="font-semibold mb-2">3. Statistical Features (5)</h4>
                <ul className="text-sm text-gray-700 space-y-1">
                  <li>• current_gap, mean_gap, std_gap</li>
                  <li>• min_gap, max_gap</li>
                </ul>
              </div>
              <div className="p-4 bg-gray-50 rounded-lg">
                <h4 className="font-semibold mb-2">4. Hot/Cold Features (3)</h4>
                <ul className="text-sm text-gray-700 space-y-1">
                  <li>• temperature_score</li>
                  <li>• is_hot, is_cold</li>
                </ul>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Explainability */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle>Explainability Analysis</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h4 className="font-semibold mb-2">SHAP (Global Importance)</h4>
                <ul className="text-sm text-gray-700 space-y-1">
                  <li className="flex items-start gap-2">
                    <span className="text-green-600">✓</span>
                    TreeExplainer for exact CatBoost analysis
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-green-600">✓</span>
                    10,000 sample analysis
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-green-600">✓</span>
                    Top features: appearance_rate, days_since_last, draw_sequence
                  </li>
                </ul>
              </div>
              <div>
                <h4 className="font-semibold mb-2">LIME (Local Explanations)</h4>
                <ul className="text-sm text-gray-700 space-y-1">
                  <li className="flex items-start gap-2">
                    <span className="text-green-600">✓</span>
                    Instance-level explanations
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-green-600">✓</span>
                    10 examples (5 positive, 5 negative)
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-green-600">✓</span>
                    85%+ agreement with SHAP validates findings
                  </li>
                </ul>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Key Findings */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle>Key Findings</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2 text-sm text-gray-700">
              <li className="flex items-start gap-2">
                <span className="text-blue-600 font-bold">•</span>
                <span><strong>Frequency momentum matters:</strong> Recent activity (last 10-30 draws) more predictive than historical</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-blue-600 font-bold">•</span>
                <span><strong>Temporal recency critical:</strong> Shorter time gaps increase probability</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-blue-600 font-bold">•</span>
                <span><strong>Categorical features irrelevant:</strong> is_weekend, is_cold, trend all ~0.0 importance</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-blue-600 font-bold">•</span>
                <span><strong>Model respects randomness:</strong> 25.92% F1 ceiling reflects true lottery randomness</span>
              </li>
            </ul>
          </CardContent>
        </Card>

        {/* Technology Stack */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Code className="h-5 w-5" />
              Technology Stack
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h4 className="font-semibold mb-3 flex items-center gap-2">
                  <Zap className="h-4 w-4 text-yellow-600" />
                  Backend
                </h4>
                <ul className="space-y-1 text-sm text-gray-700">
                  <li>• FastAPI (modern Python web framework)</li>
                  <li>• CatBoost 1.2.0 (gradient boosting)</li>
                  <li>• SHAP 0.44.0 (explainability)</li>
                  <li>• Python 3.8+</li>
                  <li>• Uvicorn (ASGI server)</li>
                </ul>
              </div>
              <div>
                <h4 className="font-semibold mb-3 flex items-center gap-2">
                  <Shield className="h-4 w-4 text-blue-600" />
                  Frontend
                </h4>
                <ul className="space-y-1 text-sm text-gray-700">
                  <li>• React 18 (UI library)</li>
                  <li>• TypeScript 5.3 (type safety)</li>
                  <li>• Vite 5 (build tool)</li>
                  <li>• Tailwind CSS 3.4 (styling)</li>
                  <li>• shadcn/ui (components)</li>
                  <li>• Recharts (visualizations)</li>
                </ul>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Disclaimers */}
        <Card className="border-yellow-300 bg-yellow-50">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-yellow-900">
              <AlertTriangle className="h-5 w-5" />
              ⚠️ Important Disclaimers
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <h4 className="font-semibold mb-2 text-yellow-900">Educational Purpose Only</h4>
              <ul className="space-y-1 text-sm text-yellow-800">
                <li>• This is an academic machine learning assignment for MSc AI coursework</li>
                <li>• NOT intended for commercial gambling or betting purposes</li>
                <li>• Lottery outcomes are inherently random</li>
                <li>• Historical patterns do not predict future results</li>
                <li>• No guarantee of winning - model performance reflects randomness ceiling</li>
              </ul>
            </div>

            <div>
              <h4 className="font-semibold mb-2 text-yellow-900">Ethical Considerations</h4>
              <ul className="space-y-1 text-sm text-yellow-800">
                <li>• All data is publicly available from official lottery websites</li>
                <li>• No personal or sensitive data is collected</li>
                <li>• Predictions should not encourage gambling addiction</li>
                <li>• Model limitations are thoroughly discussed in academic report</li>
              </ul>
            </div>

            <div>
              <h4 className="font-semibold mb-2 text-yellow-900">Model Limitations</h4>
              <ul className="space-y-1 text-sm text-yellow-800">
                <li>• Performance ceiling limited by fundamental randomness (~26% F1)</li>
                <li>• Cannot predict perfectly (lotteries are designed to be random)</li>
                <li>• Model extracts weak statistical patterns, not causal relationships</li>
                <li>• Should not be used for actual betting decisions</li>
              </ul>
            </div>
          </CardContent>
        </Card>

        {/* References */}
        <Card>
          <CardHeader>
            <CardTitle>References</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2 text-sm text-gray-700">
              <li>
                <strong>Data Sources:</strong>
                <ul className="ml-4 mt-1 space-y-1">
                  <li>• National Lotteries Board (NLB): <a href="https://www.nlb.lk" target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">www.nlb.lk</a></li>
                  <li>• Development Lotteries Board (DLB): <a href="https://www.dlb.lk" target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">www.dlb.lk</a></li>
                </ul>
              </li>
              <li>
                <strong>Technology Documentation:</strong>
                <ul className="ml-4 mt-1 space-y-1">
                  <li>• CatBoost: <a href="https://catboost.ai" target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">catboost.ai</a></li>
                  <li>• SHAP: <a href="https://shap.readthedocs.io" target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">shap.readthedocs.io</a></li>
                  <li>• LIME: <a href="https://github.com/marcotcr/lime" target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">github.com/marcotcr/lime</a></li>
                </ul>
              </li>
            </ul>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

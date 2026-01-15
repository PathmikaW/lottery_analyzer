import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import { Menu, X, Sparkles } from 'lucide-react'
import { useState } from 'react'
import Home from './pages/Home'
import Predict from './pages/Predict'
import Explain from './pages/Explain'
import About from './pages/About'
import { Button } from './components/ui/button'

function App() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  return (
    <Router>
      <div className="min-h-screen flex flex-col bg-gradient-to-br from-blue-50 via-white to-purple-50">
        {/* Responsive Navbar */}
        <nav className="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b shadow-sm">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center h-16">
              {/* Logo */}
              <Link to="/" className="flex items-center space-x-2 group">
                <Sparkles className="h-6 w-6 text-blue-600 group-hover:text-blue-700 transition-colors" />
                <span className="text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  Lottery ML Analyzer
                </span>
              </Link>

              {/* Desktop Navigation */}
              <div className="hidden md:flex items-center space-x-1">
                <Button variant="ghost" asChild>
                  <Link to="/">Home</Link>
                </Button>
                <Button variant="ghost" asChild>
                  <Link to="/predict">Predict</Link>
                </Button>
                <Button variant="ghost" asChild>
                  <Link to="/explain">Explain</Link>
                </Button>
                <Button variant="ghost" asChild>
                  <Link to="/about">About</Link>
                </Button>
              </div>

              {/* Mobile Menu Button */}
              <button
                className="md:hidden p-2 rounded-md text-gray-700 hover:bg-gray-100"
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              >
                {mobileMenuOpen ? (
                  <X className="h-6 w-6" />
                ) : (
                  <Menu className="h-6 w-6" />
                )}
              </button>
            </div>
          </div>

          {/* Mobile Navigation */}
          {mobileMenuOpen && (
            <div className="md:hidden border-t bg-white">
              <div className="px-4 py-4 space-y-2">
                <Link
                  to="/"
                  className="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-md"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  Home
                </Link>
                <Link
                  to="/predict"
                  className="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-md"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  Predict
                </Link>
                <Link
                  to="/explain"
                  className="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-md"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  Explain
                </Link>
                <Link
                  to="/about"
                  className="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-md"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  About
                </Link>
              </div>
            </div>
          )}
        </nav>

        {/* Main Content */}
        <main className="flex-grow">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/predict" element={<Predict />} />
            <Route path="/explain" element={<Explain />} />
            <Route path="/about" element={<About />} />
          </Routes>
        </main>

        {/* Footer */}
        <footer className="bg-gray-900 text-white mt-auto">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div>
                <h3 className="text-lg font-semibold mb-3">About</h3>
                <p className="text-gray-400 text-sm">
                  Educational ML project for MSc AI Applied Machine Learning Assignment
                </p>
              </div>
              <div>
                <h3 className="text-lg font-semibold mb-3">Technology</h3>
                <ul className="text-gray-400 text-sm space-y-1">
                  <li>• CatBoost ML Algorithm</li>
                  <li>• SHAP + LIME Explainability</li>
                  <li>• FastAPI Backend</li>
                  <li>• React + TypeScript Frontend</li>
                </ul>
              </div>
              <div>
                <h3 className="text-lg font-semibold mb-3">Disclaimer</h3>
                <p className="text-yellow-400 text-sm">
                  ⚠️ Educational purpose only. NOT for commercial gambling.
                </p>
              </div>
            </div>
            <div className="mt-8 pt-6 border-t border-gray-800 text-center text-gray-400 text-sm">
              <p>© 2026 Lottery ML Analyzer | MSc AI Assignment</p>
            </div>
          </div>
        </footer>
      </div>
    </Router>
  )
}

export default App

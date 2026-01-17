import { useState, useEffect } from 'react'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from './ui/dialog'
import { Button } from './ui/button'
import { Download, Code, FileText, Terminal } from 'lucide-react'

interface FileViewerProps {
  isOpen: boolean
  onClose: () => void
  filePath: string
  fileName: string
}

// Jupyter notebook types
interface NotebookCell {
  cell_type: 'code' | 'markdown' | 'raw'
  source: string | string[]
  outputs?: NotebookOutput[]
  execution_count?: number | null
}

interface NotebookOutput {
  output_type: 'stream' | 'execute_result' | 'display_data' | 'error'
  text?: string | string[]
  data?: {
    'text/plain'?: string | string[]
    'text/html'?: string | string[]
    'image/png'?: string
  }
  name?: string
  ename?: string
  evalue?: string
  traceback?: string[]
}

interface Notebook {
  cells: NotebookCell[]
  metadata?: Record<string, unknown>
}

export default function FileViewer({ isOpen, onClose, filePath, fileName }: FileViewerProps) {
  const [fileContent, setFileContent] = useState<string>('')
  const [notebook, setNotebook] = useState<Notebook | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const isNotebook = filePath.endsWith('.ipynb')

  useEffect(() => {
    if (isOpen && filePath) {
      loadFile()
    }
  }, [isOpen, filePath])

  const loadFile = async () => {
    setLoading(true)
    setError(null)
    setNotebook(null)

    try {
      const response = await fetch(`http://localhost:8000/api/files/${filePath}`)
      if (!response.ok) {
        throw new Error(`Failed to load file: ${response.statusText}`)
      }
      const content = await response.text()
      setFileContent(content)

      // Parse notebook if it's a .ipynb file
      if (isNotebook) {
        try {
          const nb = JSON.parse(content) as Notebook
          setNotebook(nb)
        } catch {
          setError('Failed to parse notebook JSON')
        }
      }
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Unknown error'
      setError(`Unable to load file: ${errorMsg}`)
    } finally {
      setLoading(false)
    }
  }

  const downloadFile = () => {
    const blob = new Blob([fileContent], { type: 'application/octet-stream' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = fileName
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  // Helper to join source lines
  const getSource = (source: string | string[]): string => {
    return Array.isArray(source) ? source.join('') : source
  }

  // Helper to get output text
  const getOutputText = (output: NotebookOutput): string => {
    if (output.text) {
      return Array.isArray(output.text) ? output.text.join('') : output.text
    }
    if (output.data?.['text/plain']) {
      const plain = output.data['text/plain']
      return Array.isArray(plain) ? plain.join('') : plain
    }
    return ''
  }

  // Render markdown (simple version - renders as formatted text)
  const renderMarkdown = (source: string) => {
    // Simple markdown rendering
    const lines = source.split('\n')
    return lines.map((line, i) => {
      // Headers
      if (line.startsWith('# ')) {
        return <h1 key={i} className="text-2xl font-bold text-gray-900 mt-4 mb-2">{line.slice(2)}</h1>
      }
      if (line.startsWith('## ')) {
        return <h2 key={i} className="text-xl font-bold text-gray-800 mt-3 mb-2">{line.slice(3)}</h2>
      }
      if (line.startsWith('### ')) {
        return <h3 key={i} className="text-lg font-semibold text-gray-800 mt-2 mb-1">{line.slice(4)}</h3>
      }
      // Bold
      if (line.includes('**')) {
        const parts = line.split(/\*\*(.*?)\*\*/g)
        return (
          <p key={i} className="text-gray-700 my-1">
            {parts.map((part, j) => j % 2 === 1 ? <strong key={j}>{part}</strong> : part)}
          </p>
        )
      }
      // List items
      if (line.startsWith('- ') || line.startsWith('* ')) {
        return <li key={i} className="text-gray-700 ml-4">{line.slice(2)}</li>
      }
      // Empty line
      if (line.trim() === '') {
        return <div key={i} className="h-2" />
      }
      // Regular paragraph
      return <p key={i} className="text-gray-700 my-1">{line}</p>
    })
  }

  // Render a single notebook cell
  const renderCell = (cell: NotebookCell, index: number) => {
    const source = getSource(cell.source)

    if (cell.cell_type === 'markdown') {
      return (
        <div key={index} className="mb-4 p-4 bg-white rounded-lg border border-gray-200">
          <div className="flex items-center gap-2 text-xs text-gray-500 mb-2">
            <FileText className="h-3 w-3" />
            <span>Markdown</span>
          </div>
          <div className="prose prose-sm max-w-none">
            {renderMarkdown(source)}
          </div>
        </div>
      )
    }

    if (cell.cell_type === 'code') {
      return (
        <div key={index} className="mb-4 rounded-lg border border-gray-300 overflow-hidden">
          {/* Code input */}
          <div className="bg-gray-50 border-b border-gray-200">
            <div className="flex items-center gap-2 px-3 py-1 text-xs text-gray-500 border-b border-gray-100">
              <Code className="h-3 w-3" />
              <span>In [{cell.execution_count ?? ' '}]</span>
            </div>
            <pre className="p-3 text-sm overflow-x-auto bg-gray-900 text-gray-100">
              <code>{source}</code>
            </pre>
          </div>

          {/* Outputs */}
          {cell.outputs && cell.outputs.length > 0 && (
            <div className="bg-white">
              <div className="flex items-center gap-2 px-3 py-1 text-xs text-gray-500 border-b border-gray-100">
                <Terminal className="h-3 w-3" />
                <span>Out [{cell.execution_count ?? ' '}]</span>
              </div>
              <div className="p-3">
                {cell.outputs.map((output, oi) => renderOutput(output, oi))}
              </div>
            </div>
          )}
        </div>
      )
    }

    // Raw cell
    return (
      <div key={index} className="mb-4 p-4 bg-gray-100 rounded-lg border">
        <pre className="text-sm whitespace-pre-wrap">{source}</pre>
      </div>
    )
  }

  // Render cell output
  const renderOutput = (output: NotebookOutput, index: number) => {
    // Error output
    if (output.output_type === 'error') {
      return (
        <div key={index} className="bg-red-50 border border-red-200 rounded p-2 mb-2">
          <div className="text-red-700 font-semibold">{output.ename}: {output.evalue}</div>
          {output.traceback && (
            <pre className="text-xs text-red-600 mt-1 overflow-x-auto">
              {output.traceback.join('\n').replace(/\x1b\[[0-9;]*m/g, '')}
            </pre>
          )}
        </div>
      )
    }

    // Image output
    if (output.data?.['image/png']) {
      return (
        <div key={index} className="mb-2">
          <img
            src={`data:image/png;base64,${output.data['image/png']}`}
            alt="Output"
            className="max-w-full"
          />
        </div>
      )
    }

    // HTML output
    if (output.data?.['text/html']) {
      const html = Array.isArray(output.data['text/html'])
        ? output.data['text/html'].join('')
        : output.data['text/html']
      return (
        <div
          key={index}
          className="mb-2 overflow-x-auto notebook-html"
          dangerouslySetInnerHTML={{ __html: html }}
        />
      )
    }

    // Text output
    const text = getOutputText(output)
    if (text) {
      return (
        <pre key={index} className="text-sm text-gray-800 whitespace-pre-wrap font-mono bg-gray-50 p-2 rounded mb-2 overflow-x-auto">
          {text}
        </pre>
      )
    }

    return null
  }

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-6xl h-[85vh] overflow-hidden flex flex-col p-0 gap-0">
        <div className="p-6 pb-4 border-b flex-none">
          <DialogHeader>
            <DialogTitle className="flex items-center justify-between pr-8">
              <span>{fileName}</span>
              <div className="flex gap-2">
                <Button variant="outline" size="sm" onClick={downloadFile}>
                  <Download className="h-4 w-4 mr-2" />
                  Download
                </Button>
              </div>
            </DialogTitle>
            <DialogDescription>{filePath}</DialogDescription>
          </DialogHeader>
        </div>

        <div className="flex-1 overflow-auto min-h-0 p-6 bg-gray-100">
          {loading && (
            <div className="flex items-center justify-center h-64">
              <div className="text-gray-500">Loading file...</div>
            </div>
          )}

          {error && (
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
              <p className="text-sm text-gray-700 whitespace-pre-wrap font-mono">{error}</p>
            </div>
          )}

          {!loading && !error && isNotebook && notebook && (
            <div className="space-y-2">
              {notebook.cells.map((cell, index) => renderCell(cell, index))}
            </div>
          )}

          {!loading && !error && !isNotebook && fileContent && (
            <div className="bg-gray-900 rounded-lg p-4 text-sm overflow-x-auto">
              <pre className="font-mono text-xs leading-relaxed text-gray-100">
                <code>{fileContent}</code>
              </pre>
            </div>
          )}
        </div>
      </DialogContent>
    </Dialog>
  )
}

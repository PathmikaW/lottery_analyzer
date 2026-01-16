import { useState, useEffect } from 'react'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from './ui/dialog'
import { Button } from './ui/button'
import { ExternalLink } from 'lucide-react'

interface FileViewerProps {
  isOpen: boolean
  onClose: () => void
  filePath: string
  fileName: string
}

export default function FileViewer({ isOpen, onClose, filePath, fileName }: FileViewerProps) {
  const [fileContent, setFileContent] = useState<string>('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (isOpen && filePath) {
      loadFile()
    }
  }, [isOpen, filePath])

  const loadFile = async () => {
    setLoading(true)
    setError(null)

    try {
      // Try to fetch from backend or local path
      const response = await fetch(`/api/files/${filePath}`)
      if (!response.ok) {
        throw new Error('File not found')
      }
      const content = await response.text()
      setFileContent(content)
    } catch (err) {
      // Fallback: show path info
      setError(`Unable to load file. File path: ${filePath}`)
      setFileContent(`# File Location\n\n${filePath}\n\nTo view this file:\n1. Open VS Code\n2. Press Ctrl+P\n3. Type: ${filePath}`)
    } finally {
      setLoading(false)
    }
  }

  const openInVSCode = () => {
    // This would require a VS Code extension or protocol handler
    alert(`To open in VS Code:\n\n1. Press Ctrl+P\n2. Type: ${filePath}`)
  }

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-6xl max-h-[90vh] overflow-hidden flex flex-col">
        <DialogHeader>
          <DialogTitle className="flex items-center justify-between pr-8">
            <span>{fileName}</span>
            <div className="flex gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={openInVSCode}
              >
                <ExternalLink className="h-4 w-4 mr-2" />
                Open in VS Code
              </Button>
            </div>
          </DialogTitle>
          <DialogDescription>
            {filePath}
          </DialogDescription>
        </DialogHeader>

        <div className="flex-1 overflow-auto">
          {loading && (
            <div className="flex items-center justify-center h-64">
              <div className="text-gray-500">Loading file...</div>
            </div>
          )}

          {error && (
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
              <p className="text-sm text-gray-700 whitespace-pre-wrap">{fileContent}</p>
            </div>
          )}

          {!loading && !error && fileContent && (
            <pre className="bg-gray-50 rounded-lg p-4 text-sm overflow-x-auto">
              <code>{fileContent}</code>
            </pre>
          )}
        </div>
      </DialogContent>
    </Dialog>
  )
}

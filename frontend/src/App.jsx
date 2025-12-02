import { useState, useRef, useEffect } from 'react'
import { Search, Sparkles, Database, Zap, RefreshCw } from 'lucide-react'
import QueryInput from './components/QueryInput'
import ResultCard from './components/ResultCard'
import ExampleQueries from './components/ExampleQueries'
import Header from './components/Header'

const API_URL = import.meta.env.DEV ? '/api' : ''

function App() {
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)
  const [sessionId] = useState(() => `session_${Date.now()}`)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleQuery = async (question) => {
    setLoading(true)

    // Add user message
    setMessages(prev => [...prev, { type: 'user', content: question }])

    try {
      const response = await fetch(`${API_URL}/ask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question, session_id: sessionId })
      })

      const data = await response.json()

      if (data.success) {
        setMessages(prev => [...prev, {
          type: 'result',
          data: data
        }])
      } else {
        setMessages(prev => [...prev, {
          type: 'error',
          content: data.error || 'An error occurred'
        }])
      }
    } catch (error) {
      setMessages(prev => [...prev, {
        type: 'error',
        content: 'Failed to connect to the server. Make sure the backend is running.'
      }])
    } finally {
      setLoading(false)
    }
  }

  const handleClear = async () => {
    try {
      await fetch(`${API_URL}/clear/${sessionId}`, { method: 'POST' })
    } catch (e) {
      // Ignore
    }
    setMessages([])
  }

  return (
    <div className="min-h-screen flex flex-col">
      <div className="stars" />

      <Header onClear={handleClear} hasMessages={messages.length > 0} />

      <main className="flex-1 container mx-auto px-4 py-8 max-w-5xl">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center min-h-[60vh]">
            <div className="text-center mb-12">
              <div className="inline-flex items-center gap-2 px-4 py-2 bg-space-700/50 rounded-full text-sm text-accent-cyan mb-6">
                <Sparkles className="w-4 h-4" />
                AI-Powered Exoplanet Explorer
              </div>
              <h2 className="text-4xl md:text-5xl font-bold mb-4 bg-gradient-to-r from-accent-blue via-accent-purple to-accent-cyan bg-clip-text text-transparent">
                Explore the Cosmos
              </h2>
              <p className="text-gray-400 text-lg max-w-2xl mx-auto">
                Ask questions about exoplanets in natural language. Get instant visualizations
                from NASA's Exoplanet Archive.
              </p>
            </div>

            <div className="w-full max-w-2xl mb-12">
              <QueryInput onSubmit={handleQuery} loading={loading} />
            </div>

            <ExampleQueries onSelect={handleQuery} />

            <div className="grid grid-cols-3 gap-8 mt-16 text-center">
              <div className="flex flex-col items-center">
                <div className="w-12 h-12 rounded-xl bg-accent-blue/20 flex items-center justify-center mb-3">
                  <Search className="w-6 h-6 text-accent-blue" />
                </div>
                <h3 className="font-semibold mb-1">Natural Language</h3>
                <p className="text-sm text-gray-500">Ask in plain English</p>
              </div>
              <div className="flex flex-col items-center">
                <div className="w-12 h-12 rounded-xl bg-accent-purple/20 flex items-center justify-center mb-3">
                  <Database className="w-6 h-6 text-accent-purple" />
                </div>
                <h3 className="font-semibold mb-1">NASA Archive</h3>
                <p className="text-sm text-gray-500">5000+ confirmed planets</p>
              </div>
              <div className="flex flex-col items-center">
                <div className="w-12 h-12 rounded-xl bg-accent-cyan/20 flex items-center justify-center mb-3">
                  <Zap className="w-6 h-6 text-accent-cyan" />
                </div>
                <h3 className="font-semibold mb-1">Instant Insights</h3>
                <p className="text-sm text-gray-500">Charts & visualizations</p>
              </div>
            </div>
          </div>
        ) : (
          <div className="space-y-6">
            {messages.map((msg, idx) => (
              <div key={idx}>
                {msg.type === 'user' && (
                  <div className="flex justify-end mb-4">
                    <div className="bg-accent-blue/20 border border-accent-blue/30 rounded-2xl rounded-tr-sm px-5 py-3 max-w-xl">
                      <p className="text-white">{msg.content}</p>
                    </div>
                  </div>
                )}
                {msg.type === 'result' && (
                  <ResultCard data={msg.data} />
                )}
                {msg.type === 'error' && (
                  <div className="bg-red-500/10 border border-red-500/30 rounded-2xl px-5 py-4">
                    <p className="text-red-400">{msg.content}</p>
                  </div>
                )}
              </div>
            ))}

            {loading && (
              <div className="flex items-center gap-3 text-gray-400">
                <RefreshCw className="w-5 h-5 animate-spin" />
                <span>Querying the cosmos...</span>
              </div>
            )}

            <div ref={messagesEndRef} />

            <div className="sticky bottom-4 pt-4">
              <QueryInput onSubmit={handleQuery} loading={loading} compact />
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

export default App

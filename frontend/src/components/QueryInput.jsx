import { useState } from 'react'
import { Send, Sparkles } from 'lucide-react'

function QueryInput({ onSubmit, loading, compact }) {
  const [query, setQuery] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (query.trim() && !loading) {
      onSubmit(query.trim())
      setQuery('')
    }
  }

  return (
    <form onSubmit={handleSubmit} className="relative">
      <div className={`relative ${compact ? '' : 'group'}`}>
        <div className={`
          absolute inset-0 rounded-2xl bg-gradient-to-r from-accent-blue via-accent-purple to-accent-cyan opacity-0
          ${compact ? '' : 'group-hover:opacity-100 group-focus-within:opacity-100'}
          blur-xl transition-opacity duration-500
        `} />

        <div className={`
          relative flex items-center gap-3 bg-space-800 border border-space-600
          rounded-2xl overflow-hidden transition-all duration-300
          ${compact ? 'hover:border-space-500' : 'group-hover:border-accent-blue/50 group-focus-within:border-accent-blue'}
        `}>
          {!compact && (
            <div className="pl-4">
              <Sparkles className="w-5 h-5 text-accent-purple" />
            </div>
          )}

          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder={compact ? "Ask another question..." : "Ask about exoplanets... (e.g., 'How many Earth-sized planets are there?')"}
            className={`
              flex-1 bg-transparent outline-none text-white placeholder-gray-500
              ${compact ? 'px-4 py-3 text-sm' : 'py-4 pr-4 text-base'}
            `}
            disabled={loading}
          />

          <button
            type="submit"
            disabled={!query.trim() || loading}
            className={`
              flex items-center justify-center transition-all duration-300
              ${compact ? 'w-10 h-10 mr-1' : 'w-12 h-12 mr-2'}
              rounded-xl
              ${query.trim() && !loading
                ? 'bg-gradient-to-r from-accent-blue to-accent-purple text-white hover:shadow-lg hover:shadow-accent-blue/25'
                : 'bg-space-700 text-gray-500 cursor-not-allowed'
              }
            `}
          >
            <Send className={compact ? 'w-4 h-4' : 'w-5 h-5'} />
          </button>
        </div>
      </div>
    </form>
  )
}

export default QueryInput

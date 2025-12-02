import { Database, Clock, Zap, Code, ChevronDown, ChevronUp } from 'lucide-react'
import { useState } from 'react'
import ChartRenderer from './ChartRenderer'

function ResultCard({ data }) {
  const [showSql, setShowSql] = useState(false)
  const viz = data.visualization

  return (
    <div className="bg-space-800/50 border border-space-700 rounded-2xl overflow-hidden">
      {/* Header */}
      <div className="px-5 py-4 border-b border-space-700/50">
        <div className="flex items-start justify-between gap-4">
          <div>
            <h3 className="font-semibold text-lg text-white mb-1">
              {viz?.title || 'Query Results'}
            </h3>
            {viz?.description && (
              <p className="text-sm text-gray-400">{viz.description}</p>
            )}
          </div>
          <div className="flex items-center gap-3 text-xs">
            {data.cached && (
              <span className="flex items-center gap-1 px-2 py-1 bg-accent-cyan/20 text-accent-cyan rounded-full">
                <Zap className="w-3 h-3" />
                Cached
              </span>
            )}
            <span className="flex items-center gap-1 px-2 py-1 bg-space-700 text-gray-400 rounded-full">
              <Database className="w-3 h-3" />
              {data.row_count} rows
            </span>
          </div>
        </div>
      </div>

      {/* Visualization */}
      <div className="p-5">
        <ChartRenderer visualization={viz} />
      </div>

      {/* SQL Toggle */}
      <div className="border-t border-space-700/50">
        <button
          onClick={() => setShowSql(!showSql)}
          className="w-full px-5 py-3 flex items-center justify-between text-sm text-gray-400 hover:text-white hover:bg-space-700/30 transition-colors"
        >
          <span className="flex items-center gap-2">
            <Code className="w-4 h-4" />
            View SQL Query
          </span>
          {showSql ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
        </button>

        {showSql && (
          <div className="px-5 pb-4">
            <pre className="bg-space-900 rounded-lg p-4 overflow-x-auto text-sm font-mono text-accent-cyan">
              {data.sql}
            </pre>
          </div>
        )}
      </div>
    </div>
  )
}

export default ResultCard

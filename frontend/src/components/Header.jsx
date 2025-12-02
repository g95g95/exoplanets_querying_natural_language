import { Rocket, Trash2, Github } from 'lucide-react'

function Header({ onClear, hasMessages }) {
  return (
    <header className="border-b border-space-700/50 backdrop-blur-sm bg-space-900/80 sticky top-0 z-50">
      <div className="container mx-auto px-4 py-4 max-w-5xl">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-accent-blue to-accent-purple flex items-center justify-center">
              <Rocket className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="font-bold text-lg">Exoplanet Explorer</h1>
              <p className="text-xs text-gray-500">NASA Exoplanet Archive</p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            {hasMessages && (
              <button
                onClick={onClear}
                className="flex items-center gap-2 px-3 py-2 text-sm text-gray-400 hover:text-white hover:bg-space-700 rounded-lg transition-colors"
              >
                <Trash2 className="w-4 h-4" />
                <span className="hidden sm:inline">Clear</span>
              </button>
            )}
            <a
              href="https://exoplanetarchive.ipac.caltech.edu/"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-2 px-3 py-2 text-sm text-gray-400 hover:text-white hover:bg-space-700 rounded-lg transition-colors"
            >
              <span className="hidden sm:inline">Archive</span>
              <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
                <polyline points="15 3 21 3 21 9" />
                <line x1="10" y1="14" x2="21" y2="3" />
              </svg>
            </a>
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header

import { ArrowRight } from 'lucide-react'

const examples = [
  {
    text: "How many Earth-sized planets have been discovered?",
    icon: "🌍"
  },
  {
    text: "Show me hot Jupiters discovered by transit method",
    icon: "🪐"
  },
  {
    text: "Plot planet radius vs mass for nearby stars",
    icon: "📊"
  },
  {
    text: "Which discovery method found the most planets?",
    icon: "🔭"
  },
  {
    text: "List planets in the habitable zone",
    icon: "🌡️"
  },
  {
    text: "Show discoveries per year as a timeline",
    icon: "📈"
  }
]

function ExampleQueries({ onSelect }) {
  return (
    <div className="w-full max-w-3xl">
      <p className="text-sm text-gray-500 text-center mb-4">Try an example:</p>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {examples.map((example, idx) => (
          <button
            key={idx}
            onClick={() => onSelect(example.text)}
            className="group flex items-center gap-3 p-4 bg-space-800/50 hover:bg-space-700/70 border border-space-700 hover:border-space-500 rounded-xl text-left transition-all duration-300"
          >
            <span className="text-2xl">{example.icon}</span>
            <span className="flex-1 text-sm text-gray-300 group-hover:text-white transition-colors">
              {example.text}
            </span>
            <ArrowRight className="w-4 h-4 text-gray-600 group-hover:text-accent-blue group-hover:translate-x-1 transition-all" />
          </button>
        ))}
      </div>
    </div>
  )
}

export default ExampleQueries

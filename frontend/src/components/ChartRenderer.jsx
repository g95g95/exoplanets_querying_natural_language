import {
  ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  BarChart, Bar, LineChart, Line, Cell, Legend
} from 'recharts'
import { TrendingUp, Table as TableIcon } from 'lucide-react'

const COLORS = ['#4f8fff', '#8b5cf6', '#06b6d4', '#f97316', '#10b981', '#ec4899', '#f59e0b', '#6366f1']

function ChartRenderer({ visualization }) {
  if (!visualization) return null

  const { type, data, x_field, y_field, color_field, x_label, y_label, x_scale, y_scale } = visualization

  // No data case
  if (!data || data.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-12 text-gray-500">
        <TableIcon className="w-12 h-12 mb-3 opacity-50" />
        <p>No data found for this query</p>
      </div>
    )
  }

  // KPI - Single value display
  if (type === 'kpi') {
    const value = data[0] ? Object.values(data[0])[0] : 0
    const label = data[0] ? Object.keys(data[0])[0] : 'Value'
    return (
      <div className="flex flex-col items-center justify-center py-8">
        <div className="text-6xl font-bold bg-gradient-to-r from-accent-blue to-accent-purple bg-clip-text text-transparent mb-2">
          {typeof value === 'number' ? value.toLocaleString() : value}
        </div>
        <div className="text-gray-400 capitalize">{label.replace(/_/g, ' ')}</div>
      </div>
    )
  }

  // Scatter Plot
  if (type === 'scatter') {
    return (
      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <ScatterChart margin={{ top: 20, right: 20, bottom: 40, left: 60 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#2a2a4a" />
            <XAxis
              type="number"
              dataKey={x_field}
              name={x_label || x_field}
              scale={x_scale === 'log' ? 'log' : 'auto'}
              domain={x_scale === 'log' ? ['auto', 'auto'] : ['auto', 'auto']}
              tick={{ fill: '#9ca3af', fontSize: 12 }}
              axisLine={{ stroke: '#3a3a5a' }}
              label={{ value: x_label || x_field, position: 'bottom', fill: '#9ca3af', offset: -5 }}
            />
            <YAxis
              type="number"
              dataKey={y_field}
              name={y_label || y_field}
              scale={y_scale === 'log' ? 'log' : 'auto'}
              domain={y_scale === 'log' ? ['auto', 'auto'] : ['auto', 'auto']}
              tick={{ fill: '#9ca3af', fontSize: 12 }}
              axisLine={{ stroke: '#3a3a5a' }}
              label={{ value: y_label || y_field, angle: -90, position: 'insideLeft', fill: '#9ca3af' }}
            />
            <Tooltip
              contentStyle={{ backgroundColor: '#1a1a3a', border: '1px solid #3a3a5a', borderRadius: '8px' }}
              labelStyle={{ color: '#fff' }}
              itemStyle={{ color: '#9ca3af' }}
            />
            <Scatter
              data={data}
              fill="#4f8fff"
            >
              {color_field && data.map((entry, index) => (
                <Cell key={index} fill={COLORS[index % COLORS.length]} />
              ))}
            </Scatter>
          </ScatterChart>
        </ResponsiveContainer>
      </div>
    )
  }

  // Bar Chart
  if (type === 'bar_chart') {
    const xKey = x_field || Object.keys(data[0])[0]
    const yKey = y_field || Object.keys(data[0])[1] || 'count'

    return (
      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} margin={{ top: 20, right: 20, bottom: 60, left: 60 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#2a2a4a" />
            <XAxis
              dataKey={xKey}
              tick={{ fill: '#9ca3af', fontSize: 11 }}
              axisLine={{ stroke: '#3a3a5a' }}
              angle={-45}
              textAnchor="end"
              height={80}
              interval={0}
            />
            <YAxis
              tick={{ fill: '#9ca3af', fontSize: 12 }}
              axisLine={{ stroke: '#3a3a5a' }}
              label={{ value: y_label || yKey, angle: -90, position: 'insideLeft', fill: '#9ca3af' }}
            />
            <Tooltip
              contentStyle={{ backgroundColor: '#1a1a3a', border: '1px solid #3a3a5a', borderRadius: '8px' }}
              labelStyle={{ color: '#fff' }}
              itemStyle={{ color: '#9ca3af' }}
            />
            <Bar dataKey={yKey} radius={[4, 4, 0, 0]}>
              {data.map((entry, index) => (
                <Cell key={index} fill={COLORS[index % COLORS.length]} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    )
  }

  // Line Chart
  if (type === 'line_chart') {
    const xKey = x_field || Object.keys(data[0])[0]
    const yKey = y_field || Object.keys(data[0])[1] || 'count'

    return (
      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data} margin={{ top: 20, right: 20, bottom: 40, left: 60 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#2a2a4a" />
            <XAxis
              dataKey={xKey}
              tick={{ fill: '#9ca3af', fontSize: 12 }}
              axisLine={{ stroke: '#3a3a5a' }}
              label={{ value: x_label || xKey, position: 'bottom', fill: '#9ca3af', offset: -5 }}
            />
            <YAxis
              tick={{ fill: '#9ca3af', fontSize: 12 }}
              axisLine={{ stroke: '#3a3a5a' }}
              label={{ value: y_label || yKey, angle: -90, position: 'insideLeft', fill: '#9ca3af' }}
            />
            <Tooltip
              contentStyle={{ backgroundColor: '#1a1a3a', border: '1px solid #3a3a5a', borderRadius: '8px' }}
              labelStyle={{ color: '#fff' }}
              itemStyle={{ color: '#9ca3af' }}
            />
            <Line
              type="monotone"
              dataKey={yKey}
              stroke="#4f8fff"
              strokeWidth={2}
              dot={{ fill: '#4f8fff', strokeWidth: 2, r: 4 }}
              activeDot={{ r: 6, fill: '#8b5cf6' }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    )
  }

  // Histogram (treat as bar chart)
  if (type === 'histogram') {
    const xKey = x_field || Object.keys(data[0])[0]
    const yKey = y_field || Object.keys(data[0])[1] || 'count'

    return (
      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} margin={{ top: 20, right: 20, bottom: 40, left: 60 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#2a2a4a" />
            <XAxis
              dataKey={xKey}
              tick={{ fill: '#9ca3af', fontSize: 12 }}
              axisLine={{ stroke: '#3a3a5a' }}
            />
            <YAxis
              tick={{ fill: '#9ca3af', fontSize: 12 }}
              axisLine={{ stroke: '#3a3a5a' }}
            />
            <Tooltip
              contentStyle={{ backgroundColor: '#1a1a3a', border: '1px solid #3a3a5a', borderRadius: '8px' }}
            />
            <Bar dataKey={yKey} fill="#8b5cf6" radius={[2, 2, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    )
  }

  // Table (default)
  if (type === 'table' || !type) {
    const columns = data.length > 0 ? Object.keys(data[0]) : []
    const displayData = data.slice(0, 100) // Limit to 100 rows

    return (
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-space-700">
              {columns.map(col => (
                <th key={col} className="px-4 py-3 text-left text-gray-400 font-medium whitespace-nowrap">
                  {col.replace(/_/g, ' ')}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {displayData.map((row, idx) => (
              <tr key={idx} className="border-b border-space-700/50 hover:bg-space-700/30 transition-colors">
                {columns.map(col => (
                  <td key={col} className="px-4 py-3 text-gray-300 whitespace-nowrap">
                    {typeof row[col] === 'number'
                      ? row[col].toLocaleString(undefined, { maximumFractionDigits: 4 })
                      : row[col] ?? '-'}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
        {data.length > 100 && (
          <p className="text-center text-sm text-gray-500 py-3">
            Showing 100 of {data.length} rows
          </p>
        )}
      </div>
    )
  }

  // Fallback
  return (
    <div className="text-gray-400 text-center py-8">
      Unknown visualization type: {type}
    </div>
  )
}

export default ChartRenderer

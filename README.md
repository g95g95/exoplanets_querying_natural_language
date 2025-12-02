# Exoplanet Data Analyst Agent

AI-powered natural language interface to the NASA Exoplanet Archive. Ask questions about exoplanets in plain English and get beautiful, interactive visualizations.

![Exoplanet Explorer](https://img.shields.io/badge/NASA-Exoplanet%20Archive-blue) ![React](https://img.shields.io/badge/React-18-61DAFB) ![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688)

## Features

- Natural language to ADQL (Astronomical Data Query Language) translation
- Query execution against NASA TAP endpoint with intelligent caching
- Beautiful React frontend with interactive charts (Scatter, Bar, Line, KPI)
- Dark space theme with responsive design
- Conversational context for follow-up questions
- Support for astronomical concepts (Earth-sized, Hot Jupiter, habitable zone, etc.)

## Quick Start

### Backend Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Configure API keys
cp .env.example .env
# Edit .env with your OPENAI_API_KEY or ANTHROPIC_API_KEY

# Start the backend server
python -m src.agent.server
```

The API will be available at `http://localhost:8000`.

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:3000`.

## Screenshots

The frontend features:
- Space-themed dark UI with gradient accents
- Real-time query input with example suggestions
- Interactive charts powered by Recharts
- SQL query viewer for transparency
- Cache status indicators

## API Usage

### Ask a Question

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "How many Earth-sized planets have been discovered?"}'
```

### Response Format

```json
{
  "success": true,
  "sql": "SELECT COUNT(*) as count FROM pscomppars WHERE pl_rade >= 0.8 AND pl_rade <= 1.25",
  "row_count": 1,
  "cached": false,
  "visualization": {
    "type": "kpi",
    "title": "Earth-sized Planets Count",
    "description": "Number of planets with radius 0.8-1.25 Earth radii",
    "data": [{"count": 1234}]
  }
}
```

### Additional Endpoints

- `GET /health` - Health check
- `GET /schema/{table}` - Get table schema (ps, pscomppars, keplernames)
- `POST /clear/{session_id}` - Clear conversation state
- `GET /cache/stats` - View cache statistics
- `POST /cache/clear` - Clear query cache

## Example Questions

- "How many Earth-sized planets have been discovered?"
- "Show me hot Jupiters discovered by transit method"
- "Plot planet radius vs mass for nearby stars"
- "Which discovery method found the most planets?"
- "List planets in the habitable zone"
- "Show discoveries per year as a timeline"

## Project Structure

```
├── src/
│   ├── agent/          # LLM integration and FastAPI server
│   ├── tools/          # TAP query, SQL validation, caching
│   ├── mappings/       # Astronomical concept mappings
│   └── viz/            # Visualization specifications
├── frontend/
│   ├── src/
│   │   ├── components/ # React components
│   │   └── App.jsx     # Main application
│   └── package.json
├── schema_cache/       # NASA table metadata
├── tests/              # Unit and integration tests
└── requirements.txt
```

## Visualization Types

| Type | Use Case |
|------|----------|
| `scatter` | Compare two continuous variables (radius vs mass) |
| `line_chart` | Time series data (discoveries per year) |
| `bar_chart` | Categorical comparisons (count by discovery method) |
| `histogram` | Distribution of a single variable |
| `table` | Raw data display or lists |
| `kpi` | Single numeric value (total count) |

## Running Tests

```bash
# All tests
pytest tests/ -v

# Unit tests only
pytest tests/unit/ -v

# Integration tests (requires network)
pytest tests/integration/ -v -m integration
```

## Caching

Query results are cached for 15 minutes to improve performance and reduce load on NASA's servers. Cache is stored both in-memory and on disk.

```bash
# View cache stats
curl http://localhost:8000/cache/stats

# Clear cache
curl -X POST http://localhost:8000/cache/clear
```

## Configuration

Environment variables (`.env`):

| Variable | Description | Default |
|----------|-------------|---------|
| `LLM_PROVIDER` | LLM provider (openai/anthropic) | openai |
| `LLM_MODEL` | Model name | gpt-4o |
| `OPENAI_API_KEY` | OpenAI API key | - |
| `ANTHROPIC_API_KEY` | Anthropic API key | - |
| `HOST` | Server host | 0.0.0.0 |
| `PORT` | Server port | 8000 |
| `DEBUG` | Enable debug mode | false |

## License

MIT

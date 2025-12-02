# Exoplanet Data Analyst Agent

AI-powered natural language interface to the NASA Exoplanet Archive. Ask questions about exoplanets in plain English and get structured data visualizations.

## Features

- Natural language to ADQL (Astronomical Data Query Language) translation
- Query execution against NASA TAP endpoint
- Automatic visualization specification generation
- Conversational context for follow-up questions
- Support for astronomical concepts (Earth-sized, Hot Jupiter, habitable zone, etc.)

## Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Configuration

Copy `.env.example` to `.env` and add your API keys:

```bash
cp .env.example .env
```

Edit `.env`:
```
OPENAI_API_KEY=your_openai_key
# or
ANTHROPIC_API_KEY=your_anthropic_key
LLM_PROVIDER=openai  # or anthropic
```

### Run the Server

```bash
python -m src.agent.server
```

The API will be available at `http://localhost:8000`.

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
  "visualization": {
    "type": "kpi",
    "title": "Earth-sized Planets Count",
    "description": "Number of planets with radius 0.8-1.25 Earth radii",
    "data": [{"count": 1234}]
  }
}
```

## Example Questions

- "Show me all hot Jupiters discovered in the last 5 years"
- "What are the 10 closest exoplanets to Earth?"
- "Plot planet radius vs mass for transiting planets"
- "How many planets are in the habitable zone?"
- "Which discovery method has found the most planets?"

## Project Structure

```
src/
├── agent/          # LLM integration and server
├── tools/          # TAP query and SQL validation
├── mappings/       # Astronomical concept mappings
└── viz/            # Visualization specifications
schema_cache/       # NASA table metadata
tests/              # Unit and integration tests
```

## Running Tests

```bash
# All tests
pytest tests/ -v

# Unit tests only
pytest tests/unit/ -v

# Integration tests (requires network)
pytest tests/integration/ -v -m integration
```

## Refresh Schema Cache

```bash
python -m src.tools.schema --refresh
```

## License

MIT

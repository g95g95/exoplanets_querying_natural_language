# CLAUDE.md - Exoplanet Data Analyst Agent

## Best Practices

1. First think through the problem, read the codebase for relevant files, and write a plan to `tasks/todo.md`.
2. The plan should have a list of todo items that you can check off as you complete them.
3. Before you begin working, check in with me and I will verify the plan.
4. Then, begin working on the todo items, marking them as complete as you go.
5. Please every step of the way just give me a high level explanation of what changes you made.
6. Make every task and code change you do as simple as possible. We want to avoid making any massive or complex changes. Every change should impact as little code as possible. Everything is about simplicity.
7. Finally, add a review section to the `tasks/todo.md` file with a summary of the changes you made and any other relevant information.
8. DO NOT BE LAZY. NEVER BE LAZY. IF THERE IS A BUG FIND THE ROOT CAUSE AND FIX IT. NO TEMPORARY FIXES. YOU ARE A SENIOR DEVELOPER. NEVER BE LAZY.
9. MAKE ALL FIXES AND CODE CHANGES AS SIMPLE AS HUMANLY POSSIBLE. THEY SHOULD ONLY IMPACT NECESSARY CODE RELEVANT TO THE TASK AND NOTHING ELSE. IT SHOULD IMPACT AS LITTLE CODE AS POSSIBLE. YOUR GOAL IS TO NOT INTRODUCE ANY BUGS. IT'S ALL ABOUT SIMPLICITY.



## Project Overview

This project implements an AI-powered agent that translates natural language questions about exoplanets into valid TAP (Table Access Protocol) SQL queries against the NASA Exoplanet Archive, executes them, and returns structured visualization specifications for frontend rendering.

**Primary endpoint:** `https://exoplanetarchive.ipac.caltech.edu/TAP`

---

## Architecture

```
User Question → LLM Agent → TAP SQL Generation → NASA TAP API → JSON Results → Visualization Spec
```

### Key Components

| Directory | Purpose |
|-----------|---------|
| `src/agent/` | LLM integration, prompt templates, conversation state |
| `src/tools/` | Tool implementations: schema lookup, TAP query execution, SQL validation |
| `src/mappings/` | Astronomical concept → numeric threshold mappings |
| `src/viz/` | Visualization specification builders |
| `schema_cache/` | Cached NASA Exoplanet Archive table/column metadata |
| `frontend/` | React-based chart renderer consuming viz specs |
| `tests/` | Unit and integration tests |

---

## Core Tools

### 1. `get_exoplanet_schema`
Returns curated column metadata from NASA Exoplanet Archive tables.

**Primary tables:**
- `ps` - Planetary Systems (main table, one row per planet-reference combination)
- `pscomppars` - Planetary Systems Composite Parameters (one row per planet, best values)
- `keplernames` - Kepler Objects of Interest

### 2. `run_tap_query`
Executes ADQL queries against NASA TAP endpoint. Returns JSON rows.

### 3. `validate_sql` (optional)
Pre-flight safety and schema validation.

---

## Critical Schema Reference

### Commonly Used Columns (ps/pscomppars tables)

| Column | Description | Units |
|--------|-------------|-------|
| `pl_name` | Planet name | - |
| `hostname` | Host star name | - |
| `pl_rade` | Planet radius | Earth radii |
| `pl_bmasse` | Planet mass | Earth masses |
| `pl_orbper` | Orbital period | days |
| `pl_orbsmax` | Semi-major axis | AU |
| `pl_eqt` | Equilibrium temperature | K |
| `pl_tranflag` | Transit flag | 0/1 |
| `pl_discmethod` | Discovery method | string |
| `disc_year` | Discovery year | year |
| `st_teff` | Stellar effective temp | K |
| `st_rad` | Stellar radius | Solar radii |
| `st_mass` | Stellar mass | Solar masses |
| `st_dist` | Distance to star | parsec |
| `sy_snum` | Number of stars in system | count |
| `sy_pnum` | Number of planets in system | count |

---

## Astronomical Concept Mappings

When users use qualitative language, convert to these thresholds:

| Concept | Column(s) | Condition |
|---------|-----------|-----------|
| Earth-sized | `pl_rade` | `0.8 <= pl_rade <= 1.25` |
| Earth-like | `pl_rade`, `pl_bmasse` | `0.8 <= pl_rade <= 1.5 AND pl_bmasse <= 2` |
| Super-Earth | `pl_rade` | `1.25 < pl_rade <= 2.0` |
| Mini-Neptune | `pl_rade` | `2.0 < pl_rade <= 4.0` |
| Neptune-sized | `pl_rade` | `3.0 <= pl_rade <= 6.0` |
| Jupiter-sized | `pl_rade` | `9.0 <= pl_rade <= 13.0` |
| Hot Jupiter | `pl_rade`, `pl_orbper` | `pl_rade >= 9.0 AND pl_orbper < 10` |
| Warm Jupiter | `pl_rade`, `pl_orbper` | `pl_rade >= 9.0 AND 10 <= pl_orbper <= 100` |
| Cold Jupiter | `pl_rade`, `pl_orbper` | `pl_rade >= 9.0 AND pl_orbper > 100` |
| Close-in / Ultra-short period | `pl_orbper` | `pl_orbper < 1` |
| Habitable zone (approx) | `pl_eqt` | `200 <= pl_eqt <= 320` |
| Transiting | `pl_tranflag` | `pl_tranflag = 1` |
| Multi-planet system | `sy_pnum` | `sy_pnum >= 2` |
| Nearby | `st_dist` | `st_dist <= 30` (parsecs) |

---

## SQL Generation Rules

### MUST follow:
1. **Read-only SELECT only** - Never INSERT, UPDATE, DELETE, DROP, ALTER
2. **No semicolons** - TAP ADQL doesn't use them
3. **No SELECT *** - Always specify columns explicitly
4. **Use ORDER BY** - For deterministic results
5. **Use LIMIT** - When results could be large (default: 1000, max: 10000)
6. **Column validation** - Only reference columns that exist in schema

### Query template:
```sql
SELECT column1, column2, column3
FROM ps
WHERE condition1 AND condition2
ORDER BY column1
LIMIT 1000
```

### Common patterns:
```sql
-- Count by discovery method
SELECT pl_discmethod, COUNT(*) as count
FROM ps
WHERE pl_discmethod IS NOT NULL
GROUP BY pl_discmethod
ORDER BY count DESC

-- Planets with radius and mass
SELECT pl_name, pl_rade, pl_bmasse, pl_orbper
FROM pscomppars
WHERE pl_rade IS NOT NULL AND pl_bmasse IS NOT NULL
ORDER BY pl_rade

-- Discovery timeline
SELECT disc_year, COUNT(*) as discoveries
FROM pscomppars
WHERE disc_year IS NOT NULL
GROUP BY disc_year
ORDER BY disc_year
```

---

## Visualization Spec Format

All agent responses MUST return this JSON structure:

```json
{
  "visualization": {
    "type": "scatter | line_chart | bar_chart | stacked_bar | histogram | table | kpi",
    "title": "Human-readable title",
    "description": "Brief explanation of what's shown",
    "x_field": "column_name or null",
    "y_field": "column_name or null", 
    "color_field": "column_name or null",
    "size_field": "column_name or null",
    "x_label": "Axis label with units",
    "y_label": "Axis label with units",
    "x_scale": "linear | log",
    "y_scale": "linear | log",
    "data": [
      {"col1": value1, "col2": value2},
      ...
    ]
  }
}
```

### Visualization type guidelines:
- **scatter** - Comparing two continuous variables (e.g., radius vs mass)
- **line_chart** - Time series or ordered sequences (e.g., discoveries per year)
- **bar_chart** - Categorical comparisons (e.g., count by discovery method)
- **histogram** - Distribution of a single variable
- **table** - Raw data display or when user asks for "list"
- **kpi** - Single numeric answer (e.g., "how many Earth-sized planets?")

---

## Conversational Context Rules

The agent MUST maintain state across conversation turns:

1. **Additive filters**: "now only transiting" → add `AND pl_tranflag = 1`
2. **Replace filters**: "change to planets larger than 5 Earth radii" → update `pl_rade` condition
3. **Visualization changes**: "show as bar chart" → change `type`, keep query
4. **Column additions**: "color by discovery method" → add `color_field`, ensure column in SELECT

Store and track:
- Last SQL query
- Last visualization spec
- Active filters as structured object
- Selected columns

---

## Error Handling

| Error Type | Handling |
|------------|----------|
| Invalid column reference | Return error with suggestion from schema |
| TAP timeout | Retry once, then suggest adding LIMIT or filters |
| Empty results | Return valid spec with empty data array + helpful message |
| Ambiguous request | Choose most reasonable interpretation, note assumption in description |

---

## Testing

### Unit tests (`tests/unit/`)
- SQL generation from various natural language inputs
- Schema validation
- Concept mapping thresholds
- Viz spec structure validation

### Integration tests (`tests/integration/`)
- Live TAP queries (use small LIMITs)
- End-to-end: question → viz spec
- Conversation state persistence

### Run tests:
```bash
pytest tests/ -v
pytest tests/unit/ -v --fast  # Skip integration
```

---

## Development Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the agent server
python -m src.agent.server

# Refresh schema cache from NASA
python -m src.tools.schema --refresh

# Validate a SQL query
python -m src.tools.sql_validator "SELECT pl_name FROM ps LIMIT 10"

# Run frontend
cd frontend && npm install && npm run dev
```

---

## Code Style

- **Python**: Follow PEP 8, use type hints, docstrings for public functions
- **SQL**: UPPERCASE keywords, lowercase column names
- **JSON**: 2-space indentation
- **Naming**: snake_case for Python, camelCase for JavaScript/TypeScript

---

## Security Constraints

1. **Never execute arbitrary SQL** - Always validate against schema
2. **No credentials in code** - Use environment variables
3. **Rate limiting** - Respect NASA TAP limits (be a good citizen)
4. **Input sanitization** - Escape/validate all user inputs before SQL generation

---

## References

- [NASA Exoplanet Archive TAP Documentation](https://exoplanetarchive.ipac.caltech.edu/docs/TAP/usingTAP.html)
- [ADQL (Astronomical Data Query Language) Spec](https://www.ivoa.net/documents/ADQL/)
- [Planetary Systems Table Column Definitions](https://exoplanetarchive.ipac.caltech.edu/docs/API_PS_columns.html)
- [pyvo - Python TAP Client](https://pyvo.readthedocs.io/)

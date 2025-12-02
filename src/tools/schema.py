"""Schema lookup tool for NASA Exoplanet Archive tables."""

import json
from pathlib import Path
from typing import Dict, List, Optional

SCHEMA_CACHE_PATH = Path(__file__).parent.parent.parent / "schema_cache" / "columns.json"

_schema_cache: Optional[Dict] = None


def _load_schema() -> Dict:
    """Load schema from cache file."""
    global _schema_cache
    if _schema_cache is None:
        with open(SCHEMA_CACHE_PATH, "r") as f:
            _schema_cache = json.load(f)
    return _schema_cache


def get_exoplanet_schema(table: str = "pscomppars") -> Dict:
    """Get schema information for a NASA Exoplanet Archive table.

    Args:
        table: Table name (ps, pscomppars, keplernames). Default: pscomppars

    Returns:
        Dict with table description and column metadata
    """
    schema = _load_schema()
    if table not in schema:
        available = list(schema.keys())
        raise ValueError(f"Unknown table '{table}'. Available: {available}")
    return schema[table]


def get_column_info(column: str, table: str = "pscomppars") -> Optional[Dict]:
    """Get information about a specific column.

    Args:
        column: Column name
        table: Table name

    Returns:
        Dict with type, description, units or None if not found
    """
    schema = get_exoplanet_schema(table)
    return schema["columns"].get(column)


def validate_columns(columns: List[str], table: str = "pscomppars") -> Dict:
    """Validate that columns exist in the schema.

    Args:
        columns: List of column names to validate
        table: Table name

    Returns:
        Dict with 'valid', 'invalid', and 'suggestions' keys
    """
    schema = get_exoplanet_schema(table)
    valid_columns = set(schema["columns"].keys())

    valid = []
    invalid = []
    suggestions = {}

    for col in columns:
        if col in valid_columns:
            valid.append(col)
        else:
            invalid.append(col)
            # Find similar column names
            similar = [c for c in valid_columns if col.lower() in c.lower() or c.lower() in col.lower()]
            if similar:
                suggestions[col] = similar

    return {
        "valid": valid,
        "invalid": invalid,
        "suggestions": suggestions
    }


def get_all_columns(table: str = "pscomppars") -> List[str]:
    """Get all column names for a table.

    Args:
        table: Table name

    Returns:
        List of column names
    """
    schema = get_exoplanet_schema(table)
    return list(schema["columns"].keys())


def refresh_schema_cache():
    """Refresh schema cache from NASA TAP endpoint.

    This function queries the NASA TAP endpoint to get current schema
    and updates the local cache file.
    """
    import requests

    url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"

    tables = ["ps", "pscomppars", "keplernames"]
    schema = {}

    for table in tables:
        query = f"SELECT column_name, datatype, description, unit FROM TAP_SCHEMA.columns WHERE table_name = '{table}'"
        params = {"query": query, "format": "json"}

        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        columns = {}
        for row in data:
            col_name = row.get("column_name")
            if col_name:
                columns[col_name] = {
                    "type": row.get("datatype", "string"),
                    "description": row.get("description", ""),
                    "units": row.get("unit")
                }

        schema[table] = {
            "description": f"Table {table}",
            "columns": columns
        }

    with open(SCHEMA_CACHE_PATH, "w") as f:
        json.dump(schema, f, indent=2)

    global _schema_cache
    _schema_cache = schema

    return schema


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--refresh":
        print("Refreshing schema cache from NASA TAP endpoint...")
        refresh_schema_cache()
        print("Schema cache updated.")
    else:
        schema = get_exoplanet_schema()
        print(f"Table: pscomppars")
        print(f"Columns: {len(schema['columns'])}")
        for col, info in list(schema['columns'].items())[:5]:
            print(f"  {col}: {info['description']}")

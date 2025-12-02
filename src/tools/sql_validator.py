"""SQL validation tool for ADQL queries."""

import re
from typing import Dict, List, Optional, Tuple

from .schema import get_all_columns, validate_columns


def validate_sql(query: str, table: str = "pscomppars") -> Dict:
    """Validate an ADQL query for safety and schema compliance.

    Args:
        query: ADQL query string
        table: Expected table name for column validation

    Returns:
        Dict with 'valid', 'errors', 'warnings' keys
    """
    errors = []
    warnings = []

    query = query.strip()
    query_upper = query.upper()

    # Check for SELECT
    if not query_upper.startswith("SELECT"):
        errors.append("Query must start with SELECT")

    # Check for semicolons
    if ";" in query:
        warnings.append("Semicolons should be removed for TAP ADQL")

    # Check for SELECT *
    if re.search(r"SELECT\s+\*", query_upper):
        errors.append("SELECT * is not allowed. Specify columns explicitly.")

    # Check for forbidden operations
    forbidden = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "TRUNCATE", "CREATE"]
    for op in forbidden:
        if re.search(rf"\b{op}\b", query_upper):
            errors.append(f"Forbidden operation: {op}")

    # Check for LIMIT
    if "LIMIT" not in query_upper:
        warnings.append("Consider adding LIMIT to prevent large result sets")

    # Extract and validate columns
    columns_result = _extract_columns(query)
    if columns_result:
        validation = validate_columns(columns_result, table)
        if validation["invalid"]:
            for col in validation["invalid"]:
                suggestion = validation["suggestions"].get(col, [])
                if suggestion:
                    errors.append(f"Invalid column '{col}'. Did you mean: {suggestion}")
                else:
                    errors.append(f"Invalid column '{col}'")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "query": query.rstrip(";")
    }


def _extract_columns(query: str) -> List[str]:
    """Extract column names from SELECT clause.

    Args:
        query: SQL query

    Returns:
        List of column names
    """
    query_upper = query.upper()

    # Find SELECT ... FROM
    match = re.search(r"SELECT\s+(.+?)\s+FROM", query, re.IGNORECASE | re.DOTALL)
    if not match:
        return []

    select_clause = match.group(1)

    # Handle aggregates and aliases
    columns = []
    for part in select_clause.split(","):
        part = part.strip()

        # Skip if it's an aggregate without column
        if re.match(r"^(COUNT|SUM|AVG|MIN|MAX)\s*\(\s*\*\s*\)", part, re.IGNORECASE):
            continue

        # Extract column from aggregate function
        agg_match = re.match(r"(COUNT|SUM|AVG|MIN|MAX)\s*\(\s*(\w+)\s*\)", part, re.IGNORECASE)
        if agg_match:
            columns.append(agg_match.group(2))
            continue

        # Handle alias (column AS alias or column alias)
        alias_match = re.match(r"(\w+)\s+(?:AS\s+)?(\w+)", part, re.IGNORECASE)
        if alias_match:
            columns.append(alias_match.group(1))
            continue

        # Plain column name
        if re.match(r"^\w+$", part):
            columns.append(part)

    return columns


def suggest_fix(error_message: str, query: str) -> Optional[str]:
    """Suggest a fix for common query errors.

    Args:
        error_message: Error message from validation or TAP
        query: Original query

    Returns:
        Suggested fixed query or None
    """
    # Remove semicolons
    if "semicolon" in error_message.lower():
        return query.rstrip(";")

    # SELECT * fix
    if "SELECT *" in error_message:
        return None  # Can't auto-fix without knowing desired columns

    return None


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        result = validate_sql(query)
        print(f"Valid: {result['valid']}")
        if result['errors']:
            print(f"Errors: {result['errors']}")
        if result['warnings']:
            print(f"Warnings: {result['warnings']}")
    else:
        print("Usage: python -m src.tools.sql_validator \"SELECT pl_name FROM ps LIMIT 10\"")

"""TAP query execution tool for NASA Exoplanet Archive."""

import requests
from typing import Dict, List, Optional, Any

from ..config import NASA_TAP_URL, DEFAULT_LIMIT, MAX_LIMIT


def run_tap_query(
    query: str,
    timeout: int = 60,
    format: str = "json"
) -> Dict[str, Any]:
    """Execute an ADQL query against the NASA Exoplanet Archive TAP endpoint.

    Args:
        query: ADQL query string (no semicolons)
        timeout: Request timeout in seconds
        format: Response format (json, csv, votable)

    Returns:
        Dict with 'success', 'data', 'row_count', and optionally 'error' keys
    """
    # Clean query - remove semicolons if present
    query = query.strip().rstrip(";")

    # Validate query is SELECT only
    query_upper = query.upper().strip()
    if not query_upper.startswith("SELECT"):
        return {
            "success": False,
            "error": "Only SELECT queries are allowed",
            "data": [],
            "row_count": 0
        }

    # Check for forbidden operations
    forbidden = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "TRUNCATE", "CREATE"]
    for op in forbidden:
        if op in query_upper:
            return {
                "success": False,
                "error": f"Forbidden operation: {op}",
                "data": [],
                "row_count": 0
            }

    url = f"{NASA_TAP_URL}/sync"
    params = {
        "query": query,
        "format": format
    }

    try:
        response = requests.get(url, params=params, timeout=timeout)
        response.raise_for_status()

        if format == "json":
            data = response.json()
            return {
                "success": True,
                "data": data,
                "row_count": len(data)
            }
        else:
            return {
                "success": True,
                "data": response.text,
                "row_count": None
            }

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "Query timed out. Try adding LIMIT or more filters.",
            "data": [],
            "row_count": 0
        }
    except requests.exceptions.HTTPError as e:
        error_msg = str(e)
        if response.text:
            error_msg = f"{error_msg}: {response.text[:500]}"
        return {
            "success": False,
            "error": error_msg,
            "data": [],
            "row_count": 0
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"Request failed: {str(e)}",
            "data": [],
            "row_count": 0
        }
    except ValueError as e:
        return {
            "success": False,
            "error": f"Invalid JSON response: {str(e)}",
            "data": [],
            "row_count": 0
        }


def build_query(
    columns: List[str],
    table: str = "pscomppars",
    where: Optional[str] = None,
    order_by: Optional[str] = None,
    limit: int = DEFAULT_LIMIT
) -> str:
    """Build an ADQL query string.

    Args:
        columns: List of column names to select
        table: Table name
        where: WHERE clause conditions (without 'WHERE' keyword)
        order_by: ORDER BY clause (without 'ORDER BY' keyword)
        limit: Maximum rows to return

    Returns:
        ADQL query string
    """
    if limit > MAX_LIMIT:
        limit = MAX_LIMIT

    columns_str = ", ".join(columns)
    query = f"SELECT {columns_str}\nFROM {table}"

    if where:
        query += f"\nWHERE {where}"

    if order_by:
        query += f"\nORDER BY {order_by}"

    query += f"\nLIMIT {limit}"

    return query

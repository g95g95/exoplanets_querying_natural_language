"""Visualization specification builder."""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional, Literal

VizType = Literal["scatter", "line_chart", "bar_chart", "stacked_bar", "histogram", "table", "kpi"]
ScaleType = Literal["linear", "log"]


@dataclass
class VisualizationSpec:
    """Visualization specification for frontend rendering."""

    type: VizType
    title: str
    description: str
    data: List[Dict[str, Any]]
    x_field: Optional[str] = None
    y_field: Optional[str] = None
    color_field: Optional[str] = None
    size_field: Optional[str] = None
    x_label: Optional[str] = None
    y_label: Optional[str] = None
    x_scale: ScaleType = "linear"
    y_scale: ScaleType = "linear"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {"visualization": asdict(self)}


def build_visualization(
    viz_type: VizType,
    title: str,
    description: str,
    data: List[Dict[str, Any]],
    x_field: Optional[str] = None,
    y_field: Optional[str] = None,
    color_field: Optional[str] = None,
    size_field: Optional[str] = None,
    x_label: Optional[str] = None,
    y_label: Optional[str] = None,
    x_scale: ScaleType = "linear",
    y_scale: ScaleType = "linear"
) -> VisualizationSpec:
    """Build a visualization specification.

    Args:
        viz_type: Type of visualization
        title: Human-readable title
        description: Brief explanation
        data: List of data rows
        x_field: Column for x-axis
        y_field: Column for y-axis
        color_field: Column for color encoding
        size_field: Column for size encoding
        x_label: X-axis label with units
        y_label: Y-axis label with units
        x_scale: X-axis scale (linear or log)
        y_scale: Y-axis scale (linear or log)

    Returns:
        VisualizationSpec instance
    """
    return VisualizationSpec(
        type=viz_type,
        title=title,
        description=description,
        data=data,
        x_field=x_field,
        y_field=y_field,
        color_field=color_field,
        size_field=size_field,
        x_label=x_label,
        y_label=y_label,
        x_scale=x_scale,
        y_scale=y_scale
    )


def suggest_visualization_type(
    columns: List[str],
    query_intent: Optional[str] = None
) -> VizType:
    """Suggest appropriate visualization type based on columns and intent.

    Args:
        columns: List of column names in the result
        query_intent: Optional hint about query purpose

    Returns:
        Suggested visualization type
    """
    # Single value queries
    if len(columns) == 1 and "count" in columns[0].lower():
        return "kpi"

    # Time series
    if "disc_year" in columns or "year" in columns:
        return "line_chart"

    # Categorical groupings
    categorical = ["pl_discmethod", "hostname"]
    if any(c in columns for c in categorical) and "count" in str(columns).lower():
        return "bar_chart"

    # Two numeric columns -> scatter
    numeric_cols = ["pl_rade", "pl_bmasse", "pl_orbper", "pl_eqt", "st_teff", "st_rad", "st_mass", "st_dist"]
    numeric_count = sum(1 for c in columns if c in numeric_cols)
    if numeric_count >= 2:
        return "scatter"

    # Default to table
    return "table"


# Column label mappings for better axis labels
COLUMN_LABELS = {
    "pl_name": "Planet Name",
    "hostname": "Host Star",
    "pl_rade": "Planet Radius (Earth radii)",
    "pl_bmasse": "Planet Mass (Earth masses)",
    "pl_orbper": "Orbital Period (days)",
    "pl_orbsmax": "Semi-major Axis (AU)",
    "pl_eqt": "Equilibrium Temperature (K)",
    "pl_discmethod": "Discovery Method",
    "disc_year": "Discovery Year",
    "st_teff": "Stellar Temperature (K)",
    "st_rad": "Stellar Radius (Solar radii)",
    "st_mass": "Stellar Mass (Solar masses)",
    "st_dist": "Distance (parsecs)",
    "sy_pnum": "Planets in System",
    "count": "Count",
}


def get_column_label(column: str) -> str:
    """Get human-readable label for a column.

    Args:
        column: Column name

    Returns:
        Human-readable label
    """
    return COLUMN_LABELS.get(column, column)

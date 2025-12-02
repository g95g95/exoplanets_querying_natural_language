"""Pytest configuration and fixtures."""

import pytest


@pytest.fixture
def sample_query_result():
    """Sample TAP query result."""
    return {
        "success": True,
        "data": [
            {"pl_name": "Kepler-442 b", "pl_rade": 1.34, "pl_bmasse": 2.34},
            {"pl_name": "Kepler-62 f", "pl_rade": 1.41, "pl_bmasse": 2.80},
        ],
        "row_count": 2
    }


@pytest.fixture
def sample_viz_spec():
    """Sample visualization specification."""
    return {
        "type": "scatter",
        "title": "Planet Radius vs Mass",
        "description": "Scatter plot of exoplanet radius against mass",
        "x_field": "pl_rade",
        "y_field": "pl_bmasse",
        "x_label": "Planet Radius (Earth radii)",
        "y_label": "Planet Mass (Earth masses)",
        "x_scale": "log",
        "y_scale": "log"
    }

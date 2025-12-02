"""Tests for visualization specification builder."""

import pytest
from src.viz.spec_builder import (
    VisualizationSpec,
    build_visualization,
    suggest_visualization_type,
    get_column_label
)


class TestVisualizationSpec:
    """Test VisualizationSpec class."""

    def test_create_scatter_spec(self):
        """Test creating scatter plot spec."""
        spec = VisualizationSpec(
            type="scatter",
            title="Test Scatter",
            description="Test description",
            data=[{"x": 1, "y": 2}],
            x_field="x",
            y_field="y"
        )
        assert spec.type == "scatter"
        assert spec.title == "Test Scatter"
        assert len(spec.data) == 1

    def test_to_dict(self):
        """Test conversion to dictionary."""
        spec = VisualizationSpec(
            type="table",
            title="Test Table",
            description="Test",
            data=[]
        )
        result = spec.to_dict()
        assert "visualization" in result
        assert result["visualization"]["type"] == "table"

    def test_default_scales(self):
        """Test default scale values."""
        spec = VisualizationSpec(
            type="scatter",
            title="Test",
            description="Test",
            data=[]
        )
        assert spec.x_scale == "linear"
        assert spec.y_scale == "linear"


class TestBuildVisualization:
    """Test build_visualization function."""

    def test_build_scatter(self):
        """Test building scatter visualization."""
        data = [{"pl_rade": 1.0, "pl_bmasse": 1.0}]
        spec = build_visualization(
            viz_type="scatter",
            title="Radius vs Mass",
            description="Test",
            data=data,
            x_field="pl_rade",
            y_field="pl_bmasse",
            x_scale="log",
            y_scale="log"
        )
        assert spec.type == "scatter"
        assert spec.x_field == "pl_rade"
        assert spec.y_field == "pl_bmasse"
        assert spec.x_scale == "log"
        assert spec.y_scale == "log"

    def test_build_kpi(self):
        """Test building KPI visualization."""
        data = [{"count": 5000}]
        spec = build_visualization(
            viz_type="kpi",
            title="Total Exoplanets",
            description="Count of confirmed exoplanets",
            data=data
        )
        assert spec.type == "kpi"
        assert spec.data[0]["count"] == 5000


class TestSuggestVisualizationType:
    """Test visualization type suggestions."""

    def test_suggest_kpi_for_count(self):
        """Test KPI suggested for count queries."""
        viz_type = suggest_visualization_type(["count"])
        assert viz_type == "kpi"

    def test_suggest_line_for_time_series(self):
        """Test line chart for time series."""
        viz_type = suggest_visualization_type(["disc_year", "count"])
        assert viz_type == "line_chart"

    def test_suggest_bar_for_categorical(self):
        """Test bar chart for categorical data."""
        viz_type = suggest_visualization_type(["pl_discmethod", "count"])
        assert viz_type == "bar_chart"

    def test_suggest_scatter_for_numeric(self):
        """Test scatter for two numeric columns."""
        viz_type = suggest_visualization_type(["pl_rade", "pl_bmasse"])
        assert viz_type == "scatter"

    def test_suggest_table_default(self):
        """Test table as default."""
        viz_type = suggest_visualization_type(["pl_name", "hostname"])
        assert viz_type == "table"


class TestColumnLabels:
    """Test column label lookups."""

    def test_known_column_label(self):
        """Test label for known column."""
        label = get_column_label("pl_rade")
        assert "Radius" in label
        assert "Earth" in label

    def test_unknown_column_returns_itself(self):
        """Test unknown column returns column name."""
        label = get_column_label("unknown_col")
        assert label == "unknown_col"

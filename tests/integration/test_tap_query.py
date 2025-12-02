"""Integration tests for TAP queries against NASA endpoint."""

import pytest
from src.tools.tap_query import run_tap_query, build_query


@pytest.mark.integration
class TestTapQueryIntegration:
    """Integration tests for TAP queries."""

    def test_simple_query(self):
        """Test simple query execution."""
        query = "SELECT pl_name, pl_rade FROM pscomppars WHERE pl_rade IS NOT NULL ORDER BY pl_rade LIMIT 5"
        result = run_tap_query(query)
        assert result["success"] is True
        assert result["row_count"] == 5
        assert len(result["data"]) == 5
        assert "pl_name" in result["data"][0]

    def test_count_query(self):
        """Test count query."""
        query = "SELECT COUNT(*) as count FROM pscomppars WHERE pl_rade IS NOT NULL"
        result = run_tap_query(query)
        assert result["success"] is True
        assert result["row_count"] == 1
        assert "count" in result["data"][0]
        assert result["data"][0]["count"] > 0

    def test_discovery_method_grouping(self):
        """Test GROUP BY query."""
        query = """SELECT pl_discmethod, COUNT(*) as count
                   FROM pscomppars
                   WHERE pl_discmethod IS NOT NULL
                   GROUP BY pl_discmethod
                   ORDER BY count DESC
                   LIMIT 5"""
        result = run_tap_query(query)
        assert result["success"] is True
        assert len(result["data"]) > 0
        assert "pl_discmethod" in result["data"][0]
        assert "count" in result["data"][0]

    def test_invalid_column_error(self):
        """Test error on invalid column."""
        query = "SELECT invalid_column FROM pscomppars LIMIT 1"
        result = run_tap_query(query)
        assert result["success"] is False
        assert "error" in result


@pytest.mark.integration
class TestBuildQuery:
    """Test query builder."""

    def test_build_simple_query(self):
        """Test building simple query."""
        query = build_query(
            columns=["pl_name", "pl_rade"],
            table="pscomppars",
            limit=10
        )
        assert "SELECT pl_name, pl_rade" in query
        assert "FROM pscomppars" in query
        assert "LIMIT 10" in query

    def test_build_query_with_where(self):
        """Test building query with WHERE clause."""
        query = build_query(
            columns=["pl_name"],
            where="pl_rade > 1",
            limit=10
        )
        assert "WHERE pl_rade > 1" in query

    def test_build_query_with_order(self):
        """Test building query with ORDER BY."""
        query = build_query(
            columns=["pl_name", "pl_rade"],
            order_by="pl_rade DESC",
            limit=10
        )
        assert "ORDER BY pl_rade DESC" in query

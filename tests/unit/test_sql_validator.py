"""Tests for SQL validator."""

import pytest
from src.tools.sql_validator import validate_sql, _extract_columns


class TestSqlValidation:
    """Test SQL validation rules."""

    def test_valid_select_query(self):
        """Test valid SELECT query passes."""
        query = "SELECT pl_name, pl_rade FROM pscomppars WHERE pl_rade > 1 LIMIT 100"
        result = validate_sql(query)
        assert result["valid"] is True
        assert len(result["errors"]) == 0

    def test_select_star_rejected(self):
        """Test SELECT * is rejected."""
        query = "SELECT * FROM pscomppars LIMIT 100"
        result = validate_sql(query)
        assert result["valid"] is False
        assert any("SELECT *" in e for e in result["errors"])

    def test_insert_rejected(self):
        """Test INSERT is rejected."""
        query = "INSERT INTO pscomppars VALUES (1, 2)"
        result = validate_sql(query)
        assert result["valid"] is False
        assert any("INSERT" in e for e in result["errors"])

    def test_delete_rejected(self):
        """Test DELETE is rejected."""
        query = "DELETE FROM pscomppars"
        result = validate_sql(query)
        assert result["valid"] is False
        assert any("DELETE" in e for e in result["errors"])

    def test_drop_rejected(self):
        """Test DROP is rejected."""
        query = "DROP TABLE pscomppars"
        result = validate_sql(query)
        assert result["valid"] is False
        assert any("DROP" in e for e in result["errors"])

    def test_semicolon_warning(self):
        """Test semicolon produces warning."""
        query = "SELECT pl_name FROM pscomppars LIMIT 10;"
        result = validate_sql(query)
        assert any("semicolon" in w.lower() for w in result["warnings"])

    def test_no_limit_warning(self):
        """Test missing LIMIT produces warning."""
        query = "SELECT pl_name FROM pscomppars"
        result = validate_sql(query)
        assert any("LIMIT" in w for w in result["warnings"])

    def test_invalid_column_error(self):
        """Test invalid column produces error."""
        query = "SELECT invalid_column FROM pscomppars LIMIT 10"
        result = validate_sql(query)
        assert result["valid"] is False
        assert any("invalid_column" in e.lower() for e in result["errors"])


class TestColumnExtraction:
    """Test column extraction from queries."""

    def test_simple_columns(self):
        """Test extracting simple column names."""
        query = "SELECT pl_name, pl_rade FROM pscomppars"
        columns = _extract_columns(query)
        assert "pl_name" in columns
        assert "pl_rade" in columns

    def test_aggregate_function(self):
        """Test extracting column from aggregate."""
        query = "SELECT COUNT(pl_name) FROM pscomppars"
        columns = _extract_columns(query)
        assert "pl_name" in columns

    def test_count_star(self):
        """Test COUNT(*) doesn't produce columns."""
        query = "SELECT COUNT(*) as count FROM pscomppars"
        columns = _extract_columns(query)
        # COUNT(*) should not add any column
        assert "count" not in columns or len(columns) == 0

    def test_alias(self):
        """Test column with alias."""
        query = "SELECT pl_name AS name, pl_rade AS radius FROM pscomppars"
        columns = _extract_columns(query)
        assert "pl_name" in columns
        assert "pl_rade" in columns
        assert "name" not in columns
        assert "radius" not in columns

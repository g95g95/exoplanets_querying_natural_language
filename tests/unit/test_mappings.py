"""Tests for astronomical concept mappings."""

import pytest
from src.mappings.concepts import (
    CONCEPT_MAPPINGS,
    get_sql_condition,
    normalize_concept,
    get_required_columns
)


class TestConceptMappings:
    """Test concept mapping definitions."""

    def test_earth_sized_mapping(self):
        """Test Earth-sized planet mapping."""
        mapping = get_sql_condition("earth-sized")
        assert mapping is not None
        assert "pl_rade" in mapping["columns"]
        assert "0.8" in mapping["condition"]
        assert "1.25" in mapping["condition"]

    def test_super_earth_mapping(self):
        """Test Super-Earth mapping."""
        mapping = get_sql_condition("super-earth")
        assert mapping is not None
        assert "pl_rade" in mapping["columns"]
        assert "1.25" in mapping["condition"]
        assert "2.0" in mapping["condition"]

    def test_hot_jupiter_mapping(self):
        """Test Hot Jupiter mapping."""
        mapping = get_sql_condition("hot-jupiter")
        assert mapping is not None
        assert "pl_rade" in mapping["columns"]
        assert "pl_orbper" in mapping["columns"]

    def test_habitable_zone_mapping(self):
        """Test habitable zone mapping."""
        mapping = get_sql_condition("habitable-zone")
        assert mapping is not None
        assert "pl_eqt" in mapping["columns"]
        assert "200" in mapping["condition"]
        assert "320" in mapping["condition"]

    def test_transiting_mapping(self):
        """Test transiting planets mapping."""
        mapping = get_sql_condition("transiting")
        assert mapping is not None
        assert "pl_tranflag = 1" in mapping["condition"]

    def test_unknown_concept_returns_none(self):
        """Test that unknown concepts return None."""
        result = get_sql_condition("unknown-concept")
        assert result is None


class TestConceptAliases:
    """Test concept alias normalization."""

    def test_normalize_with_spaces(self):
        """Test normalizing concepts with spaces."""
        assert normalize_concept("earth sized") == "earth-sized"
        assert normalize_concept("hot jupiter") == "hot-jupiter"
        assert normalize_concept("super earth") == "super-earth"

    def test_normalize_without_separators(self):
        """Test normalizing concepts without separators."""
        assert normalize_concept("earthsized") == "earth-sized"
        assert normalize_concept("hotjupiter") == "hot-jupiter"

    def test_normalize_case_insensitive(self):
        """Test case insensitivity."""
        assert normalize_concept("Earth-Sized") == "earth-sized"
        assert normalize_concept("HOT JUPITER") == "hot-jupiter"

    def test_normalize_already_normalized(self):
        """Test that normalized concepts stay normalized."""
        assert normalize_concept("earth-sized") == "earth-sized"
        assert normalize_concept("hot-jupiter") == "hot-jupiter"


class TestGetRequiredColumns:
    """Test getting required columns for concepts."""

    def test_single_concept(self):
        """Test columns for single concept."""
        columns = get_required_columns(["earth-sized"])
        assert "pl_rade" in columns

    def test_multiple_concepts(self):
        """Test columns for multiple concepts."""
        columns = get_required_columns(["hot-jupiter", "habitable-zone"])
        assert "pl_rade" in columns
        assert "pl_orbper" in columns
        assert "pl_eqt" in columns

    def test_empty_list(self):
        """Test empty concept list."""
        columns = get_required_columns([])
        assert columns == []

    def test_unknown_concepts_ignored(self):
        """Test that unknown concepts are ignored."""
        columns = get_required_columns(["unknown", "earth-sized"])
        assert "pl_rade" in columns
        assert len(columns) == 1

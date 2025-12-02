"""Astronomical concept to SQL condition mappings.

Maps qualitative terms to quantitative thresholds based on CLAUDE.md specifications.
"""

from typing import Dict, List, Optional

# Concept mappings: concept_name -> (columns_needed, sql_condition)
CONCEPT_MAPPINGS: Dict[str, Dict] = {
    # Planet size categories
    "earth-sized": {
        "columns": ["pl_rade"],
        "condition": "pl_rade >= 0.8 AND pl_rade <= 1.25",
        "description": "Planets with radius 0.8-1.25 Earth radii"
    },
    "earth-like": {
        "columns": ["pl_rade", "pl_bmasse"],
        "condition": "pl_rade >= 0.8 AND pl_rade <= 1.5 AND pl_bmasse <= 2",
        "description": "Planets with Earth-like radius and mass"
    },
    "super-earth": {
        "columns": ["pl_rade"],
        "condition": "pl_rade > 1.25 AND pl_rade <= 2.0",
        "description": "Planets with radius 1.25-2.0 Earth radii"
    },
    "mini-neptune": {
        "columns": ["pl_rade"],
        "condition": "pl_rade > 2.0 AND pl_rade <= 4.0",
        "description": "Planets with radius 2.0-4.0 Earth radii"
    },
    "neptune-sized": {
        "columns": ["pl_rade"],
        "condition": "pl_rade >= 3.0 AND pl_rade <= 6.0",
        "description": "Planets with radius 3.0-6.0 Earth radii"
    },
    "jupiter-sized": {
        "columns": ["pl_rade"],
        "condition": "pl_rade >= 9.0 AND pl_rade <= 13.0",
        "description": "Planets with radius 9.0-13.0 Earth radii"
    },

    # Jupiter temperature categories
    "hot-jupiter": {
        "columns": ["pl_rade", "pl_orbper"],
        "condition": "pl_rade >= 9.0 AND pl_orbper < 10",
        "description": "Large planets with very short orbital periods"
    },
    "warm-jupiter": {
        "columns": ["pl_rade", "pl_orbper"],
        "condition": "pl_rade >= 9.0 AND pl_orbper >= 10 AND pl_orbper <= 100",
        "description": "Large planets with moderate orbital periods"
    },
    "cold-jupiter": {
        "columns": ["pl_rade", "pl_orbper"],
        "condition": "pl_rade >= 9.0 AND pl_orbper > 100",
        "description": "Large planets with long orbital periods"
    },

    # Orbital characteristics
    "close-in": {
        "columns": ["pl_orbper"],
        "condition": "pl_orbper < 1",
        "description": "Planets with orbital period less than 1 day"
    },
    "ultra-short-period": {
        "columns": ["pl_orbper"],
        "condition": "pl_orbper < 1",
        "description": "Planets with orbital period less than 1 day"
    },

    # Habitability
    "habitable-zone": {
        "columns": ["pl_eqt"],
        "condition": "pl_eqt >= 200 AND pl_eqt <= 320",
        "description": "Planets with equilibrium temperature 200-320 K"
    },
    "habitable": {
        "columns": ["pl_eqt"],
        "condition": "pl_eqt >= 200 AND pl_eqt <= 320",
        "description": "Planets in approximate habitable zone"
    },

    # Observation characteristics
    "transiting": {
        "columns": ["pl_tranflag"],
        "condition": "pl_tranflag = 1",
        "description": "Planets that transit their host star"
    },

    # System characteristics
    "multi-planet": {
        "columns": ["sy_pnum"],
        "condition": "sy_pnum >= 2",
        "description": "Systems with 2 or more planets"
    },
    "multi-planet-system": {
        "columns": ["sy_pnum"],
        "condition": "sy_pnum >= 2",
        "description": "Systems with 2 or more planets"
    },

    # Distance
    "nearby": {
        "columns": ["st_dist"],
        "condition": "st_dist <= 30",
        "description": "Stars within 30 parsecs"
    },
    "close": {
        "columns": ["st_dist"],
        "condition": "st_dist <= 30",
        "description": "Stars within 30 parsecs"
    },
}

# Aliases for common variations
CONCEPT_ALIASES: Dict[str, str] = {
    "earth sized": "earth-sized",
    "earthsized": "earth-sized",
    "earth like": "earth-like",
    "earthlike": "earth-like",
    "super earth": "super-earth",
    "superearth": "super-earth",
    "mini neptune": "mini-neptune",
    "minineptune": "mini-neptune",
    "neptune sized": "neptune-sized",
    "neptunesized": "neptune-sized",
    "jupiter sized": "jupiter-sized",
    "jupitersized": "jupiter-sized",
    "hot jupiter": "hot-jupiter",
    "hotjupiter": "hot-jupiter",
    "warm jupiter": "warm-jupiter",
    "warmjupiter": "warm-jupiter",
    "cold jupiter": "cold-jupiter",
    "coldjupiter": "cold-jupiter",
    "ultra short period": "ultra-short-period",
    "ultrashortperiod": "ultra-short-period",
    "habitable zone": "habitable-zone",
    "habitablezone": "habitable-zone",
    "multi planet": "multi-planet",
    "multiplanet": "multi-planet",
}


def normalize_concept(concept: str) -> str:
    """Normalize a concept name to its canonical form."""
    normalized = concept.lower().strip()
    return CONCEPT_ALIASES.get(normalized, normalized)


def get_sql_condition(concept: str) -> Optional[Dict]:
    """Get SQL condition for a concept.

    Args:
        concept: The astronomical concept (e.g., "earth-sized", "hot jupiter")

    Returns:
        Dict with 'columns' and 'condition' keys, or None if not found
    """
    normalized = normalize_concept(concept)
    return CONCEPT_MAPPINGS.get(normalized)


def get_required_columns(concepts: List[str]) -> List[str]:
    """Get all columns required for a list of concepts.

    Args:
        concepts: List of concept names

    Returns:
        List of unique column names
    """
    columns = set()
    for concept in concepts:
        mapping = get_sql_condition(concept)
        if mapping:
            columns.update(mapping["columns"])
    return list(columns)

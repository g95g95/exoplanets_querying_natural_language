"""Conversation state management for the Exoplanet Agent."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any


@dataclass
class ConversationState:
    """Maintains state across conversation turns."""

    last_sql: Optional[str] = None
    last_visualization: Optional[Dict[str, Any]] = None
    active_filters: Dict[str, str] = field(default_factory=dict)
    selected_columns: List[str] = field(default_factory=list)
    table: str = "pscomppars"
    history: List[Dict[str, Any]] = field(default_factory=list)

    def update(
        self,
        sql: Optional[str] = None,
        visualization: Optional[Dict[str, Any]] = None,
        filters: Optional[Dict[str, str]] = None,
        columns: Optional[List[str]] = None
    ):
        """Update state with new values.

        Args:
            sql: New SQL query
            visualization: New visualization spec
            filters: New or updated filters
            columns: New selected columns
        """
        if sql:
            self.last_sql = sql

        if visualization:
            self.last_visualization = visualization

        if filters:
            self.active_filters.update(filters)

        if columns:
            self.selected_columns = columns

        # Add to history
        self.history.append({
            "sql": sql,
            "visualization": visualization
        })

    def get_context(self) -> str:
        """Get context string for prompt.

        Returns:
            Formatted context string
        """
        if not self.last_sql:
            return ""

        filters_str = ", ".join(f"{k}={v}" for k, v in self.active_filters.items())
        columns_str = ", ".join(self.selected_columns)

        return f"""Previous query: {self.last_sql}
Active filters: {filters_str or 'none'}
Selected columns: {columns_str or 'none'}"""

    def clear(self):
        """Clear all state."""
        self.last_sql = None
        self.last_visualization = None
        self.active_filters = {}
        self.selected_columns = []
        self.history = []

    def add_filter(self, name: str, condition: str):
        """Add or update a filter.

        Args:
            name: Filter name/key
            condition: SQL condition
        """
        self.active_filters[name] = condition

    def remove_filter(self, name: str):
        """Remove a filter.

        Args:
            name: Filter name/key
        """
        self.active_filters.pop(name, None)

    def get_combined_where(self) -> Optional[str]:
        """Get combined WHERE clause from active filters.

        Returns:
            Combined WHERE clause or None if no filters
        """
        if not self.active_filters:
            return None
        return " AND ".join(self.active_filters.values())

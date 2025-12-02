"""Main agent for translating questions to TAP queries."""

import json
import re
from typing import Dict, Any, Optional

from ..config import LLM_PROVIDER, LLM_MODEL, OPENAI_API_KEY, ANTHROPIC_API_KEY
from ..tools.tap_query import run_tap_query
from ..tools.sql_validator import validate_sql
from ..viz.spec_builder import VisualizationSpec, build_visualization, get_column_label
from .prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
from .state import ConversationState


class ExoplanetAgent:
    """Agent that translates natural language to TAP queries."""

    def __init__(self):
        """Initialize the agent."""
        self.state = ConversationState()
        self._llm_client = None

    def _get_llm_client(self):
        """Get or create LLM client."""
        if self._llm_client is not None:
            return self._llm_client

        if LLM_PROVIDER == "openai":
            from openai import OpenAI
            self._llm_client = OpenAI(api_key=OPENAI_API_KEY)
        elif LLM_PROVIDER == "anthropic":
            from anthropic import Anthropic
            self._llm_client = Anthropic(api_key=ANTHROPIC_API_KEY)
        else:
            raise ValueError(f"Unknown LLM provider: {LLM_PROVIDER}")

        return self._llm_client

    def _call_llm(self, user_message: str) -> str:
        """Call the LLM with a message.

        Args:
            user_message: The user's question with context

        Returns:
            LLM response text
        """
        client = self._get_llm_client()

        if LLM_PROVIDER == "openai":
            response = client.chat.completions.create(
                model=LLM_MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            return response.choices[0].message.content

        elif LLM_PROVIDER == "anthropic":
            response = client.messages.create(
                model=LLM_MODEL,
                max_tokens=4096,
                system=SYSTEM_PROMPT,
                messages=[
                    {"role": "user", "content": user_message}
                ]
            )
            return response.content[0].text

        raise ValueError(f"Unknown LLM provider: {LLM_PROVIDER}")

    def _parse_llm_response(self, response: str) -> Dict[str, Any]:
        """Parse LLM response to extract SQL and visualization spec.

        Args:
            response: Raw LLM response

        Returns:
            Parsed dict with 'sql' and 'visualization' keys
        """
        # Try to parse as JSON directly
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            pass

        # Try to extract JSON from markdown code block
        json_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass

        # Last resort: try to find any JSON object
        json_match = re.search(r"\{.*\}", response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(0))
            except json.JSONDecodeError:
                pass

        raise ValueError(f"Could not parse LLM response as JSON: {response[:200]}")

    def ask(self, question: str) -> Dict[str, Any]:
        """Process a user question and return visualization spec with data.

        Args:
            question: Natural language question about exoplanets

        Returns:
            Dict with visualization spec and data
        """
        print(f"[AGENT] Processing question: {question}")

        # Build prompt with context
        context = self.state.get_context()
        user_message = USER_PROMPT_TEMPLATE.format(
            question=question,
            context=context if context else "No previous context."
        )

        # Call LLM
        print(f"[AGENT] Calling LLM provider: {LLM_PROVIDER}, model: {LLM_MODEL}")
        print(f"[AGENT] API Key configured: {'Yes' if (OPENAI_API_KEY or ANTHROPIC_API_KEY) else 'NO - MISSING!'}")
        llm_response = self._call_llm(user_message)
        print(f"[AGENT] LLM response received, length: {len(llm_response)}")
        parsed = self._parse_llm_response(llm_response)
        print(f"[AGENT] Parsed response - SQL: {parsed.get('sql', 'N/A')[:100]}...")

        sql = parsed.get("sql", "")
        viz_spec = parsed.get("visualization", {})

        # Validate SQL
        validation = validate_sql(sql)
        if not validation["valid"]:
            return {
                "success": False,
                "error": f"Invalid SQL: {validation['errors']}",
                "sql": sql,
                "visualization": None
            }

        # Execute query
        result = run_tap_query(validation["query"])

        if not result["success"]:
            return {
                "success": False,
                "error": result["error"],
                "sql": sql,
                "visualization": None
            }

        # Build visualization
        visualization = build_visualization(
            viz_type=viz_spec.get("type", "table"),
            title=viz_spec.get("title", "Query Results"),
            description=viz_spec.get("description", ""),
            data=result["data"],
            x_field=viz_spec.get("x_field"),
            y_field=viz_spec.get("y_field"),
            color_field=viz_spec.get("color_field"),
            size_field=viz_spec.get("size_field"),
            x_label=viz_spec.get("x_label"),
            y_label=viz_spec.get("y_label"),
            x_scale=viz_spec.get("x_scale", "linear"),
            y_scale=viz_spec.get("y_scale", "linear")
        )

        # Update state
        self.state.update(
            sql=sql,
            visualization=visualization.to_dict()
        )

        return {
            "success": True,
            "sql": sql,
            "row_count": result["row_count"],
            **visualization.to_dict()
        }

    def clear_state(self):
        """Clear conversation state."""
        self.state.clear()

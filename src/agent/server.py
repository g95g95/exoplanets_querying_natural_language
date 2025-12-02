"""FastAPI server for the Exoplanet Agent."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any

from .agent import ExoplanetAgent
from ..config import HOST, PORT, DEBUG

app = FastAPI(
    title="Exoplanet Data Analyst API",
    description="AI-powered natural language interface to the NASA Exoplanet Archive",
    version="1.0.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Session storage for agents
sessions: Dict[str, ExoplanetAgent] = {}


class QuestionRequest(BaseModel):
    """Request model for asking questions."""
    question: str
    session_id: Optional[str] = "default"


class QuestionResponse(BaseModel):
    """Response model for question answers."""
    success: bool
    sql: Optional[str] = None
    row_count: Optional[int] = None
    error: Optional[str] = None
    visualization: Optional[Dict[str, Any]] = None
    cached: Optional[bool] = False


def get_agent(session_id: str) -> ExoplanetAgent:
    """Get or create an agent for a session.

    Args:
        session_id: Session identifier

    Returns:
        ExoplanetAgent instance
    """
    if session_id not in sessions:
        sessions[session_id] = ExoplanetAgent()
    return sessions[session_id]


@app.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest) -> QuestionResponse:
    """Process a natural language question about exoplanets.

    Args:
        request: Question request with session_id

    Returns:
        Query results with visualization spec
    """
    print(f"[LOG] Received question: {request.question}")
    print(f"[LOG] Session ID: {request.session_id}")
    try:
        agent = get_agent(request.session_id)
        print("[LOG] Agent created/retrieved successfully")
        result = agent.ask(request.question)
        print(f"[LOG] Result: success={result.get('success')}, rows={result.get('row_count')}")
        return QuestionResponse(**result)
    except Exception as e:
        import traceback
        print(f"[ERROR] Exception occurred: {str(e)}")
        print(f"[ERROR] Traceback:\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/clear/{session_id}")
async def clear_session(session_id: str):
    """Clear conversation state for a session.

    Args:
        session_id: Session identifier
    """
    if session_id in sessions:
        sessions[session_id].clear_state()
    return {"status": "cleared"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/schema/{table}")
async def get_schema(table: str = "pscomppars"):
    """Get schema information for a table.

    Args:
        table: Table name

    Returns:
        Schema information
    """
    from ..tools.schema import get_exoplanet_schema
    try:
        schema = get_exoplanet_schema(table)
        return schema
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/cache/stats")
async def cache_stats():
    """Get cache statistics."""
    from ..tools.cache import get_cache_stats
    return get_cache_stats()


@app.post("/cache/clear")
async def cache_clear():
    """Clear all cached queries."""
    from ..tools.cache import clear_cache
    clear_cache()
    return {"status": "cache cleared"}


def main():
    """Run the server."""
    import uvicorn
    uvicorn.run(
        "src.agent.server:app",
        host=HOST,
        port=PORT,
        reload=DEBUG
    )


if __name__ == "__main__":
    main()

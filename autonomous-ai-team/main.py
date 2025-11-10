"""
Main entry point for the Autonomous AI Team system.
Run with: uvicorn main:app --reload
"""

from src.api.routes import app

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

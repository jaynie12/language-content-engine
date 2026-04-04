"""
French Learning App - FastAPI Backend
Main entry point for the application.
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from database import init_db

# Configure logging
logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    logger.info("Starting French Learning App...")
    init_db()  # Create tables if they don't exist
    yield
    # Shutdown
    logger.info("Shutting down French Learning App...")


# Create FastAPI app
app = FastAPI(
    title="French Learning App API",
    description="Extract key vocabulary from French YouTube videos",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routes placeholder (will be expanded)
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "version": "0.1.0",
        "environment": settings.environment,
    }


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "French Learning App API",
        "docs": "/docs",
        "version": "0.1.0",
    }


# Placeholder for analyze route (to be implemented)
@app.post("/api/analyze", tags=["Analysis"])
async def analyze_video(request: dict):
    """Analyze a YouTube video - placeholder"""
    return {"message": "Analyze endpoint - coming soon"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level=settings.log_level.lower(),
    )

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import logging
from app.database import engine, Base, get_db
from app.routers import analyze, history

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="AI Spam Detector API",
    description="Detect spam messages using Hugging Face transformers",
    version="1.0.0"
)

# Include routers
app.include_router(analyze.router)
app.include_router(history.router)

@app.get("/health", tags=["Health"])
async def health_check(db: Session = Depends(get_db)):
    """
    Check if the service is healthy
    """
    try:
        # Test database connection
        db.execute("SELECT 1")
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed")

@app.on_event("startup")
async def startup_event():
    logger.info("=" * 50)
    logger.info("AI Spam Detector API Started")
    logger.info("=" * 50)

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down AI Spam Detector API")

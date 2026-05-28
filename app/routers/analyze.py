from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import logging
from app.schemas import AnalyzeRequest, AnalyzeResponse
from app.database import get_db
from app.models import RequestHistory
from app.ml_service import spam_detector

router = APIRouter(prefix="/analyze", tags=["Analysis"])
logger = logging.getLogger(__name__)

@router.post("", response_model=AnalyzeResponse)
async def analyze_text(request: AnalyzeRequest, db: Session = Depends(get_db)):
    """
    Analyze text for spam detection
    """
    logger.info(f"Received request with text length: {len(request.text)}")

    # Validate text is not empty
    if not request.text or not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    try:
        # Get prediction from model
        prediction = spam_detector.predict(request.text)

        # Save to database
        db_record = RequestHistory(
            input_text=request.text,
            result_text=prediction["result"],
            score=str(prediction["score"]),
            model_name=prediction["model_name"]
        )

        db.add(db_record)
        db.commit()
        db.refresh(db_record)

        logger.info(f"Saved request with id: {db_record.id}")

        return AnalyzeResponse(
            result=prediction["result"],
            score=prediction["score"],
            model_name=prediction["model_name"]
        )

    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

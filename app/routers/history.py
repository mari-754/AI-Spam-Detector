from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import logging
from app.schemas import HistoryResponse
from app.database import get_db
from app.models import RequestHistory

router = APIRouter(prefix="/history", tags=["History"])
logger = logging.getLogger(__name__)

@router.get("", response_model=List[HistoryResponse])
async def get_history(limit: int = 20, db: Session = Depends(get_db)):
    """
    Get last 20 requests (or custom limit)
    """
    logger.info(f"Fetching last {limit} requests")

    try:
        history = db.query(RequestHistory).order_by(
            RequestHistory.created_at.desc()
        ).limit(limit).all()

        return history
    except Exception as e:
        logger.error(f"Error fetching history: {e}")
        raise HTTPException(status_code=500, detail="Database error")

@router.get("/{request_id}", response_model=HistoryResponse)
async def get_request_by_id(request_id: int, db: Session = Depends(get_db)):
    """
    Get specific request by ID
    """
    logger.info(f"Fetching request with id: {request_id}")

    try:
        request = db.query(RequestHistory).filter(RequestHistory.id == request_id).first()

        if not request:
            raise HTTPException(status_code=404, detail=f"Request with id {request_id} not found")

        return request
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching request: {e}")
        raise HTTPException(status_code=500, detail="Database error")

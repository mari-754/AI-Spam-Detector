from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class AnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=1000, description="Text to analyze")

    class Config:
        json_schema_extra = {
            "example": {
                "text": "Congratulations! You won a free iPhone. Click here to claim!"
            }
        }

class AnalyzeResponse(BaseModel):
    result: str  # "SPAM" or "NOT SPAM"
    score: float
    model_name: str

class HistoryResponse(BaseModel):
    id: int
    input_text: str
    result_text: str
    score: Optional[str] = None
    model_name: str
    created_at: datetime

class HealthResponse(BaseModel):
    status: str

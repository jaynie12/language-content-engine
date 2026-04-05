from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class AnalyzeRequest(BaseModel):
    """Request to analyze a YouTube video"""
    url: str = Field(..., description="YouTube video URL")
class SaveVocabularyRequest(BaseModel):
    """Request to save a word to user's list"""
    video_id: int
    vocabulary_id: int
class ExportVocabularyRequest(BaseModel):
    """Request to export vocabulary"""
    format: str = Field(..., description="'anki' or 'csv'")
    filters: Optional[dict] = None 
class VocabularyItemSchema(BaseModel):
    """Single vocabulary item"""
    id: int
    word: str
    translation: str
    cefr_level: str
    frequency: Optional[str] = None
    example_sentence: Optional[str] = None
    class Config: #Pydantic automatically converts the SQLAlchemy object's attributes into the Pydantic model's fields
        from_attributes = True
class VideoAnalysisResponse(BaseModel):
    """Response from video analysis"""
    video_id: int
    youtube_id: str
    title: str
    cefr_level: str
    confidence: float
    topics: List[str]
    vocabulary: List[VocabularyItemSchema]
    analyzed_at: datetime
    class Config:
        from_attributes = True
class VideoSummarySchema(BaseModel):
    """Summary of a video (for list views)"""
    id: int
    youtube_id: str
    title: str
    cefr_level: str
    created_at: datetime
    class Config:
        from_attributes = True

class SavedVocabularySchema(BaseModel):
    """User's saved vocabulary item"""
    id: int
    word: str
    translation: str
    cefr_level: str
    example_sentence: Optional[str] = None
    video_title: str
    saved_at: datetime
    
    class Config:
        from_attributes = True


class ErrorResponse(BaseModel):
    """Standard error response"""
    error: str
    detail: Optional[str] = None
    code: Optional[str] = None


class HealthCheckResponse(BaseModel):
    """Health check response"""
    status: str
    version: str = "0.1.0"

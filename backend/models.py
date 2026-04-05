from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class User(Base):
    """Single user for MVP (no auth yet, just placeholder)"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    videos = relationship("Video", back_populates="user")
    saved_vocabulary = relationship("UserVocabulary", back_populates="user")


class Video(Base):
    """Analyzed YouTube videos"""
    __tablename__ = "videos"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    youtube_id = Column(String(255), unique=True, nullable=False)
    title = Column(String(500), nullable=False)
    transcript = Column(Text, nullable=False)
    cefr_level = Column(String(3), nullable=True)  # A1, A2, B1, B2, C1, C2
    confidence = Column(Float, nullable=True)  # 0.0 - 1.0
    topics = Column(JSON, nullable=True)  # List of strings
    analyzed_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="videos")
    vocabulary_items = relationship("VocabularyItem", back_populates="video", cascade="all, delete-orphan")


class VocabularyItem(Base):
    """20 key words extracted from each video"""
    __tablename__ = "vocabulary_items"
    
    id = Column(Integer, primary_key=True)
    video_id = Column(Integer, ForeignKey("videos.id"), nullable=False)
    word = Column(String(255), nullable=False)
    translation = Column(String(255), nullable=False)
    cefr_level = Column(String(3), nullable=False)  # A1, A2, B1, B2, C1, C2
    frequency = Column(String(50), nullable=True)  # "common", "uncommon", etc
    example_sentence = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    video = relationship("Video", back_populates="vocabulary_items")
    user_items = relationship("UserVocabulary", back_populates="vocabulary_item", cascade="all, delete-orphan")


class UserVocabulary(Base):
    """User's saved vocabulary (personal list)"""
    __tablename__ = "user_vocabulary"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    vocabulary_id = Column(Integer, ForeignKey("vocabulary_items.id"), nullable=False)
    in_anki = Column(Boolean, default=False)
    saved_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="saved_vocabulary")
    vocabulary_item = relationship("VocabularyItem", back_populates="user_items")

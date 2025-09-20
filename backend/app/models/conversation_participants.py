"""
ConversationParticipant model for database storage - Participants in conversations
"""

from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class ConversationParticipant(Base):
    """
    ConversationParticipant model - Association table between conversations and participants
    """
    __tablename__ = "conversation_participants"
    
    # Composite primary key
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="CASCADE"), primary_key=True)
    participant_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    
    joined_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    conversation = relationship("Conversation", back_populates="participants")
    participant = relationship("User", back_populates="conversation_participations")

    def __repr__(self):
        return f"<ConversationParticipant(conversation_id='{self.conversation_id}', participant_id='{self.participant_id}')>"
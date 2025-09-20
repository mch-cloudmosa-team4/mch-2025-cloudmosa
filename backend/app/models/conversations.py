"""
Conversation model for database storage - Conversations between users
"""

from datetime import datetime
from typing import Optional
import uuid
from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Conversation(Base):
    """
    Conversation model for storing conversations between two users
    """
    __tablename__ = "conversations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    last_message_at = Column(DateTime(timezone=True), nullable=True)  # Timestamp of the last message in this conversation
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    participants = relationship("ConversationParticipant", back_populates="conversation", cascade="all, delete-orphan")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan", order_by="Message.sent_at")

    def __repr__(self):
        participant_count = len(self.participants) if self.participants else 0
        return f"<Conversation(id='{self.id}', participants={participant_count})>"

    def get_other_participant(self, user_id):
        """
        Get the other participant in the conversation given one user's ID
        (For conversations with exactly 2 participants)
        """
        if not self.participants or len(self.participants) != 2:
            return None
            
        participant_ids = [p.participant_id for p in self.participants]
        if user_id not in participant_ids:
            return None
            
        other_id = [pid for pid in participant_ids if pid != user_id][0]
        return next((p.participant for p in self.participants if p.participant_id == other_id), None)
            
    def has_participant(self, user_id):
        """
        Check if a user is a participant in this conversation
        """
        if not self.participants:
            return False
        return any(p.participant_id == user_id for p in self.participants)
        
    def get_participant_users(self):
        """
        Get all participant User objects
        """
        return [p.participant for p in self.participants] if self.participants else []
"""
Message model for database storage - Chat messages in conversations
"""

from datetime import datetime
from typing import Optional
import uuid
import enum
from sqlalchemy import Column, Text, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class MessageType(enum.Enum):
    """
    Message type enumeration
    """
    TEXT = "text"    # 純文本消息
    IMAGE = "img"    # 圖片消息
    FILE = "file"    # 文件消息


class Message(Base):
    """
    Message model for storing chat messages in conversations
    """
    __tablename__ = "messages"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False, index=True)
    sender_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    message_type = Column(Enum(MessageType), nullable=False)
    content = Column(Text, nullable=True)  # Text content for text messages, description/caption for media
    file_id = Column(UUID(as_uuid=True), ForeignKey("files.id", ondelete="SET NULL"), nullable=True, index=True)
    sent_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # Relationships
    conversation = relationship("Conversation", back_populates="messages")
    sender = relationship("User", back_populates="sent_messages")
    file = relationship("File", back_populates="messages")

    def __repr__(self):
        return f"<Message(id='{self.id}', conversation_id='{self.conversation_id}', sender_id='{self.sender_id}', type='{self.message_type.value}')>"
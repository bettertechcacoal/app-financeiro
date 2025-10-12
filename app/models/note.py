# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.database import Base
import enum


class NoteColor(enum.Enum):
    YELLOW = "yellow"
    PINK = "pink"
    GREEN = "green"
    BLUE = "blue"
    PURPLE = "purple"


class Note(Base):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    color = Column(Enum(NoteColor), default=NoteColor.YELLOW, nullable=False)
    icon = Column(String(50), default='fa-sticky-note')
    label = Column(String(50))  # Ex: "Hoje", "Urgente", "Amanhã"
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationship
    user = relationship('User', backref='notes')

    def __repr__(self):
        return f"<Note {self.title}>"

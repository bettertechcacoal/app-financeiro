# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Table
from sqlalchemy.sql import func
from app.models.database import Base


# Tabela pivot para relacionamento muitos-para-muitos entre users e groups
user_groups = Table(
    'user_groups',
    Base.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
    Column('group_id', Integer, ForeignKey('groups.id', ondelete='CASCADE'), nullable=False),
    Column('created_at', DateTime(timezone=True), server_default=func.now(), nullable=False)
)

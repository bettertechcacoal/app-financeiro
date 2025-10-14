# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Table
from sqlalchemy.sql import func
from app.models.database import Base


# Tabela pivot para relacionamento muitos-para-muitos entre groups e permissions
group_permissions = Table(
    'group_permissions',
    Base.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('group_id', Integer, ForeignKey('groups.id', ondelete='CASCADE'), nullable=False),
    Column('permission_id', Integer, ForeignKey('permissions.id', ondelete='CASCADE'), nullable=False),
    Column('created_at', DateTime(timezone=True), server_default=func.now(), nullable=False)
)

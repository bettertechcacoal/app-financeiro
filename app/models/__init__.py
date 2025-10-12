# -*- coding: utf-8 -*-

# Importar todos os modelos para que o SQLAlchemy os registre corretamente
from app.models.database import Base
from app.models.user import User
from app.models.organization import Organization
from app.models.client import Client
from app.models.ticket import Ticket
from app.models.state import State
from app.models.city import City
from app.models.travel import Travel
from app.models.travel_passenger import TravelPassenger

__all__ = [
    'Base',
    'User',
    'Organization',
    'Client',
    'Ticket',
    'State',
    'City',
    'Travel',
    'TravelPassenger'
]

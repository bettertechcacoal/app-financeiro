# -*- coding: utf-8 -*-

# Importar todos os modelos para que o SQLAlchemy os registre corretamente
from app.models.database import Base
from app.models.group import Group
from app.models.user_group import user_groups
from app.models.user import User
from app.models.organization import Organization
from app.models.client import Client
from app.models.ticket import Ticket
from app.models.state import State
from app.models.city import City
from app.models.travel import Travel
from app.models.travel_passenger import TravelPassenger
from app.models.travel_payout import TravelPayout
from app.models.vehicle_travel_history import VehicleTravelHistory
from app.models.notification import Notification
from app.models.parameter_group import ParameterGroup
from app.models.parameter import Parameter
from app.models.note import Note
from app.models.application import Application
from app.models.client_application import ClientApplication
from app.models.permission import Permission
from app.models.group_permission import group_permissions
from app.models.vehicle import Vehicle
from app.models.maintenance_type import MaintenanceType
from app.models.vehicle_km_log import VehicleKmLog
from app.models.vehicle_issue import VehicleIssue
from app.models.vehicle_maintenance_history import VehicleMaintenanceHistory
from app.models.vehicle_maintenance_config import VehicleMaintenanceConfig
from app.models.travel_statement import TravelStatement

__all__ = [
    'Base',
    'Group',
    'user_groups',
    'User',
    'Organization',
    'Client',
    'Ticket',
    'State',
    'City',
    'Travel',
    'TravelPassenger',
    'TravelPayout',
    'TravelStatement',
    'VehicleTravelHistory',
    'Notification',
    'ParameterGroup',
    'Parameter',
    'Note',
    'Application',
    'ClientApplication',
    'Permission',
    'group_permissions',
    'Vehicle',
    'MaintenanceType',
    'VehicleKmLog',
    'VehicleIssue',
    'VehicleMaintenanceHistory',
    'VehicleMaintenanceConfig'
]

from sqlalchemy import Table, Column, Integer, ForeignKey
from ..database.core import Base

workout_routine_association = Table(
    'workout_routine', Base.metadata,
    Column('workout_id', Integer, ForeignKey('workouts.id')),
    Column('routine_id', Integer, ForeignKey('routines.id'))
) 
from sqlalchemy import Column, Integer, String, ForeignKey, Index
from sqlalchemy.orm import relationship
from ..database.core import Base
from ..entities.association import workout_routine_association

class Routine(Base):
    __tablename__ = 'routines'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String, index=True)
    description = Column(String, index=True)
    workouts = relationship('Workout', secondary=workout_routine_association, back_populates='routines')

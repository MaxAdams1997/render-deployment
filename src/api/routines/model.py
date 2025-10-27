from pydantic import BaseModel
from typing import List, Optional

class RoutineBase(BaseModel):
    name: str
    description: Optional[str] = None

class RoutineCreate(RoutineBase):
    workouts: List[int] = []

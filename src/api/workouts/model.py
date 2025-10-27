from pydantic import BaseModel
from typing import Optional

class WorkoutBase(BaseModel):
    name: str
    description: Optional[str] = None
    
class WorkoutCreate(WorkoutBase):
    pass
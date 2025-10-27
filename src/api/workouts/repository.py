from sqlalchemy.orm import Session
from ..entities.workout import Workout
from typing import List, Optional
from sqlalchemy.orm import load_only


def get_workout_by_id(db: Session, workout_id: int) -> Optional[Workout]:
    return db.query(Workout).filter(Workout.id == workout_id).first()


def get_workouts(db: Session, user_id: int, skip: int = 0, limit: int = 10) -> List[Workout]:
     return db.query(Workout).options(load_only(Workout.id, Workout.name, Workout.description))\
        .filter(Workout.user_id == user_id).offset(skip).limit(limit).all()

def create_workout(db: Session, user_id: int, name: str, description: Optional[str]) -> Workout:
    db_workout = Workout(name=name, description=description, user_id=user_id)
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    return db_workout


def delete_workout(db: Session, workout_id: int) -> Optional[Workout]:
    db_workout = db.query(Workout).filter(Workout.id == workout_id).first()
    if db_workout:
        db.delete(db_workout)
        db.commit()
    return db_workout

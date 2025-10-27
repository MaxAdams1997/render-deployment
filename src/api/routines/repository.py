from sqlalchemy.orm import Session, joinedload, load_only
from ..entities.routine import Routine
from ..entities.workout import Workout
from typing import List, Optional


def get_routines(db: Session, user_id: int, skip: int = 0, limit: int = 10) -> List[Routine]:
    return (
        db.query(Routine)
        .options(
            load_only(Routine.id, Routine.name, Routine.description),
            joinedload(Routine.workouts).load_only(Workout.id, Workout.name)
        )
        .filter(Routine.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    

def create_routine(db: Session, user_id: int, name: str, description: Optional[str], workout_ids: List[int]) -> Routine:
    workouts = db.query(Workout).filter(Workout.id.in_(workout_ids)).all() if workout_ids else []
    db_routine = Routine(name=name, description=description, user_id=user_id, workouts=workouts)
    db.add(db_routine)
    db.commit()
    db.refresh(db_routine)
    return db.query(Routine).options(joinedload(Routine.workouts)).filter(Routine.id == db_routine.id).first()


def delete_routine(db: Session, user_id: int, routine_id: int) -> Optional[Routine]:
    db_routine = db.query(Routine).filter(Routine.id == routine_id, Routine.user_id == user_id).first()
    if db_routine:
        db.delete(db_routine)
        db.commit()
    return db_routine

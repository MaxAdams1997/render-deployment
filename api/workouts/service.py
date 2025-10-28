from sqlalchemy.orm import Session
from ..workouts import repository, model

def get_workout(db: Session, user: dict, workout_id: int):
    return repository.get_workout_by_id(db, workout_id)


def get_workouts(db: Session, user: dict, skip: int = 0, limit: int = 10):
    return repository.get_workouts(db, user_id=user.get('id'), skip=skip, limit=limit)


def create_workout(db: Session, user: dict, workout: model.WorkoutCreate):
    return repository.create_workout(db, user_id=user.get('id'), name=workout.name, description=workout.description)


def delete_workout(db: Session, user: dict, workout_id: int):
    return repository.delete_workout(db, workout_id)

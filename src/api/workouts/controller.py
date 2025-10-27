from fastapi import APIRouter, status

from api.deps import db_dependency, user_dependency
from . import model, service

router = APIRouter(
    prefix='/workouts',
    tags=['workouts']
)

@router.get('/')
def get_workout(db: db_dependency, user: user_dependency, workout_id: int):
    return service.get_workout(db, user, workout_id)

@router.get('/workouts')
def get_workouts(db: db_dependency, user: user_dependency, skip: int = 0, limit: int = 10):
    return service.get_workouts(db, user, skip=skip, limit=limit)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_workout(db: db_dependency, user: user_dependency, workout: model.WorkoutCreate):
    return service.create_workout(db, user, workout)

@router.delete("/")
def delete_workout(db: db_dependency, user: user_dependency, workout_id: int):
    return service.delete_workout(db, user, workout_id)
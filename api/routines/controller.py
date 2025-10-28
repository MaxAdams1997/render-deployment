from fastapi import APIRouter
from ..deps import db_dependency, user_dependency
from . import model, service

router = APIRouter(
    prefix='/routines',
    tags=['routines']
)

@router.get("/")
def get_routines(db: db_dependency, user: user_dependency, skip: int = 0, limit: int = 10):
    return service.get_routines(db, user, skip=skip, limit=limit)

@router.post("/")
def create_routine(db: db_dependency, user: user_dependency, routine: model.RoutineCreate):
    return service.create_routine(db, user, routine)

@router.delete('/')
def delete_routine(db: db_dependency, user: user_dependency, routine_id: int):
    return service.delete_routine(db, user, routine_id)
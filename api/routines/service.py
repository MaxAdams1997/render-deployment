from sqlalchemy.orm import Session
from ..routines import repository, model

def get_routines(db: Session, user: dict, skip: int = 0, limit: int = 10):
    return repository.get_routines(db, user_id=user.get('id'), skip=skip, limit=limit)


def create_routine(db: Session, user: dict, routine: model.RoutineCreate):
    return repository.create_routine(
        db,
        user_id=user.get('id'),
        name=routine.name,
        description=routine.description,
        workout_ids=routine.workouts
    )


def delete_routine(db: Session, user: dict, routine_id: int):
    return repository.delete_routine(db, user_id=user.get('id'), routine_id=routine_id)

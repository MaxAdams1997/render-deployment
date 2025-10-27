from fastapi import FastAPI
from .routines.controller import router as routines_router
from .workouts.controller import router as workouts_router
from .auth.controller import router as auth_router

def register_routes(app: FastAPI):
    app.include_router(auth_router)
    app.include_router(workouts_router)
    app.include_router(routines_router)
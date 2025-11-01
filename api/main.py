from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import HTMLResponse
from .middleware import configure_middleware
from .api import register_routes
from .database.core import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

configure_middleware(app)

templates = Jinja2Templates(directory="templates")

@app.get("/healthy")
def health_check():
    return 'Health check complete'

@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.get("/signin", response_class=HTMLResponse)
def signin_page(request: Request):
    return templates.TemplateResponse("signin.html", {"request": request})

register_routes(app)

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import HTMLResponse
from .middleware import configure_middleware
from .api import register_routes
from .database.core import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

configure_middleware(app)

# Mount static directory for images/css/js. Uses path relative to this file (src/api) -> src/static
import os
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))
if os.path.isdir(static_dir):
    app.mount('/static', StaticFiles(directory=static_dir), name='static')

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


@app.get("/contact", response_class=HTMLResponse)
def contact_page(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})

register_routes(app)

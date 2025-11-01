from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import urllib.request
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

# Simple proxy endpoint to fetch and cache external cover artwork (no DB usage).
@app.get('/static/proxy/greensleeves')
def proxy_greensleeves():
    # Try multiple remote artwork URLs (some CDNs block hotlinking). If all fail, serve local SVG fallback.
    remote_candidates = [
        'https://images.discogs.com/1QwQvQwQvQwQvQwQvQwQvQwQvQw=/fit-in/600x600/filters:strip_icc():format(jpeg):mode_rgb():quality(90)/discogs-images/R-7549711-1463402822-5637.jpeg.jpg',
        'https://img.discogs.com/SW1hZ2U6MjAzNjgwMzI=/fit-in/600x600/filters:strip_icc():format(jpeg):mode_rgb():quality(90)/discogs-images/R-7549711-1463402822-5637.jpeg.jpg'
    ]
    cache_dir = os.path.join(static_dir, 'cache')
    os.makedirs(cache_dir, exist_ok=True)
    cache_file = os.path.join(cache_dir, 'greensleeves.jpg')
    # if cache exists return it immediately
    if os.path.exists(cache_file):
        return FileResponse(cache_file, media_type='image/jpeg')

    for url in remote_candidates:
        try:
            # fetch with timeout
            with urllib.request.urlopen(url, timeout=6) as resp:
                if resp.status == 200:
                    # write to cache
                    with open(cache_file, 'wb') as fh:
                        fh.write(resp.read())
                    return FileResponse(cache_file, media_type='image/jpeg')
        except Exception:
            continue

    # fallback to the embedded SVG file in static/images
    fallback = os.path.join(static_dir, 'images', 'greensleeves.svg')
    if os.path.exists(fallback):
        return FileResponse(fallback, media_type='image/svg+xml')
    # final fallback: return 404-like response but still point to fallback path
    return FileResponse(fallback, media_type='image/svg+xml')

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

from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from db.utilis.config import SessionLocal
from db.utilis.queries import get_top_similar_metadata

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

# Mount for image dataset
app.mount("/static", StaticFiles(directory="data/ixi_png_dataset"), name="static")

# DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Homepage
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Render results
@app.get("/search", response_class=HTMLResponse)
def search(request: Request, participant_id: str, db: Session = Depends(get_db)):
    results = get_top_similar_metadata(db, participant_id)
    return templates.TemplateResponse("results.html", {
        "request": request,
        "results": results
    })
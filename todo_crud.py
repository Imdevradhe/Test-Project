from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .database import SessionLocal, engine, Base
from . import models, crud

Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    todos = crud.get_all_todos(db)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "todos": todos
    })


@app.get("/create", response_class=HTMLResponse)
def create_page(request: Request):
    return templates.TemplateResponse("create.html", {"request": request})


@app.post("/create")
def create_todo(
    title: str = Form(...),
    description: str = Form(...),
    db: Session = Depends(get_db)
):
    crud.create_todo(db, title, description)
    return RedirectResponse("/", status_code=303)


@app.get("/edit/{todo_id}", response_class=HTMLResponse)
def edit_page(todo_id: int, request: Request, db: Session = Depends(get_db)):
    todo = crud.get_todo(db, todo_id)

    return templates.TemplateResponse("edit.html", {
        "request": request,
        "todo": todo
    })


@app.post("/edit/{todo_id}")
def update_todo(
    todo_id: int,
    title: str = Form(...),
    description: str = Form(...),
    completed: bool = Form(False),
    db: Session = Depends(get_db)
):
    crud.update_todo(db, todo_id, title, description, completed)

    return RedirectResponse("/", status_code=303)


@app.get("/delete/{todo_id}")
def delete(todo_id: int, db: Session = Depends(get_db)):
    crud.delete_todo(db, todo_id)

    return RedirectResponse("/", status_code=303)

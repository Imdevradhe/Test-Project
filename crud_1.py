from sqlalchemy.orm import Session
from app import models


def get_all_todos(db: Session):
    return db.query(models.Todo).all()


def get_todo(db: Session, todo_id: int):
    return db.query(models.Todo).filter(models.Todo.id == todo_id).first()


def create_todo(db: Session, title: str, description: str):
    todo = models.Todo(title=title, description=description)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    print("")
    return todo


def update_todo(db: Session, todo_id: int, title: str, description: str, completed: bool):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()

    if todo:
        todo.title = title
        todo.description = description
        todo.completed = completed
        db.commit()
        db.refresh(todo)

    return todo


def delete_todo(db: Session, todo_id: int):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()

    if todo:
        db.delete(todo)
        db.commit()

from sqlalchemy.orm import Session

from . import models, schemas


def get_task(db: Session, id: int):
    return db.query(models.Task).filter(models.Task.id == id).first()


def create_user(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(
        time_limit = task.time_limit,
        to_user = task.to_user,
        details = task.details,
        by_user = task.by_user
        )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

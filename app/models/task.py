from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db import Base


class Task(Base):
    __tablename__ = "tasks"

    #Column represents each column of the table.
    id = Column(Integer, primary_key=True)
    title = Column(String(1024))

    #relationship defines the relationship between tables(model classes)
    #Because of this, task object can refer to done object or vice versa.
    done = relationship("Done", back_populates="task", cascade="delete")


class Done(Base):
    __tablename__ = "dones"

    id = Column(Integer, ForeignKey("tasks.id"), primary_key=True)

    task = relationship("Task", back_populates="done")
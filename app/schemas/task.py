#This file represents the schema. 
#The schema defines the api request and response.
from typing import Optional

from pydantic import BaseModel, Field


#BaseModel represents FastAPI shema model.
#TaskBase class is made by inheriting BaseModel.
#TaskBase class has 3 fields(id, title, and done).
#Each field has type hint(int, Optional[str], and bool).
#On the right of =, Field has the optional info.
#first attribute is to be set default value.
class TaskBase(BaseModel):
    title: Optional[str] = Field(None, example="Do laundry")


class TaskCreate(TaskBase):
    pass


#As a response to TaskCreate, add the id to TaskCreateResponse.
class TaskCreateResponse(TaskCreate):
    id: int

    #orm_mode = true implies that TaskCreateResponse(response schema) take ORM
    #(object relational mapping), and convert it into response schema.
    #ORM is a technique used in creating a bridge between object-oriented
    #programs and, in most case, relational databases.
    class Config:
        orm_mode = True


class Task(TaskBase):
    id: int
    done: bool = Field(False, description="Done")


    class Config:
        #Use this mode to connect DB.
        orm_mode = True

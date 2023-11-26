from sqlalchemy.ext.asyncio import AsyncSession

import app.models.task as task_model
import app.schemas.task as task_schema

from typing import List, Tuple, Optional

from sqlalchemy import select
from sqlalchemy.engine import Result


#async def defines a coroutine expression that returns a coroutine object.
#Coroutines are computer program components that allow execution to be supended #and resumed, generalizing subroutines for cooperative multitasking.
async def create_task(
    db: AsyncSession, task_create: task_schema.TaskCreate
) -> task_model.Task:
    task = task_model.Task(**task_create.dict())
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task
#await let python stop this coroutine process, and do the other coroutine process.

# 1. Take the schema(task_create: task_schema.TaskCreate) as the argument.
# 2. Convert this into DB model, task_model.Task.
# 3. Commit to DB.
# 4. Update task(Task instance) based on the data in DB.
#    In this case, take the id of created record.
# 5. Return the created DB model.


async def get_tasks_with_done(db: AsyncSession) -> List[Tuple[int, str, bool]]:
    result: Result = await (
        db.execute(
            select(
                task_model.Task.id,
                task_model.Task.title,
                task_model.Done.id.isnot(None).label("done"),
            ).outerjoin(task_model.Done)
        )
    )
    return result.all() #Take the all of DB records.

#select() selects the necessary fields, and then .outerjoin() selects the model
#to be joined to main DB model.

#task_model.Done.id.isnot(None).label("done")
#If Done.id exists, then done=True, otherwise done=False.
#Then, return the joined record.


async def get_task(db: AsyncSession, task_id: int) -> Optional[task_model.Task]:
    result: Result = await db.execute(
        select(task_model.Task).filter(task_model.Task.id == task_id)
    )
    task: Optional[Tuple[task_model.Task]] = result.first()
    return task[0] if task is not None else None
#.filter() narrows the target by SELECT ~ WHERE.


async def update_task(
    db: AsyncSession, task_create: task_schema.TaskCreate, original: task_model.Task
) -> task_model.Task:
    original.title = task_create.title
    db.add(original)
    await db.commit()
    await db.refresh(original)
    return original
#Take DB model as an original, then Update the contents and return them.


async def delete_task(db: AsyncSession, original: task_model.Task) -> None:
    await db.delete(original)
    await db.commit()
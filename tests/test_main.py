import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.db import get_db, Base
from app.main import app

import starlette.status

ASYNC_DB_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture
async def async_client() -> AsyncClient:
    # Create an engine and session for Async
    async_engine = create_async_engine(ASYNC_DB_URL, echo=True)
    async_session = sessionmaker(
        autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
    )

    # Initialize SQLite table for the test
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # Change the direction of FastAPI DB to DB for the test using DI
    async def get_test_db():
        async with async_session() as session:
            yield session

    app.dependency_overrides[get_db] = get_test_db

    # Return Async HTTP client for the test
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_create_and_read(async_client): #async_client has the return value of fixture
    response = await async_client.post("/tasks", json={"title": "test_task"}) #POST makes todo task
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["title"] == "test_task"

    response = await async_client.get("/tasks") #GET checks the created todo task
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert len(response_obj) == 1
    assert response_obj[0]["title"] == "test_task"
    assert response_obj[0]["done"] is False


@pytest.mark.asyncio
async def test_done_flag(async_client):
    response = await async_client.post("/tasks", json={"title": "test_task2"})
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["title"] == "test_task2"

    # Put done flag
    response = await async_client.put("/tasks/1/done")
    assert response.status_code == starlette.status.HTTP_200_OK

    # Return 400 as there is the flag already
    response = await async_client.put("/tasks/1/done")
    assert response.status_code == starlette.status.HTTP_400_BAD_REQUEST

    # Get rid of the done flag
    response = await async_client.delete("/tasks/1/done")
    assert response.status_code == starlette.status.HTTP_200_OK

    # Return 404 as there is no done flag anymore
    response = await async_client.delete("/tasks/1/done")
    assert response.status_code == starlette.status.HTTP_404_NOT_FOUND
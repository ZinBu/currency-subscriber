import typing

import pytest
from httpx import AsyncClient

from database.db import engine, SQLModel
from main import app


class TestRunningError(Exception):
    pass


# TODO resolve pre_init for test base
# if 'test' not in engine.url.database.lower():
#     raise TestRunningError(f'Not relevant database: {engine.url.database}')


# Set async test runner
@pytest.fixture(autouse=True)
def anyio_backend() -> str:
    return 'asyncio'


async def create_new_test_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


@pytest.fixture
async def prepare_db() -> typing.Coroutine:
    # await create_new_test_db()
    # yield
    return create_new_test_db()


# Make requests in our tests
@pytest.fixture
async def client() -> AsyncClient:
    async with AsyncClient(
        app=app,
        base_url='http://localhost:8000',
        headers={'Content-Type': 'application/json'}
    ) as client:
        yield client

import typing

import pytest

from database.db import engine, SQLModel
from database.init_db_data import init_data_in_db


# Set async test runner
@pytest.fixture(autouse=True)
def anyio_backend() -> str:
    return 'asyncio'


async def create_new_test_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


@pytest.fixture(autouse=True)
async def prepare_db() -> typing.Coroutine:
    await create_new_test_db()
    await init_data_in_db()
    yield

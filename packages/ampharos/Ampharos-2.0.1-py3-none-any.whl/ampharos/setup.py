import json

from collections import namedtuple
from typing import Any, List, Tuple

from donphan import MaybeAcquire

from .tables import ALL_TABLES
from .utils import get_base_dir


BASE_DIR = get_base_dir()


async def setup_ampharos():
    """Populates the Pokemon database.

    This method should always be called on startup"""
    async with MaybeAcquire() as connection:

        # Populate the tables if required
        for table in ALL_TABLES:

            # If Table is empty
            if (await table.fetchrow(connection=connection)) is None:

                record = namedtuple("record", (column.name for column in table._columns))
                data: List[Tuple[Any, ...]] = []

                try:
                    with open(BASE_DIR / f"data/{table.__name__.lower()}.json") as f:
                        for item in json.load(f):
                            data.append(record(**item))
                except FileNotFoundError:
                    print(f"Could not find Pokemon data file {table.__name__.lower()}.json")
                else:
                    try:
                        await table.insert_many(table._columns, *data, connection=connection)
                    except Exception as e:
                        print(e)

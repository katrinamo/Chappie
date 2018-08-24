import asyncio
import asyncpg


class AsyncClient:
    def __init__(self):
        self.conn: asyncpg.Connection = None

    async def connect(self, **kwargs):
        self.conn = await asyncpg.connect(**kwargs)
        return self.conn

    async def disconnect(self):
        if self.conn is not None:
            await self.conn.close()
            self.conn = None

    async def execute(self, query: str, is_select: bool = False, fetch_all: bool = False, params: tuple = ()):
        if self.conn is not None:
            if is_select:
                if fetch_all:
                    return await self.conn.fetch(query)
                else:
                    return await self.conn.fetchrow(query)
            else:
                try:
                    return await self.conn.execute(query, *params)
                except asyncpg.UniqueViolationError:
                    return


class Database(AsyncClient):

    def __init__(self, **kwargs):
        super().__init__()
        self.loop = asyncio.get_event_loop()
        self.connect(**kwargs)

    def wait(self, future):
        return self.loop.run_until_complete(future)

    def connect(self, **kwargs):
        return self.wait(super().connect(**kwargs))

    def disconnect(self):
        return self.wait(super().disconnect())

    def execute(self, **kwargs):
        return self.wait(super().execute(**kwargs))
import asyncpg
import logging
import asyncio

class Database(object):
    logger = None
    pool = None
    conn = None
    current_transaction = None

    @classmethod
    async def create_pool(cls, config):
        """
        Creates a database pool
        """

        new_config = config.copy()
        if new_config.pop('enabled') is False:
            cls.logger.error("Database pool is being creating despite being disabled.")
            return

        cls.pool = await asyncpg.create_pool(**new_config)

    @classmethod
    async def get_connection(cls):
        cls.conn = await cls.pool.aquire()
        return cls

    async def disconnect(self):
        await self.pool.release(self.conn)
        self.conn = None

    async def start_transaction(self):
        self.current_transaction = self.conn.transaction()
        await self.current_transaction.start()

    async def commit_transaction(self):
        await self.current_transaction.commit()
        self.current_transaction = None

    async def __aenter__(self, *args):
        return await self.get_connection()

    async def __aexit__(self, *args):
        return await self.disconnect()

    async def __call__(self, sql, *args):
        if 'select' in sql.lower() or 'returning' in sql.lower():
            x = self.conn.fetch(sql, *args)
        else:
            await self.conn.execute(sql, *args)
            return

        if x:
            return x
        elif 'select' in sql.lower() or 'returning' in sql.lower():
            return []
        return None

#class DatabaseChannel(object):
#    def __init__(self, channel_name, callback):
#        self.channel_name = channel_name
#        self.callback = callback
#        self.cog = None
#
#        self.conn = Database
#        self.logger = self.conn.logger
#        self.loop = asyncio.get_event_loop()
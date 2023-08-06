import aioredis
import logging
import asyncio
import json

class Redis(object):
    logger = None
    pool = None

    @classmethod
    async def create_pool(cls, config):
        """
        Creates and connects to redis pool
        """

        modified_config = config.copy()
        if modified_config.pop("enabled") is False:
            cls.logger.error("Redis pool is being created despite being disabled.")
            return

        address = modified_config.pop('host'), modified_config.pop('port')
        cls.pool = await aioredis.create_redis_pool(address, **modified_config)

    @classmethod
    async def release_pool(cls):
        """
        Releases redis pool
        """
        await cls.pool.close()

    async def get(self, key):
        """
        Get a value from the redis database
        """

        self.logger.debug(f"Getting value with redis key {key}")
        value = await self.pool.get(key)
        return value.decode()

    async def mget(self, *keys):
        """
        Get multiple values from the redis database
        """

        self.logger.debug(f"Getting redis values for keys {keys}")
        values = await self.pool.mget(keys)
        return [i.decode() for i in values]

    async def set(self, key, value):
        """
        Set a value to a key with the database pool
        """

        self.logger.debug(f"Setting redis key {key} to value {value}")
        await self.pool.set(key, value)

    async def publish(self, channel, dict):
        """
        Publish a json message to a redis channel
        """

        self.logger.debug(f"Sending json message to redis channel {channel}")
        await self.pool.publish_json(channel, dict)

    #async def publish_str(self, channel, str):
    #    """
    #    Publish a message to a redis channel
    #    """

    #    self.logger.debug(f"Sending message to redis channel {channel}")
    #    await self.pool.publish(channel, str)

class RedisChannel(object):
    def __init__(self, channel_name, callback):
        self.channel_name = channel_name
        self.callback = callback
        self.cog = None

        self.pool = Redis.pool
        self.logger = Redis.logger
        self.loop = asyncio.get_event_loop()
        self.handler_task = None

    def start(self):
        self.handler_task = self.loop.create_task(self._start())

    def stop(self):
        self.handler_task.cancel()

    def cancel(self):
        self.loop.run_until_complete(self.unsubscribe(self.channel_name))

    async def _start(self):
        """
        Start redis channel handler
        """

        self.logger.debug(f"Starting redis channel {self.channel_name}")
        channel = await self.subscribe(self.channel_name)
        while (await channel.wait_message()):
            self.logger.debug(f"Recived a message at redis channel {self.channel_name}")
            data = await channel.get_json()

            # Send out the message
            try:
                self.loop.create_task(self.callback(self.cog, data))
            except Exception as e:
                self.logger.error(f"Could not send message to redis channel {self.channel_name} - {e}")

    async def _cancel(self):
        self.logger.debug(f"Stopping redis channel {self.channel_name}")
        await self.unsubscribe(self.channel_name)
        del self

    async def subscribe(self, channel):
        """
        Subscribes to a redis channel
        """

        self.logger.debug(f"Subscribing to redis channel {self.channel_name}")
        channels = await self.pool.subscribe(channel)
        return channels[0]

    async def unsubscribe(self, channel):
        """
        Unsubscribes to a redis channel
        """

        self.logger.debug(f"Unsubscribing from redis channel {self.channel_name}")
        await self.pool.unsubscribe(channel)
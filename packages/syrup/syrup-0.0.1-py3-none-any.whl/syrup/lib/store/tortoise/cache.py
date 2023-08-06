from aioredis import Redis
from syrup.lib.store.redis.client import get_client

from syrup.lib.store.redis import STANDALONE_MODE

from syrup.lib.store.redis.types import RedisConf


class Cache:
    def __init__(self) -> None:
        self.redis: Redis = None  # type: ignore
        self.expire: int = 4000

    async def init_redis_cache(self, cache_config: dict = None) -> None:
        """"""
        if cache_config:
            conf = RedisConf(
                address=cache_config.get("address", ("127.0.0.1", 3379)),
                password=cache_config.get("password", None) or None,
                mode=STANDALONE_MODE
            )
            redis, err = await get_client(conf)
            if err:
                return
            self.redis = redis

    @staticmethod
    def get_cache_pk_key(database, db_table, pk_attr, pk_value):
        return f"cache#{database}.{db_table}#{pk_attr}#{pk_value}"


cache = Cache()

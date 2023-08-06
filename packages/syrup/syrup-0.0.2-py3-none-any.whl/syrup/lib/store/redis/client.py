from aioredis import create_redis_pool, Redis
from aioredis_cluster import create_redis_cluster

from syrup.lib.store.redis import CLUSTER_MODE, STANDALONE_MODE
from syrup.lib.store.redis.types import RedisConf


async def get_client(r: RedisConf) -> (Redis, Exception):
    """"""
    if r.mode == CLUSTER_MODE:
        return await get_cluster_client(r.address, r.password)
    elif r.mode == STANDALONE_MODE:
        return await get_standalone_client(r.address, r.password)
    else:
        return None, ValueError(f"不支持的 redis 模式 '{r.mode}'")


async def get_cluster_client(address: tuple, password: str = None) -> (Redis, Exception):
    """
    cluster
    :param address: (("127.0.0.1", 6379), ("127.0.0.1", 6380),)
    :param password:
    :return:
    """
    try:
        redis = await create_redis_cluster(address, password=password)
    except Exception as e:
        return None, e
    return redis, None


async def get_standalone_client(address: tuple, password: str = None) -> (Redis, Exception):
    """
    standalone
    :param address: ("127.0.0.1", 6379)
    :param password:
    :return:
    """
    try:
        redis = await create_redis_pool(address, password=password)
    except Exception as e:
        return None, e
    return redis, None

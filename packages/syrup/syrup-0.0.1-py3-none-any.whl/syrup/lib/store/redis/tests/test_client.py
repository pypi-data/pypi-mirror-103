import aiounittest

from syrup.lib.store.redis import STANDALONE_MODE, CLUSTER_MODE
from syrup.lib.store.redis.client import get_client
from syrup.lib.store.redis.types import RedisConf


class ClientTestCase(aiounittest.AsyncTestCase):
    async def test_await_async_get_client(self):
        conf = RedisConf(
            address=("127.0.0.1", 6800),
            password="ss",
            mode=STANDALONE_MODE
        )
        # conf = RedisConf(
        #     address=(("127.0.0.1", 6800),),
        #     password=None,
        #     mode=CLUSTER_MODE
        # )
        redis, err = await get_client(conf)
        if err:
            self.assertFalse(err)
            return
        redis.close()
        await redis.wait_closed()

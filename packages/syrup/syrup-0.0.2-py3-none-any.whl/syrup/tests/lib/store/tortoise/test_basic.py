import aiounittest
from syrup.tests.lib.store.tortoise.t_init import init
from syrup.tests.lib.store.tortoise.t_model import Account


class TortoiseTestCase(aiounittest.AsyncTestCase):
    async def test_await_async_get_client(self):
        await init()
        count = await Account.filter().count()
        print(count)
        pass

    async def test_await_async_get_one(self):
        await init()
        account = await Account.get_or_none(id=7)
        if account:
            print(account.mobile)
            kwargs = {
                "id": 7
            }
            # await Account.update_or_create(**kwargs)
            # await account.delete()
            # account.is_valid = 2
            # await account.save()
        # t = {k: getattr(account, k) for k in account._meta.db_fields if getattr(account, k) != None}
        # print(t)
        pass

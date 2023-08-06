from syrup.lib.store.tortoise import Tortoise


async def init():
    # Here we create a SQLite DB using file "db.sqlite3"
    #  also specify the app name of "models"
    #  which contain models from "app.models"
    await Tortoise.init(
        db_url='mysql://root:asdfasdf@127.0.0.1:3306/nest_user',
        modules={'models': ['syrup.tests.lib.store.tortoise.t_model']},
        cache_config={
            "address": ("127.0.0.1", 6800),
            "password": None,
        }
    )
    # Generate the schema
    # await Tortoise.generate_schemas()

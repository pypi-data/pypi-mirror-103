from syrup.lib.store.tortoise import fields
from syrup.lib.store.tortoise.models import Model


class Account(Model):
    id = fields.IntField(pk=True)
    mobile = fields.CharField(max_length=18)
    password = fields.CharField(max_length=64, default="")
    is_valid = fields.IntField(default=1)
    last_login_ip = fields.CharField(max_length=15, default="")
    last_login_at = fields.DatetimeField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(null=True)
    is_activate = fields.IntField(default=1)
    tenant_id = fields.IntField(default=1)

    class Meta:
        table = 'account'
        use_cache = True

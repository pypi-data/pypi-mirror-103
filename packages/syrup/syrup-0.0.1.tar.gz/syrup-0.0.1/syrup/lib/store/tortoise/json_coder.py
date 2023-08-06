import datetime
import decimal
import json
import sys


class TortoiseJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            args = ('year', 'month', 'day', 'hour', 'minute',
                    'second', 'microsecond')
            return {'__type__': 'datetime.datetime',
                    'args': [getattr(obj, a) for a in args]}
        elif isinstance(obj, datetime.date):
            args = ('year', 'month', 'day')
            return {'__type__': 'datetime.date',
                    'args': [getattr(obj, a) for a in args]}
        elif isinstance(obj, datetime.time):
            args = ('hour', 'minute', 'second', 'microsecond')
            return {'__type__': 'datetime.time',
                    'args': [getattr(obj, a) for a in args]}
        elif isinstance(obj, datetime.timedelta):
            args = ('days', 'seconds', 'microseconds')
            return {'__type__': 'datetime.timedelta',
                    'args': [getattr(obj, a) for a in args]}
        elif isinstance(obj, decimal.Decimal):
            return {'__type__': 'decimal.Decimal',
                    'args': [str(obj), ]}
        else:
            return super().default(obj)


class TortoiseJSONDecoder(json.JSONDecoder):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, object_hook=self.object_hook,
                         **kwargs)

    def object_hook(self, d):
        if '__type__' not in d:
            return d
        o = sys.modules[__name__]
        for e in d['__type__'].split('.'):
            o = getattr(o, e)
        args, kwargs = d.get('args', ()), d.get('kwargs', {})
        return o(*args, **kwargs)


if __name__ == '__main__':
    j1 = json.dumps({'now': datetime.datetime.now(),
                     'val': decimal.Decimal('9.3456789098765434987654567')},
                    cls=TortoiseJSONEncoder)
    print(j1)
    o1 = json.loads(j1, cls=TortoiseJSONDecoder)
    print(o1)



class RedisConf(object):
    """"""
    address: tuple
    password: str = None
    mode: str

    def __init__(self, address: tuple, password: str = None, mode: str = ''):
        self.address = address
        self.password = password
        self.mode = mode

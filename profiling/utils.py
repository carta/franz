from datetime import datetime

import faker

import franz


def timeit(func):
    def _wrap(*args, **kwargs):
        start = datetime.now()
        ret = func(*args, **kwargs)
        elapsed = datetime.now() - start
        print("Call {}({}, {}) took {}".format(
            func.__name__, args, kwargs, elapsed
        ))
        return ret
    return _wrap


class Message(franz.FranzEvent):
    fake = faker.Faker()

    def __init__(self, size=256, fields=1):
        self.size = size or 1
        self.fields = fields or 0
        self.data = {
            self.fake.first_name(): self.fake.name()
            for _ in range(self.fields)
        }
        self.data.update({
            'bin': self.fake.binary(length=self.size),
        })

    def serialize(self):
        return self.data

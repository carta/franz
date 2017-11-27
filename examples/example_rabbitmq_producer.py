import random
import time

import franz


class FranzData(franz.FranzEvent):
    def serialize(self):
        return {'data': time.time()}


with franz.RabbitProducer(exchange='topic_link') as p:
    while True:
        key = random.choice(['hello.world', 'hello.bob'])
        p.send_message(key, FranzData())
        time.sleep(1)

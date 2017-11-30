# Franz

A lite wrapper around [Kafka](https://kafka.apache.org/) and [RabbitMQ](https://www.rabbitmq.com/).

# Usage

## Installation
- `pip install franz` (recommended)
- `pip -e git+git@github.com:eshares/franz.git@master#egg=franz`
  - Change `@master` to a version or commit if required.
 
## RabbitMQ
### Sending a message
```python
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
```

### Consuming messages
```python
import franz

def callback(ch, method, properties, body):
    print('[+] {} from {}'.format(body, method.routing_key))

with franz.RabbitConsumer('hello.*', exchange='topic_link') as c:
    c.consume_messages(callback)
```


## Kafka
### Sending a message
```python
import franz
from myapp.models import SomeModel  # SomeModel must inherit `franz.FranzEvent`

instance = SomeModel.objects.get(pk=1)
producer = franz.KafkaProducer()
producer.send_message('TopicA', instance)
```

### Consuming messages
```python
import franz

consumer = franz.KafkaConsumer('TopicA')
for message in consumer:
    print(message.value)
```

### Kafka/Docker Resources

- [Docker image](https://github.com/spotify/docker-kafka)
- [Helpful article](https://howtoprogram.xyz/2016/07/21/using-apache-kafka-docker/)
- Create topic
```
./kafka-topics.sh --create --topic test --replication-factor 1 --partitions 1 --zookeeper 0.0.0.0:2181
```
- Consuming
```
./kafka-console-consumer.sh --topic test --from-beginning --zookeeper 0.0.0.0:2181
```
- Producing
```
./kafka-console-producer.sh --topic test --broker-list 0.0.0.0:9092
```

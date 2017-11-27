import franz


def callback(ch, method, properties, body):
    print('[+] {} from {}'.format(body, method.routing_key))


with franz.RabbitConsumer('hello.*', exchange='topic_link') as c:
    c.consume_messages(callback)

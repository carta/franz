from unittest import TestCase, mock

import franz


class TestConsumer(TestCase):
    @mock.patch('pika.BlockingConnection')
    def test_exchange_declare_called_for_each_topic(self, b):
        consumer = franz.RabbitConsumer('logs.critical')
        consumer._channel.exchange_declare.assert_called_with(
            exchange='logs',
            exchange_type='topic',
            durable=True
        )

    @mock.patch('pika.BlockingConnection')
    def test_queue_bind_called_for_each_topic(self, b):
        consumer = franz.RabbitConsumer('logs.critical')
        consumer._channel.queue_bind.assert_called_with(
            exchange='logs',
            queue='',
            routing_key='logs.critical',
        )

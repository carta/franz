import logging

import bson
import pika

from .parameters import RabbitConnectionParameters
from .producer import Producer


class ConsumerType:
    # User constants
    SINGLE_PROCESS = 'single'  # Single consumer
    MULTIPLE_FAST_PROCESSES = 'multiple-fast'  # Multiple fast consumers
    MULTIPLE_SLOW_PROCESSES = 'multiple-slow'  # Multiple slow consumers

    # Prefetch values
    _SINGLE_FAST_CONSUMER = 0
    _MULTIPLE_FAST_CONSUMERS = 20
    _MULTIPLE_SLOW_CONSUMERS = 1

    SPEED_TO_PREFETCH = {
        SINGLE_PROCESS: _SINGLE_FAST_CONSUMER,
        MULTIPLE_FAST_PROCESSES: _MULTIPLE_FAST_CONSUMERS,
        MULTIPLE_SLOW_PROCESSES: _MULTIPLE_SLOW_CONSUMERS,
    }


class Consumer:
    """
    A simple consumer wrapper for pika/RabbitMQ.

    Examples
    --------
    >>> from franz import RabbitConsumer
    >>> def callback(correlation_id, topic, body):
    >>>     msg = '[+] Received message {} from {}. ID: {}'.format(
    >>>         body, topic, correlation_id)
    >>>     print(msg)
    >>> with RabbitConsumer('myapp.logs.critical', queue='logs') as consumer:
    >>>     consumer.consume_messages(callback)
    """

    def __init__(self, *topics, queue='', parameters=None,
                 consumer_type=ConsumerType.SINGLE_PROCESS):
        """
        Parameters
        ----------
        topics : tuple
            The topics to consume from.
        queue : str
            The RabbitMQ queue to consume messages from.
        parameters : RabbitConnectionParameters
            The parameters to connect to the RabbitMQ server.
        consumer_type : str
            The type of consumer. A single consumer, multiple fast consumers,
            multiple slow consumers. See ConsumerType constants.
        """
        self._topics = topics
        self._queue_name = queue
        self._parameters = parameters

        self._connection = pika.BlockingConnection(self.parameters)
        self._channel = self._connection.channel()
        self._channel.basic_qos(
            prefetch_count=ConsumerType.SPEED_TO_PREFETCH[consumer_type],
        )

        self._channel.queue_declare(
            queue=self._queue_name,
            durable=True,
        )

        self._bind_queue()

    @property
    def parameters(self):
        if self._parameters is None:
            self._parameters = RabbitConnectionParameters()
        return self._parameters.connection_parameters

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._channel.stop_consuming()
        self._connection.close()

    def consume_messages(self, consumer_callback):
        def callback_wrapper(ch, method, properties, body):
            correlation_id = '{}.{}'.format(
                properties.correlation_id,
                self._queue_name,
            )
            logging.basicConfig(
                format='[%(levelname)s] {correlation_id}: %(message)s'.format(
                    correlation_id=correlation_id
                ),
                level=logging.INFO,
            )
            consumer_callback(
                correlation_id,
                method.routing_key,
                bson.loads(body),
            )
            ch.basic_ack(delivery_tag=method.delivery_tag)

        self._channel.basic_consume(
            callback_wrapper,
            queue=self._queue_name,
        )
        self._channel.start_consuming()

    def _bind_queue(self):
        for topic in self._topics:
            exchange = Producer.get_exchange_name(topic)

            self._channel.exchange_declare(
                exchange=exchange,
                exchange_type='topic',
                durable=True,
            )
            self._channel.queue_bind(
                exchange=exchange,
                queue=self._queue_name,
                routing_key=topic,
            )

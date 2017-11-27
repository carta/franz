import pika

from franz import base
from .parameters import RabbitConnectionParameters


class Producer(base.BaseProducer):
    """
    A simple producer wrapper for pika/RabbitMQ.

    Examples
    --------
    >>> from franz import RabbitProducer
    >>> from myapp.models import SomeModel
    >>> instance = SomeModel.objects.get(pk=1)
    >>> with RabbitProducer(exchange='logs') as p:
    >>>     p.send_message('myapp.logs.critical', instance)
    """

    PERSISTENT_DELIVERY_MODE = 2

    def __init__(self, parameters=None, exchange=''):
        self._parameters = parameters
        self._exchange = exchange
        self._connection = pika.BlockingConnection(self.parameters)

        self._channel = self._connection.channel()
        self._properties = pika.BasicProperties(
            delivery_mode=self.PERSISTENT_DELIVERY_MODE,
        )

        self._channel.exchange_declare(
            exchange=self._exchange,
            exchange_type='topic',
            durable=True,
        )

    @property
    def parameters(self):
        if self._parameters is None:
            self._parameters = RabbitConnectionParameters()
        return self._parameters.connection_parameters

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._connection.close()

    def _send_message_to_topic(self, topic, message):
        """
        Send a message to RabbitMQ based on the routing key (topic).

        Parameters
        ----------
        topic : str
            The routing key (topic) where the message should be sent to.
        message : FranzEvent
            The message to be sent.

        Raises
        ------
        franz.InvalidMessage
        """
        self._channel.basic_publish(
            self._exchange,
            topic,
            self.serialize_message(message),
            properties=self._properties,
        )

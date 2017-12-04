import uuid

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
    >>> with RabbitProducer(app_name='web') as p:
    >>>     p.send_message('myapp.logs.critical', instance)
    """

    PERSISTENT_DELIVERY_MODE = 2

    def __init__(self, app_name, parameters=None):
        self._parameters = parameters
        self._app_name = app_name
        self._connection = pika.BlockingConnection(self.parameters)

        self._channel = self._connection.channel()

    @property
    def parameters(self):
        if self._parameters is None:
            self._parameters = RabbitConnectionParameters()
        return self._parameters.connection_parameters

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._connection.close()

    def get_properties(self, correlation_id=None):
        return pika.BasicProperties(
            delivery_mode=self.PERSISTENT_DELIVERY_MODE,
            correlation_id=self.get_correlation_id(correlation_id),
        )

    def get_correlation_id(self, correlation_id=None):
        return '{uuid}.{app_name}'.format(
            uuid=correlation_id or str(uuid.uuid4()),
            app_name=self._app_name,
        )

    def send_message(self, topic, message, correlation_id=None):
        self._check_message_is_valid_event(message)
        self._send_message_to_topic(topic, message, correlation_id)

    def _send_message_to_topic(self, topic, message, correlation_id=None):
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
        exchange = self.get_exchange_name(topic)
        self._channel.exchange_declare(
            exchange=exchange,
            exchange_type='topic',
            durable=True,
        )
        self._channel.basic_publish(
            exchange,
            topic,
            self.serialize_message(message),
            properties=self.get_properties(correlation_id=correlation_id),
        )

    @classmethod
    def get_exchange_name(cls, topic):
        return topic.split('.')[0]

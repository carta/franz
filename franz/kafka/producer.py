from kafka import KafkaProducer
from kafka.producer.future import FutureRecordMetadata

from franz import FranzEvent, base


class Producer(base.BaseProducer):
    """
    A simple wrapper around kafka.KafkaProducer.

    Examples
    --------
    >>> from franz import KafkaProducer
    >>> from myapp.models import SomeModel
    >>> instance = SomeModel.objects.get(pk=1)
    >>> p = KafkaProducer()
    >>> p.send_message('test', instance)
    """

    def __init__(self, host='localhost', port=None):
        self.host = host
        self.port = port

        self.producer = KafkaProducer(
            bootstrap_servers=self.connection_string,
            value_serializer=Producer.serialize_message,
        )

    @property
    def connection_string(self):
        return '{host}{port}'.format(
            host=self.host,
            port=':{}'.format(self.port) if self.port else '',
        )

    def _send_message_to_topic(self, topic, message):
        """
        Send a message to a Kafka topic.

        Parameters
        ----------
        topic : str
            The kafka topic where the message should be sent to.
        message : FranzEvent
            The message to be sent.

        Raises
        ------
        franz.InvalidMessage
        """
        message_result = self.producer.send(topic, message)
        self.check_for_message_exception(message_result)
        return message_result

    @classmethod
    def check_for_message_exception(cls, message_result):
        """
        Makes sure there isn't an error when sending the message.
        Kafka will silently catch exceptions and not bubble them up.

        Parameters
        ----------
        message_result : FutureRecordMetadata
        """
        exception = message_result.exception

        if exception:
            raise exception

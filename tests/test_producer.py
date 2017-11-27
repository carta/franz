from unittest import TestCase
from unittest.mock import patch

from kafka import KafkaProducer

from franz import Producer, FranzEvent, InvalidMessage, SerializationError


class TestProducer(TestCase):

    def setUp(self):
        self.topic = 'test'
        self.producer = Producer()

    def test_producer_creation(self):
        producer = self.producer.producer
        self.assertIsInstance(producer, KafkaProducer)

    def test_send_message(self):
        class FranzBytes(FranzEvent, bytes):
            pass

        message = FranzBytes(b'testing message')

        with patch.object(self.producer.producer, 'send') as mock:
            self.producer.send_message(
                self.topic,
                message
            )
            mock.assert_called_with(self.topic, message)

    def test_send_message_without_subclassing_franz_event_raises_exception(self):
        with self.assertRaises(InvalidMessage):
            self.producer.send_message(self.topic, b'hi there')

    def test_send_message_with_valid_object_subclass_but_valid_object(self):
        class Test:
            pass

        class Unserializable(FranzEvent):
            def serialize(self):
                return {
                    'a': 'b',
                    'c': Test(),
                }

        with self.assertRaises(SerializationError):
            self.producer.send_message(self.topic, Unserializable())

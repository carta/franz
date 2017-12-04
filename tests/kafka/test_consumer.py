import re
from unittest import TestCase
from kafka import KafkaConsumer

from franz import KafkaConsumer as Consumer


class TestConsumer(TestCase):

    def setUp(self):
        self.topics = ['ResponseEvent', 'ModelChange-Certificate']
        self.consumer = Consumer(*self.topics)

    def test_topic_subscription(self):
        inner_consumer = self.consumer.consumer

        self.assertIsNotNone(inner_consumer)
        self.assertIsInstance(inner_consumer, KafkaConsumer)

    def test_make_topic_regex(self):
        assert self.consumer._make_topic_regex() == r'(ResponseEvent)|(ModelChange-Certificate)'

    def test_complicated_topic_regex(self):
        consumer = Consumer('ModelChange-*', 'ResponseEvent')
        assert consumer._make_topic_regex() == r'(ModelChange-*)|(ResponseEvent)'

    def test_complicated_topic_regex_matches(self):
        consumer = Consumer('ModelChange-*')
        pattern = re.compile(consumer._make_topic_regex())
        assert pattern.match('ModelChange-Certificate') is not None
        assert pattern.match('ModelChange-OptionGrant') is not None

    def test_regex_matches_literals(self):
        pattern = re.compile(self.consumer._make_topic_regex())
        assert pattern.match('ResponseEvent') is not None
        assert pattern.match('ModelChange-Certificate') is not None
        assert pattern.match('ModelChange-OptionGrant') is None

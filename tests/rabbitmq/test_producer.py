import re
from unittest import TestCase, mock


from franz import RabbitProducer


class TestProducer(TestCase):
    uuid4hex = re.compile('^[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}\Z', re.I)

    def test_get_exchange_name_without_dots(self):
        assert RabbitProducer.get_exchange_name('http') == 'http'

    def test_get_exchange_name_with_dots(self):
        assert RabbitProducer.get_exchange_name('http.response.404') == 'http'

    @mock.patch('pika.BlockingConnection')
    def test_get_properties_without_correlation_id_with_app_name(self, b):
        producer = RabbitProducer(app_name='web')
        properties = producer.get_properties()
        assert properties.correlation_id.endswith('.web')

    @mock.patch('pika.BlockingConnection')
    def test_get_properties_with_correlation_id_with_app_name(self, b):
        producer = RabbitProducer(app_name='web')
        properties = producer.get_properties('123.slack')
        assert properties.correlation_id == '123.slack.web'

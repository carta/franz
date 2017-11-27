import pika


class RabbitConnectionParameters:
    _DEFAULT = pika.ConnectionParameters._DEFAULT

    def __init__(
        self, host='localhost', port=5672, virtual_host='/',
        username=None, password=None,
    ):
        self.host = host
        self.port = port
        self.virtual_host = virtual_host
        self.username = username
        self.password = password

    @property
    def connection_parameters(self):
        return pika.ConnectionParameters(
            host=self.host,
            port=self.port,
            credentials=self.credentials,
            virtual_host=self.virtual_host,
        )

    @property
    def credentials(self):
        if self.username and self.password:
            return pika.PlainCredentials(
                username=self.username,
                password=self.password,
            )
        return self._DEFAULT

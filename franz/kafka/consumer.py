import bson

from kafka import KafkaConsumer


class Consumer:
    """
    A simple wrapper around KafkaConsumer.

    Examples
    --------
    >>> from franz import KafkaConsumer
    >>> consumer = KafkaConsumer('TopicA', 'Topic-*')
    >>> for message in consumer:
    >>>     print(message.value)
    """
    def __init__(self, *topics, server='localhost'):
        """
        Parameters
        ----------
        topics : tuple
            String arguments that are exact topic names like 'MyTopic' or
            pattern names like 'MyTopic-*'
        """
        self.topics = topics
        self.consumer = KafkaConsumer(
            value_deserializer=bson.loads,
            bootstrap_servers=server,
        )
        self.consumer.subscribe(pattern=self._make_topic_regex())

    def __iter__(self):
        return self.consumer.__iter__()

    def _make_topic_regex(self):
        """
        Makes an OR regex for all topics passed in. KafkaConsumer doesn't allow
        for patterns and regular topics by default so this allows support for
        both.

        Returns
        -------
        str
            The OR'd regex for all topics.
        """
        return '|'.join("({})".format(topic) for topic in self.topics)

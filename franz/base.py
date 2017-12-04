import bson

from franz import FranzEvent, InvalidMessage, SerializationError


class BaseProducer:
    def send_message(self, topic, message):
        self._check_message_is_valid_event(message)
        self._send_message_to_topic(topic, message)

    def _send_message_to_topic(self, topic, message):
        raise NotImplementedError(
            "_send_message_to_topic should be overridden in subclasses."
        )

    @staticmethod
    def serialize_message(message):
        """
        Serializes an object. It must subclass :class:`FranzEvent`.

        Parameters
        ----------
        message : FranzEvent
            The object to be serialized.

        Returns
        -------
        bytes
        """
        try:
            return bson.dumps(message.serialize())
        except bson.UnknownSerializerError:
            raise SerializationError(
                "Unable to serialize message: {}.".format(message)
            )

    @staticmethod
    def _check_message_is_valid_event(message):
        if not isinstance(message, FranzEvent):
            raise InvalidMessage(
                "{} is not a valid message. "
                "Must subclass `franz.FranzEvent`.".format(
                    type(message),
                )
            )

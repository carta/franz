class FranzEvent:
    """
    Classes that want to be sent as messages to Kafka
    should inherit from this class.
    """

    def serialize(self):
        """
        Converts the current python object to one that bson can serialize.
        Complex objects should define their own `.serialize()` method.

        Returns
        -------
        dict
        """
        return self.__dict__.copy()

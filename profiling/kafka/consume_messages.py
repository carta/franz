import argparse

import franz

from profiling.utils import timeit

if __name__ == '__main__':

    @timeit
    def consume_messages():
        consumer = franz.KafkaConsumer('test')
        parser = argparse.ArgumentParser(
            description='Consumes franz events from kafka stream'
        )
        parser.add_argument(
            '--messages', '-m', metavar='N',
            type=int, default=1000
        )
        args = parser.parse_args()
        count = 0
        try:
            for messages in consumer:
                print('recvd')
                count += 1
                if count == args.messages:
                    raise Exception("Stopping to wait for more messages.")
        except Exception:
            pass

    consume_messages()

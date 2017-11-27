import argparse

import franz
from profiling.utils import timeit, Message


if __name__ == '__main__':
    producer = franz.KafkaProducer()
    parser = argparse.ArgumentParser(
        description='Generates franz events into kafka stream'
    )
    parser.add_argument('--size', '-s', metavar='X', type=int, default=256)
    parser.add_argument('--fields', '-f', metavar='N', type=int, default=5)
    parser.add_argument('--messages', '-m', metavar='M', type=int, default=1000)

    args = parser.parse_args()

    message = Message(args.size, args.fields)

    @timeit
    def make_messages():
        for _ in range(args.messages):
            producer.send_message('test', message)

    print('sending {:,} messages.....'.format(args.messages))
    make_messages()

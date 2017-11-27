import argparse

import franz
from profiling.utils import timeit, Message


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generates franz events into rabbitmq stream'
    )
    parser.add_argument('--size', '-s', metavar='X', type=int, default=256)
    parser.add_argument('--fields', '-f', metavar='N', type=int, default=5)
    parser.add_argument('--messages', '-m', metavar='M', type=int, default=1000)

    parser.add_argument('--host', metavar='H', type=str, default='localhost')
    parser.add_argument('--username', '-u', metavar='U', type=str, default=None)
    parser.add_argument('--password', '-p', metavar='P', type=str, default=None)
    parser.add_argument('--vhost', '-v', metavar='P', type=str, default='/')
    parser.add_argument('--exchange', '-e', metavar='E', type=str, default='')

    args = parser.parse_args()

    params = franz.RabbitConnectionParameters(
        host=args.host,
        virtual_host=args.vhost,
        username=args.username,
        password=args.password,
    )

    message = Message(args.size, args.fields)

    @timeit
    def make_messages():
        with franz.RabbitProducer(
            parameters=params,
            exchange=args.exchange
        ) as producer:
            for _ in range(args.messages):
                producer.send_message('test', message)

    print('sending {:,} messages.....'.format(args.messages))
    make_messages()

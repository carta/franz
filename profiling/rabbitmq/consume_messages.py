import argparse

import franz

from profiling.utils import timeit

if __name__ == '__main__':
    count = 0

    @timeit
    def consume_messages():
        parser = argparse.ArgumentParser(
            description='Consumes franz events from kafka stream'
        )
        parser.add_argument(
            '--messages', '-m', metavar='N',
            type=int, default=500
        )
        parser.add_argument('--host', metavar='H', type=str,
                            default='localhost')
        parser.add_argument('--username', '-u', metavar='U', type=str,
                            default=None)
        parser.add_argument('--password', '-p', metavar='P', type=str,
                            default=None)
        parser.add_argument('--vhost', '-v', metavar='P', type=str,
                            default='/')
        args = parser.parse_args()

        params = franz.RabbitConnectionParameters(
            host=args.host,
            virtual_host=args.vhost,
            username=args.username,
            password=args.password,
        )

        def callback(correlation_id, topic, body):
            print('recvd message')

            global count
            if args.messages == count:
                raise Exception('done')
            count += 1

        with franz.RabbitConsumer(
            'test',
            parameters=params,
            queue='slack',
        ) as c:
            c.consume_messages(callback)

    consume_messages()

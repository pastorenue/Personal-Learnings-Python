import sys
import pika
from pika.exchange_type import ExchangeType

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost',
                              port=5672,
                              virtual_host="/",
                              credentials=pika.PlainCredentials("guest", "guest")
    )
)

channel = connection.channel()
channel.exchange_declare(exchange="logs", exchange_type=ExchangeType.fanout)

message = " ".join(sys.argv[1:]) or "info: Hello World!"
channel.basic_publish(exchange="logs",
                      routing_key="",
                      body=message)
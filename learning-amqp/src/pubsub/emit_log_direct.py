import sys
import pika
from pika.exchange_type import ExchangeType

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host="localhost",
        port=5672,
        virtual_host="/",
        credentials=pika.PlainCredentials("guest", "guest")
    )
)

channel = connection.channel()
channel.exchange_declare(exchange="direct_logs", exchange_type=ExchangeType.direct)
severity = sys.argv[1] if len(sys.argv) > 1 else "info"
message = " ".join(sys.argv[2:]) or "Hello World!"

channel.basic_publish(exchange="direct_logs", routing_key=severity, body=message)

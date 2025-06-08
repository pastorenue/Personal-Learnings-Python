import pika


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost',
                              port=5672,
                              virtual_host="/",
                              credentials=pika.PlainCredentials("guest", "guest")
    )
)
channel = connection.channel()

channel.exchange_declare(exchange="logs", exchange_type="fanout")
result = channel.queue_declare(queue="")
channel.queue_bind(exchange="logs", queue=result.method.queue)

print(" [x] Waiting for logs. To exit, press CTRL+C")

def callback(ch, method, properties, body):
    print(f" [x] {body}")

channel.basic_consume(result.method.queue, on_message_callback=callback, auto_ack=True)
channel.start_consuming()
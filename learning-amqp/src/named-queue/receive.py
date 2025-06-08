from src.connection import create_connection

_, channel = create_connection()
channel.queue_declare(queue='hello')

def callback(ch, method, properties, body):
    print(f" [x] Received {body}")
    # ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(
    queue='hello',
    on_message_callback=callback,
    auto_ack=False  # Set to False to manually acknowledge messages
)
print(' [*] Waiting for messages. To exit press CTRL+C')
try:
    channel.start_consuming()
except KeyboardInterrupt:
    print(" [*] Exiting...")

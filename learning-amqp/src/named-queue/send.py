import json

from src.connection import create_connection


connection, channel = create_connection()
channel.queue_declare(queue='hello')

msgs = [
    {'name': 'Michael Scott', 'age': 46, 'city': 'Scranton'},
    {'name': 'Pam Beesly', 'age': 31, 'city': 'Scranton'},
    {'name': 'Jim Halpert', 'age': 33, 'city': 'Philadelphia'},
    {'name': 'Dwight Schrute', 'age': 41, 'city': 'Scranton'}
]

for msg in msgs:
    channel.basic_publish(exchange='',
                        routing_key='hello',
                        body=json.dumps(msg))
    print(f" [x] Sent {json.dumps(msg)}")

channel.basic_publish(exchange='',
                    routing_key='hello',
                    body=json.dumps(msg))

print(f" [x] Sent {json.dumps(msg)}")

connection.close()
# Learning AMQP with RabbitMQ

This project is a personal exploration of RabbitMQ and the AMQP protocol. It serves as a refresher to understand and experiment with the different types of exchanges provided by RabbitMQ.

## Various Exchanges
### Direct Exchange
Learn how to route messages to specific queues based on routing keys.

### Fanout Exchange
Explore broadcasting messages to all queues bound to the exchange.

### Topic Exchange
Experiment with routing messages based on pattern matching of routing keys.

### Headers Exchange
Understand how to route messages based on message headers instead of routing keys.

### RPC (Remote Procedure Call)
Implement request-response messaging patterns using RabbitMQ.

## Prerequisites

- RabbitMQ installed using docker or installed locally.
- Basic understanding of messaging patterns and the AMQP protocol.
- A working installation of your Python

## Getting Started

1. Clone the repository:
    ```bash
    git clone https://github.com/pastorenue/msq.git
    cd msq
    ```

2. Follow the instructions in each directory's README to run the examples.

3. Experiment with the code and modify it to deepen your understanding.

## Resources

- [RabbitMQ Official Documentation](https://www.rabbitmq.com/documentation.html)
- [AMQP 0-9-1 Model Explained](https://www.rabbitmq.com/tutorials/amqp-concepts.html)
- [RabbitMQ Tutorials](https://www.rabbitmq.com/getstarted.html)

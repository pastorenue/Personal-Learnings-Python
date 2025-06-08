from concurrent import futures
import time
import grpc
import greet_pb2
import greet_pb2_grpc


def get_client_stream_requests():
    name = input("Enter a name or nothing to stop chatting: ")
    while True:
        if name == "":
            break
        greeting = input("Enter greeting message: ")
        if greeting == "":
            break
        yield greet_pb2.HelloRequest(greeting=greeting, name=name)
        time.sleep(2)

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = greet_pb2_grpc.GreeterStub(channel)
        print("Greeter client starting...")
        print("1. SayHello - Unary")
        print("2. ParrotSaysHello - Server Streaming")
        print("3. ChattyClientSaysHello - Client Side Streaming")
        print("4. InteractingHello - Both Streaming")
        choice = input("Enter choice: ")
        match choice:
            case "1":
                request = greet_pb2.HelloRequest(greeting="Hello", name="you")
                response = stub.SayHello(request)
                print("Greeter client received: " + response.message)
                return
            case "2":
                 request = greet_pb2.HelloRequest(greeting="Hello", name="you")
                 response = stub.ParrotSaysHello(request)
                 for reply in response:
                     print("Greeter client received: " + reply.message)
                 return
            case "3":
                delayed_reply = stub.ChattyClientSaysHello(get_client_stream_requests())
                print("ChattyClientSaysHello request made: ")
                print(delayed_reply)
            case "4":
                response = stub.InteractingHello(get_client_stream_requests())
                for res in response:
                    print(f"Greeter client received: {res}")
            case _:
                print("Invalid choice")
                return

        response = stub.SayHello(greet_pb2.HelloRequest(name='you'))


if __name__ == '__main__':
    run()

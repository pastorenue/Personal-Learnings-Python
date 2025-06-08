from concurrent import futures
import time
import grpc
import greet_pb2
import greet_pb2_grpc


class GreaterServicer(greet_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        print("Greeter received: " + request.greeting + " " + request.name)
        return greet_pb2.HelloReply(message="Hello " + request.name)

    def ParrotSaysHello(self, request, context):
        print("ParrotSaysHello request made")
        print(f"Parrot received: {request}")
        for i in range(3):
            reply = greet_pb2.HelloReply()
            reply.message = f"{request.greeting} {request.name} {i+1}"
            yield reply
            time.sleep(3)
    
    def ChattyClientSaysHello(self, request_iterator, context):
        delayed_reply = greet_pb2.DelayedReply()
        for request in request_iterator:
            print("ChattyClientSaysHello request made: ")
            print(f"Client received: {request}")
            delayed_reply.request.append(request)
        
        delayed_reply.message = f"You have sent {len(delayed_reply.request)} messages."
        return delayed_reply
    
    def InteractingHello(self, request_iterator, context):
        for req in request_iterator:
            print("InteractingHello request made: ")
            print(req)

            hello_reply = greet_pb2.HelloReply()
            hello_reply.message = req.greeting + " " + req.name
            yield hello_reply


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    greet_pb2_grpc.add_GreeterServicer_to_server(GreaterServicer(), server)
    server.add_insecure_port('localhost:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

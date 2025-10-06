import sys
from concurrent import futures

import grpc

from simple_example.proto import tea_grpc_pb2, tea_grpc_pb2_grpc

TEMP = {
    "white": 60,
    "green": 70,
    "black": 100,
}


class TeaServer(tea_grpc_pb2_grpc.TeaServiceServicer):
    def make_tea(self, request: tea_grpc_pb2.TeaRequest, context):
        match request.color:
            case "white":
                return tea_grpc_pb2.TeaResponse(temperature=60)
            case "green":
                return tea_grpc_pb2.TeaResponse(temperature=70)
            case "black":
                return tea_grpc_pb2.TeaResponse(temperature=100)
            case _:
                return tea_grpc_pb2.TeaResponse()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=3))
    tea_grpc_pb2_grpc.add_TeaServiceServicer_to_server(TeaServer(), server)
    server.add_insecure_port("0.0.0.0:50051")
    server.start()
    print("Server started, listening on 50051")
    server.wait_for_termination()


if __name__ == "__main__":
    sys.exit(serve())

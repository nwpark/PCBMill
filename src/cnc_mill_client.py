
import grpc

import cnc_mill_pb2
import cnc_mill_pb2_grpc


def run():
    with grpc.insecure_channel('192.168.1.89:50051') as channel:
        stub = cnc_mill_pb2_grpc.CNCMillStub(channel)
        response = stub.GoTo(cnc_mill_pb2.Position(x=5, y=7))
        print(response)


if __name__ == "__main__":
    run()

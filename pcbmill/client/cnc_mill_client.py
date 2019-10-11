import grpc
import sys
sys.path.append('../generated')
from pcbmill.generated import cnc_mill_pb2
from pcbmill.generated import cnc_mill_pb2_grpc

# ip_addr = '192.168.1.89'
ip_addr = 'localhost'


def run():
    with grpc.insecure_channel('192.168.1.89:50051') as channel:
        stub = cnc_mill_pb2_grpc.CNCMillStub(channel)
        # response = stub.GoTo(cnc_mill_pb2.Position(x=4000, y=0, z=0))
        # response = stub.GoTo(cnc_mill_pb2.Position(x=0, y=0, z=0))
        # response = stub.GoTo(cnc_mill_pb2.Position(x=4000, y=0, z=0))
        # response = stub.GoTo(cnc_mill_pb2.Position(x=0, y=0, z=0))
        response = stub.Move(cnc_mill_pb2.Position(x=2000, y=0, z=0))
        response = stub.Move(cnc_mill_pb2.Position(x=-2000, y=0, z=0))
        response = stub.Move(cnc_mill_pb2.Position(x=2000, y=0, z=0))
        response = stub.Move(cnc_mill_pb2.Position(x=-2000, y=0, z=0))
        print(response)


if __name__ == "__main__":
    run()

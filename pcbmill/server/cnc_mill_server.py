from concurrent import futures
import time
import grpc
import sys
sys.path.append('../generated')

from pcbmill.server import fpga_interface
from pcbmill.generated import cnc_mill_pb2
from pcbmill.generated import cnc_mill_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class CNCMillServicer(cnc_mill_pb2_grpc.CNCMillServicer):

    def __init__(self):
        self.fpga = fpga_interface.FPGAInterface()

    def GoTo(self, request, context):
        print(request)

        self.fpga.set_data(request.x)
        self.fpga.request_action(0).result()

        self.fpga.set_data(request.y)
        self.fpga.request_action(0).result()

        self.fpga.request_action(1).result()
        # future.add_done_callback(lambda i: print(i))
        return cnc_mill_pb2.Response(succeeded=True)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    cnc_mill_pb2_grpc.add_CNCMillServicer_to_server(CNCMillServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    while True:
        time.sleep(_ONE_DAY_IN_SECONDS)


if __name__ == "__main__":
    serve()

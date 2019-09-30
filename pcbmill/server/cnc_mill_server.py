from concurrent import futures
from pcbmill.config.config import Command, ONE_DAY_IN_SECONDS
from pcbmill.server import fpga_interface
from pcbmill.generated.cnc_mill_pb2 import Response
from RPi import GPIO
import logging
import time
import grpc
import sys
sys.path.append('../generated')
from pcbmill.generated import cnc_mill_pb2_grpc


class CNCMillServicer(cnc_mill_pb2_grpc.CNCMillServicer):

    def __init__(self):
        self.fpga = fpga_interface.FPGAInterface()

    def GoTo(self, request, context):
        print(request)

        self.fpga.set_data(request.x)
        self.fpga.request_action(Command.LOAD_DATA).result()

        self.fpga.set_data(request.y)
        self.fpga.request_action(Command.LOAD_DATA).result()

        self.fpga.request_action(Command.GOTO).result()
        # future.add_done_callback(lambda i: print(i))
        return Response(succeeded=True)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    cnc_mill_pb2_grpc.add_CNCMillServicer_to_server(CNCMillServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    while True:
        time.sleep(ONE_DAY_IN_SECONDS)


if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO)
        serve()
    finally:
        logging.warning('Service was interrupted')
        GPIO.cleanup()

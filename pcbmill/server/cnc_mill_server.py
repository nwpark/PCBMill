from concurrent import futures
from google.protobuf import text_format
from pcbmill.config.config import ONE_DAY_IN_SECONDS, log_format, log_datefmt
from pcbmill.generated.cnc_mill_pb2 import Response, Command
from pcbmill.server import fpga_interface
import grpc
import logging
import time
import sys
sys.path.append('../generated')
from pcbmill.generated import cnc_mill_pb2_grpc


class CNCMillServicer(cnc_mill_pb2_grpc.CNCMillServicer):

    def __init__(self):
        self._fpga_interface = fpga_interface.FPGAInterface()
        self._log = logging.getLogger(__name__)

    def GoTo(self, request, context):
        self._log.info('Received GoTo request: {{{}}}.'.format(text_format.MessageToString(request, as_one_line=True)))

        self._fpga_interface.request_action(Command.LOAD_DATA, data=request.x).result()
        self._fpga_interface.request_action(Command.LOAD_DATA, data=request.y).result()
        self._fpga_interface.request_action(Command.GOTO).result()
        # future.add_done_callback(lambda i: print(i))
        return Response(succeeded=True)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._log.critical('Servicer killed.')
        self._fpga_interface.cleanup()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    with CNCMillServicer() as servicer:
        cnc_mill_pb2_grpc.add_CNCMillServicer_to_server(servicer, server)
        server.add_insecure_port('[::]:50051')
        server.start()
        logging.info('Servicer started on port 50051.')
        while True:
            time.sleep(ONE_DAY_IN_SECONDS)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format=log_format, datefmt=log_datefmt)
    serve()

from concurrent import futures
import time

import grpc

import cnc_mill_pb2
import cnc_mill_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class CNCMillServicer(cnc_mill_pb2_grpc.CNCMillServicer):

    def GoTo(self, request, context):
        print(request)
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

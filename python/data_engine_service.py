import logging
import random
import grpc

from common import boxes_pb2_grpc
from common import boxes_pb2
from common.consul_services import consul_register, consul_unregister
from data_engine.data_engine import DataEngine
from concurrent import futures


class DataEngineService(boxes_pb2_grpc.DataEngineServicer):
    def __init__(self):
        self.de = DataEngine()

    def ExecuteQuery(self, request, context):
        pb_table = self.de.select_query(request.q, request.column_types)
        return pb_table

def serve(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    boxes_pb2_grpc.add_DataEngineServicer_to_server(DataEngineService(), server)
    server.add_insecure_port('[::]:' + str(port))
    server.start()
    try:
        server.wait_for_termination()
    except:
        print('User aborted')

if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

    port = 51234 #random.randint(51234, 59000)
    name = 'DataEngineService'

    #consul_register(name, port)
    serve(port)
    #consul_unregister(name, port)

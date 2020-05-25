import pandas as pd 


from concurrent import futures
import logging

import grpc

import table_pb2
import table_pb2_grpc


class CsvConnector(table_pb2_grpc.TableQueryServicer):

  def GetTable(self, request, context):
    swim_data = pd.read_csv('../input/' + request.name, usecols=['Intervaller', 'Längder', 'Sträcka', 'Tid', 'Total tid', 'Medeltempo', 'Medel-Swolf', 'Totalt antal simtag']) 
    return table_pb2.Table(message=str(swim_data))


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    table_pb2_grpc.add_TableQueryServicer_to_server(CsvConnector(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
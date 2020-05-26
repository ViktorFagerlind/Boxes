import pandas as pd 


from concurrent import futures
import logging

import grpc

import table_pb2
import table_pb2_grpc

from prototables import df_to_prototable

from pandas.api.types import is_numeric_dtype


class CsvConnector(table_pb2_grpc.TableQueryServicer):

  def GetTable(self, request, context):
    csv_df = pd.read_csv('../input/' + request.name)#, usecols=['Intervaller', 'Längder', 'Sträcka', 'Tid', 'Total tid', 'Medeltempo', 'Medel-Swolf', 'Totalt antal simtag'])

    return df_to_prototable(csv_df)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    table_pb2_grpc.add_TableQueryServicer_to_server(CsvConnector(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    serve()
    #cc = CsvConnector()
    #cc.GetTable(table_pb2.Query(name='swim.csv'), None)
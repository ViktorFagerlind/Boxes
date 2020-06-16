import random
import pandas as pd
import logging
import grpc

from concurrent import futures
from prototables import df_to_prototable
from servicediscover import consul_register, consul_unregister

import table_pb2_grpc

class CsvConnector(table_pb2_grpc.TableQueryServicer):
  def GetTable(self, request, context):
    csv_df = pd.read_csv('../input/' + request.name)#, usecols=['Intervaller', 'Längder', 'Sträcka', 'Tid', 'Total tid', 'Medeltempo', 'Medel-Swolf', 'Totalt antal simtag'])

    return df_to_prototable(csv_df)


def serve(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    table_pb2_grpc.add_TableQueryServicer_to_server(CsvConnector(), server)
    server.add_insecure_port('[::]:' + str(port))
    server.start()
    try:
        server.wait_for_termination()
    except:
        print('User aborted')


if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

    port = random.randint(50000, 59000)

    name = 'Connector'
    consul_register(name, port)
    serve(port)
    consul_unregister(name, port)

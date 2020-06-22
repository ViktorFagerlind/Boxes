import logging
import os
import random
import grpc
import pandas as pd

from concurrent import futures

from common import boxes_pb2_grpc
from common import boxes_pb2
from common.consul_services import consul_register, consul_unregister
from common.df_prototables import df_to_prototable, df_to_protoschema


class CsvConnector(boxes_pb2_grpc.ConnectorServicer):
    def __init__(self):
        self.indir = '../input'
        self.csv_to_df = {}
        for file in os.listdir(self.indir):
            if file.endswith('.csv'):
                self.csv_to_df[file] = None
                print(os.path.join(self.indir, file))

    def get_df(self, name):
        if self.csv_to_df[name] is None:
            self.csv_to_df[name] = pd.read_csv(os.path.join(self.indir, name))
        return self.csv_to_df[name]

    def GetTableNames(self, request, context):
        return boxes_pb2.TableNames(table_names = [n for n in self.csv_to_df])

    def GetTableSchemas(self, request, context):
        names = request.table_names
        proto_schemas = boxes_pb2.TableSchemas(table_schemas=[])
        for n in names:
            df = self.get_df(n)
            proto_schemas.table_schemas.append(df_to_protoschema(df))

        return proto_schemas

    def GetTable(self, request, context):
        return df_to_prototable(self.get_df(request.name))


def serve(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    boxes_pb2_grpc.add_ConnectorServicer_to_server(CsvConnector(), server)
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

import logging

import grpc

import table_pb2
import table_pb2_grpc

from prototables import prototable_to_df

def apply_alorithm(name):
    with grpc.insecure_channel('localhost:50052') as channel:
        stub = table_pb2_grpc.AlgorithmsStub(channel)
        response = stub.Average(table_pb2.Query(name=name))
        logging.info('Algorithm received: ' + str(response))

def get_table(name):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = table_pb2_grpc.TableQueryStub(channel)
        proto_table = stub.GetTable(table_pb2.Query(name=name))

        return prototable_to_df(proto_table)

def run():
    df = get_table('swim.csv')
    logging.debug(df)

    apply_alorithm('Data engine')

if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    run()

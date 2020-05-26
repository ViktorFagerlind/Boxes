import logging

import grpc

import table_pb2
import table_pb2_grpc

from prototables import prototable_to_df

def average(values):
    with grpc.insecure_channel('localhost:50052') as channel:
        stub = table_pb2_grpc.AlgorithmsStub(channel)
        response = stub.Average(table_pb2.DoubleList(values=values))

        return response.value

def get_table(name):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = table_pb2_grpc.TableQueryStub(channel)
        proto_table = stub.GetTable(table_pb2.Query(name=name))

        return prototable_to_df(proto_table)

def run():
    df = get_table('swim.csv')
    print(df)

    key = 'Totalt antal simtag'
    avg = average(df[key])
    print('\n\nAverage of %s: %f' % (key, avg))

if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    run()

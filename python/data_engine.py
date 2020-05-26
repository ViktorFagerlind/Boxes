import logging

import grpc

import table_pb2
import table_pb2_grpc


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
      stub = table_pb2_grpc.TableQueryStub(channel)
      response = stub.GetTable(table_pb2.Query(name='swim.csv'))
      logging.info('table: ' + str(response))

    with grpc.insecure_channel('localhost:50052') as channel:
      stub = table_pb2_grpc.AlgorithmsStub(channel)
      response = stub.Average(table_pb2.Query(name='Data engine'))
      logging.info('Algorithm received: ' + str(response))


if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    run()

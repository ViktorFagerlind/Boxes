import logging

import grpc

import table_pb2
import table_pb2_grpc


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
      stub = table_pb2_grpc.TableQueryStub(channel)
      response = stub.GetTable(table_pb2.Query(name='swim.csv'))
      print("csv data: " + response.message)

    with grpc.insecure_channel('localhost:50052') as channel:
      stub = table_pb2_grpc.TableQueryStub(channel)
      response = stub.GetTable(table_pb2.Query(name='Data engine'))
      print("Algorithm received: " + response.message)


if __name__ == '__main__':
    logging.basicConfig()
    run()

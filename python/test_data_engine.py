import logging

import grpc

import table_pb2
import table_pb2_grpc

def test_data_engine():
    with grpc.insecure_channel('localhost:50053') as channel:
        stub = table_pb2_grpc.DataEngineStub(channel)
        response = stub.GetPlotData(table_pb2.Query(name='swim.csv'))
        print(response)

if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    test_data_engine()

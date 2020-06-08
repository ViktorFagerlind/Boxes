from concurrent import futures
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

def fix_swimming(df):
    del df['Unnamed: 0']

def get_average(name):
    df = get_table(name)
    fix_swimming(df)
    print(df)

    key = 'Totalt antal simtag'
    avg = average(df[key])
    print('\n\nAverage of %s: %f' % (key, avg))

    return avg

class DataEngineService(table_pb2_grpc.DataEngineServicer):
  def GetPlotData(self, request, context):
    return table_pb2.DoubleValue(value=get_average(request.name))

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    table_pb2_grpc.add_DataEngineServicer_to_server(DataEngineService(), server)
    server.add_insecure_port('[::]:50053')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    serve()

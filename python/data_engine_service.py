import random
import logging
import grpc

from concurrent import futures
from prototables import prototable_to_df
from servicediscover import consul_register, consul_unregister, consul_find_service

import table_pb2
import table_pb2_grpc

services = {}


def average(values):
    with grpc.insecure_channel('localhost:50052') as channel:
        stub = table_pb2_grpc.AlgorithmsStub(channel)
        response = stub.Average(table_pb2.DoubleList(values=values))

        return response.value


def get_table(name):
    proto_table = services['Connector'][0].GetTable(table_pb2.Query(name=name))
    return prototable_to_df(proto_table)


def get_average_from_column(name, key='Totalt antal simtag'):
    df = get_table(name)

    avg = average(df[key])
    print('\n\nAverage of %s: %f' % (key, avg))

    return avg


def connect_services(service_name):
    (ip,ports) = consul_find_service(service_name)

    stubs = []
    for port in ports:
        channel = grpc.insecure_channel(ip + ':' + str(port))
        stubs.append(table_pb2_grpc.TableQueryStub(channel))
    services[service_name] = stubs


class DataEngineService(table_pb2_grpc.DataEngineServicer):
  def GetPlotData(self, request, context):
    return table_pb2.DoubleValue(value=get_average_from_column(request.name))


def serve(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    table_pb2_grpc.add_DataEngineServicer_to_server(DataEngineService(), server)
    server.add_insecure_port('[::]:' + str(port))
    server.start()
    try:
        server.wait_for_termination()
    except:
        print('User aborted')

if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

    connect_services('Connector')

    port = random.randint(50000, 59000)
    name = 'DataEngineService'

    # For testing
    df = get_table('swim.csv')
    print(df)
    # -----------

    consul_register(name, port)
    serve(port)
    consul_unregister(name, port)

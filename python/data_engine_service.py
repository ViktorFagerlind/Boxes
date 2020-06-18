import random
import logging
import grpc

from concurrent import futures
from prototables import prototable_to_df
from servicediscover import consul_register, consul_unregister, consul_find_service

import boxes_pb2
import boxes_pb2_grpc

connectors = []
name_to_connector = {}
table_to_connector = {}

def get_table_names():
    return [n for n in table_to_connector]


# Go through the names and use all names in a row that belong to the same connector in one service call
# This is to avoid one call per name while still keeping the name order
def get_table_schemas(names):
    proto_tableschemas = boxes_pb2.TableSchemas(table_schemas=[])
    i=0
    while i < len(names):
        c = table_to_connector[names[i]]
        names_for_connector = [names[i]]

        i = i+1
        while i < len(names) and table_to_connector[names[i]] == c:
            names_for_connector.append(names[i])
            i = i+1

        new_proto_tableschemas = c.GetTableSchemas(boxes_pb2.TableNames(table_names=names_for_connector))
        proto_tableschemas.table_schemas.extend(new_proto_tableschemas.table_schemas)

    return proto_tableschemas

def get_table(name):
    c = table_to_connector[name]
    t = c.GetTable(boxes_pb2.TableName(name=name))
    return t


def average(values):
    with grpc.insecure_channel('localhost:50052') as channel:
        stub = boxes_pb2_grpc.AlgorithmsStub(channel)
        response = stub.Average(boxes_pb2.DoubleList(values=values))

        return response.value

def setup_connectors():
    service_name = 'Connector'
    (ip,ports) = consul_find_service(service_name)

    name_to_connector[service_name] = []
    for port in ports:
        channel = grpc.insecure_channel(ip + ':' + str(port))
        connector = boxes_pb2_grpc.ConnectorStub(channel)
        connectors.append(connector)
        name_to_connector[service_name].append(connector)

    for connector in name_to_connector['Connector']:
        table_names = connector.GetTableNames(boxes_pb2.Empty()).table_names
        for n in table_names:
            table_to_connector[n] = connector

'''
class DataEngineService(boxes_pb2_grpc.DataEngineServicer):
  def GetPlotData(self, request, context):
    return table_pb2.DoubleValue(value=get_average_from_column(request.name))

def serve(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    boxes_pb2_grpc.add_DataEngineServicer_to_server(DataEngineService(), server)
    server.add_insecure_port('[::]:' + str(port))
    server.start()
    try:
        server.wait_for_termination()
    except:
        print('User aborted')
'''

if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

    setup_connectors()

    # For testing
    names = get_table_names()
    print(names)

    pts = get_table_schemas(names)
    #print(pts)

    for n,ps in zip(names,pts.table_schemas):
        pt = get_table(n)
        #print(pt)
        df = prototable_to_df(ps, pt)
        print(df)

        key = 'Totalt antal simtag'
        avg = average(df[key])
        print('\nAverage of %s: %f\n\n' % (key, avg))


    # -----------
    '''
    port = random.randint(50000, 59000)
    name = 'DataEngineService'

    consul_register(name, port)
    serve(port)
    consul_unregister(name, port)
    '''
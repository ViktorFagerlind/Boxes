import random
import logging
import grpc

from concurrent import futures
from prototables import prototable_to_df
from servicediscover import consul_register, consul_unregister, consul_find_service

import boxes_pb2
import boxes_pb2_grpc

class DataEngine():
    def __init__(self):
        self.connectors = []
        self.name_to_connector = {}
        self.table_to_connector = {}
        self.alg_service = None

        self.__setup_connectors()
        self.__setup_algorithms()


    def __setup_algorithms(self):
        service_name = 'Algorithms'
        (ip,ports) = consul_find_service(service_name)

        channel = grpc.insecure_channel(ip + ':' + str(ports[0]))
        self.alg_service = boxes_pb2_grpc.AlgorithmsStub(channel)


    def __setup_connectors(self):
        service_name = 'Connector'
        (ip,ports) = consul_find_service(service_name)

        self.name_to_connector[service_name] = []
        for port in ports:
            channel = grpc.insecure_channel(ip + ':' + str(port))
            connector = boxes_pb2_grpc.ConnectorStub(channel)
            self.connectors.append(connector)
            self.name_to_connector[service_name].append(connector)

        for connector in self.name_to_connector['Connector']:
            table_names = connector.GetTableNames(boxes_pb2.Empty()).table_names
            for n in table_names:
                self.table_to_connector[n] = connector


    def get_table_names(self):
        return [n for n in self.table_to_connector]


    # Go through the names and use all names in a row that belong to the same connector in one service call
    # This is to avoid one call per name while still keeping the name order
    def get_table_schemas(self, names):
        proto_tableschemas = boxes_pb2.TableSchemas(table_schemas=[])
        i=0
        while i < len(names):
            c = self.table_to_connector[names[i]]
            names_for_connector = [names[i]]

            i = i+1
            while i < len(names) and self.table_to_connector[names[i]] == c:
                names_for_connector.append(names[i])
                i = i+1

            new_proto_tableschemas = c.GetTableSchemas(boxes_pb2.TableNames(table_names=names_for_connector))
            proto_tableschemas.table_schemas.extend(new_proto_tableschemas.table_schemas)

        return proto_tableschemas

    def get_table(self, name):
        c = self.table_to_connector[name]
        t = c.GetTable(boxes_pb2.TableName(name=name))
        return t


    def average(self, values):
        response = self.alg_service.Average(boxes_pb2.DoubleList(values=values))
        return response.value



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

    de = DataEngine()


    # For testing
    names = de.get_table_names()
    print(names)

    pts = de.get_table_schemas(names)

    for n,ps in zip(names,pts.table_schemas):
        pt = de.get_table(n)
        df = prototable_to_df(ps, pt)
        print(df)

        print('')
        for key in ['Totalt antal simtag', 'Längder']:
            print('Average of %s: %f' % (key, de.average(df[key])))
        print('\n')


    # -----------
    '''
    port = random.randint(50000, 59000)
    name = 'DataEngineService'

    consul_register(name, port)
    serve(port)
    consul_unregister(name, port)
    '''
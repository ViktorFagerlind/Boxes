import grpc

from common import boxes_pb2_grpc
from common import boxes_pb2
from common.consul_services import consul_find_service


class ConnectorManager:
    def __init__(self):
        self.connectors = []
        self.name_to_connector = {}
        self.table_to_connector = {}

        self.__setup_connectors()
        print('All available tables:\n{}'.format('\n'.join(self.get_table_names())))

    def __setup_connectors(self):
        service_name = 'Connector'
        (ip, ports) = consul_find_service(service_name)

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

    def is_table_present(self, table_name):
        return table_name in self.get_table_names()

    def get_table_schema(self, name):
        return self.get_table_schemas([name]).table_schemas[0]

    def get_table_schemas(self, names):
        proto_tableschemas = boxes_pb2.TableSchemas(table_schemas=[])
        i = 0
        while i < len(names):
            c = self.table_to_connector[names[i]]
            names_for_connector = [names[i]]

            i = i + 1
            while i < len(names) and self.table_to_connector[names[i]] == c:
                names_for_connector.append(names[i])
                i = i + 1

            new_proto_tableschemas = c.GetTableSchemas(boxes_pb2.TableNames(table_names=names_for_connector))
            proto_tableschemas.table_schemas.extend(new_proto_tableschemas.table_schemas)

        return proto_tableschemas

    def get_table(self, name):
        c = self.table_to_connector[name]
        t = c.GetTable(boxes_pb2.TableName(name=name))
        return t

import argparse
import grpc

from prompt_toolkit import prompt
from common import boxes_pb2_grpc, boxes_pb2
from common.df_prototables import prototable_to_df
from common.consul_services import consul_find_service

def setup_connection():
    service_name = 'DataEngineService'
    (ip, ports) = consul_find_service(service_name)

    channel = grpc.insecure_channel(ip + ':' + str(ports[0]))
    return boxes_pb2_grpc.DataEngineStub(channel)


def execute_and_print(query):
    for stm in query.split(';'):
        column_types = []
        result_table = c.ExecuteQuery(boxes_pb2.Query(q=stm, column_types=column_types))

        column_schemas = []
        for i in range(len(result_table.columns)):
            column_schemas.append(boxes_pb2.ColumnSchema(name='col {}'.format(i),type=column_types[i] if i < len(column_types) else boxes_pb2.ColumnType.STRING))
        result_schema = boxes_pb2.TableSchema(column_schemas=column_schemas)
        print (prototable_to_df(schema=result_schema, table=result_table))

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--prompt', help="Use promt", action="store_true")
parser.add_argument('-s', '--select', help="Select query to execute and print. E.g. \"SELECT avg_cadence, "
                                           "total_distance, timestamp from \'5129419239#swim_lengths\'\"")
args = parser.parse_args()

c = setup_connection()

if args.prompt:
    while True:
        try:
            input = prompt('> ')
            execute_and_print(input)
        except KeyboardInterrupt:
            print('User aborted...')
            break
        except Exception as e:
            print('Caught exception {}:'.format(e))
elif args.select is not None:
    execute_and_print(args.select)



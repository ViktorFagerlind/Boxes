import argparse
import grpc
import matplotlib.pyplot as plt
import pandas as pd
import yaml

from prompt_toolkit import prompt
from common import boxes_pb2_grpc, boxes_pb2
from common.df_prototables import prototable_to_df
from common.consul_services import consul_find_service

def setup_connection():
    service_name = 'DataEngineService'
    #(ip, ports) = consul_find_service(service_name)
    ip = 'vfhome.asuscomm.com' #'127.0.0.1'
    ports = [51234]

    channel = grpc.insecure_channel(ip + ':' + str(ports[0]))
    return boxes_pb2_grpc.DataEngineStub(channel)


def execute_query(connection, query, column_types=[], column_names=[]):
    for stm in query.split(';'):
        result_table = connection.ExecuteQuery(boxes_pb2.Query(q=stm, column_types=column_types))

        column_schemas = []
        for i in range(len(result_table.columns)):
            name = column_names[i] if i < len(column_names) else 'col {}'.format(i)
            column_schemas.append(boxes_pb2.ColumnSchema(name=name,type=column_types[i] if i < len(column_types) else boxes_pb2.ColumnType.TEXT))
        result_schema = boxes_pb2.TableSchema(column_schemas=column_schemas)

        return  prototable_to_df(schema=result_schema, table=result_table)

def name_to_enum(name):
    for e in boxes_pb2.ColumnType.items():
        if name == e[0]:
            return e[1]
    return boxes_pb2.ColumnType.UNUSED


def plot_config(connection, plot_config):
    column_types = []
    column_names = []
    for columndef in plot_config['columns']:
        column_types.append(name_to_enum(columndef['type']))
        column_names.append(columndef['name'])

    df = execute_query(connection, query=plot_config['query'], column_types=column_types, column_names=column_names)
    print(df)

    ax = plt.gca()
    for plot in plot_config['plots']:
        df.plot(kind=plot['kind'], x=plot_config['x-axis'], y=plot['y-axis'], ax=ax, color=plot['color'])


def draw_predefined_plot(connection, names):
    filename = r'../input/plots.yaml'
    with open(filename) as file:
        plot_configs = yaml.full_load(file)

        if names == 'all':
            for cfg in plot_configs.values():
                plot_config(connection, cfg)
        else:
            namelist = names.split(',')
            for name in namelist:
                plot_config(connection, plot_configs[name])

        plt.show()


parser = argparse.ArgumentParser()
parser.add_argument('-p', '--prompt', help="Use promt", action="store_true")
parser.add_argument('-d', '--draw',   help="Draw predefined plot")
parser.add_argument('-s', '--select', help="Select query to execute and print. E.g. \"SELECT avg_cadence, "
                                           "total_distance, timestamp from \'5129419239#swim_lengths\'\"")
args = parser.parse_args()

c = setup_connection()

if args.prompt:
    while True:
        try:
            input = prompt('> ')
            df = execute_query(c, input)
            print(df)

        except KeyboardInterrupt:
            print('User aborted...')
            break
        except Exception as e:
            print('Caught exception {}:'.format(e))
else:
    if args.select is not None:
        df = execute_query(c, args.select)
        print(df)

    if args.draw is not None:
        draw_predefined_plot(c, args.draw)



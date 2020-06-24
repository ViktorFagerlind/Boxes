import logging
import argparse

from data_engine.data_engine import DataEngine

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

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test',   help="Test mode", action="store_true")
    parser.add_argument('-s', '--select', help="Select query to execute and print. E.g. \"SELECT avg_cadence, "
                                               "total_distance, timestamp from \'5129419239#swim_lengths\'\"")
    args = parser.parse_args()

    de = DataEngine()

    if args.test:
        de.create_all_tables()
        if args.select is not None:
            de.print_select_query(args.select)

    # -----------
    '''
    port = random.randint(50000, 59000)
    name = 'DataEngineService'

    consul_register(name, port)
    serve(port)
    consul_unregister(name, port)
    '''
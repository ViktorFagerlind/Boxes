import argparse
import grpc
from prompt_toolkit import prompt


from common import boxes_pb2_grpc, boxes_pb2
from common.consul_services import consul_find_service

def setup_connection():
    service_name = 'DataEngineService'
    (ip, ports) = consul_find_service(service_name)

    channel = grpc.insecure_channel(ip + ':' + str(ports[0]))
    return boxes_pb2_grpc.DataEngineStub(channel)


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
            for stm in input.split(';'):
                c.ExecuteQuery(boxes_pb2.Query(q=stm))
        except KeyboardInterrupt:
            print('User aborted...')
            break
elif args.select is not None:
    for stm in args.select.split(';'):
        c.ExecuteQuery(boxes_pb2.Query(q=stm))



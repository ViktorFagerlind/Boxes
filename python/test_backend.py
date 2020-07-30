import grpc

from common import boxes_pb2_grpc, boxes_pb2

def setup_connection():
    ip = '127.0.0.1'
    ports = [50051]

    channel = grpc.insecure_channel(ip + ':' + str(ports[0]))
    return boxes_pb2_grpc.BackendStub(channel)

connection = setup_connection()
reply = connection.Initialise (boxes_pb2.ConfigFile(yamlPath='/test/what.yaml'))
print (reply)

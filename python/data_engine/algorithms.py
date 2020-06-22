import grpc

from common import boxes_pb2_grpc
from common import boxes_pb2
from common.consul_services import consul_find_service


class Algorithms:
    def __init__(self):
        self.__setup_algorithms()


    def __setup_algorithms(self):
        service_name = 'Algorithms'
        (ip,ports) = consul_find_service(service_name)

        channel = grpc.insecure_channel(ip + ':' + str(ports[0]))
        self.alg_service = boxes_pb2_grpc.AlgorithmsStub(channel)


    def average(self, values):
        response = self.alg_service.Average(boxes_pb2.DoubleList(values=values))
        return response.value

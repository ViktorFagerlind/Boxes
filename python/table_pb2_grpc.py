# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import table_pb2 as table__pb2


class TableQueryStub(object):
    """
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetTable = channel.unary_unary(
                '/tableservices.TableQuery/GetTable',
                request_serializer=table__pb2.Query.SerializeToString,
                response_deserializer=table__pb2.Table.FromString,
                )


class TableQueryServicer(object):
    """
    """

    def GetTable(self, request, context):
        """
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_TableQueryServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetTable': grpc.unary_unary_rpc_method_handler(
                    servicer.GetTable,
                    request_deserializer=table__pb2.Query.FromString,
                    response_serializer=table__pb2.Table.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'tableservices.TableQuery', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class TableQuery(object):
    """
    """

    @staticmethod
    def GetTable(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tableservices.TableQuery/GetTable',
            table__pb2.Query.SerializeToString,
            table__pb2.Table.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)


class AlgorithmsStub(object):
    """
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Average = channel.unary_unary(
                '/tableservices.Algorithms/Average',
                request_serializer=table__pb2.DoubleList.SerializeToString,
                response_deserializer=table__pb2.DoubleValue.FromString,
                )


class AlgorithmsServicer(object):
    """
    """

    def Average(self, request, context):
        """
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AlgorithmsServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Average': grpc.unary_unary_rpc_method_handler(
                    servicer.Average,
                    request_deserializer=table__pb2.DoubleList.FromString,
                    response_serializer=table__pb2.DoubleValue.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'tableservices.Algorithms', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Algorithms(object):
    """
    """

    @staticmethod
    def Average(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tableservices.Algorithms/Average',
            table__pb2.DoubleList.SerializeToString,
            table__pb2.DoubleValue.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

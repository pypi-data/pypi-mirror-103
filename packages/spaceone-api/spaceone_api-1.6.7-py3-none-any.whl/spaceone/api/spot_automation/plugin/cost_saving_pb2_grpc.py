# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from spaceone.api.spot_automation.plugin import cost_saving_pb2 as spaceone_dot_api_dot_spot__automation_dot_plugin_dot_cost__saving__pb2


class CostSavingStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.get = channel.unary_unary(
                '/spaceone.api.spot_automation.plugin.CostSaving/get',
                request_serializer=spaceone_dot_api_dot_spot__automation_dot_plugin_dot_cost__saving__pb2.CostSavingRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_spot__automation_dot_plugin_dot_cost__saving__pb2.CostSavingInfo.FromString,
                )


class CostSavingServicer(object):
    """Missing associated documentation comment in .proto file."""

    def get(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_CostSavingServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'get': grpc.unary_unary_rpc_method_handler(
                    servicer.get,
                    request_deserializer=spaceone_dot_api_dot_spot__automation_dot_plugin_dot_cost__saving__pb2.CostSavingRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_spot__automation_dot_plugin_dot_cost__saving__pb2.CostSavingInfo.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'spaceone.api.spot_automation.plugin.CostSaving', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class CostSaving(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def get(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.spot_automation.plugin.CostSaving/get',
            spaceone_dot_api_dot_spot__automation_dot_plugin_dot_cost__saving__pb2.CostSavingRequest.SerializeToString,
            spaceone_dot_api_dot_spot__automation_dot_plugin_dot_cost__saving__pb2.CostSavingInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from speechly.slu.v1 import wlu_pb2 as speechly_dot_slu_dot_v1_dot_wlu__pb2


class WLUStub(object):
  """Service that implements Speechly WLU (Written Language Understanding).

  To use this service you MUST use an access token from Speechly Identity API.
  The token MUST be passed in gRPC metadata with `Authorization` key and `Bearer $ACCESS_TOKEN` as value, e.g. in Go:

  ```
  ctx := context.Background()
  ctx = metadata.AppendToOutgoingContext(ctx, "Authorization", "Bearer "+accessToken)
  res, err := speechlyWLUClient.Text(ctx, req)
  ```
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.Text = channel.unary_unary(
        '/speechly.slu.v1.WLU/Text',
        request_serializer=speechly_dot_slu_dot_v1_dot_wlu__pb2.WLURequest.SerializeToString,
        response_deserializer=speechly_dot_slu_dot_v1_dot_wlu__pb2.WLUResponse.FromString,
        )


class WLUServicer(object):
  """Service that implements Speechly WLU (Written Language Understanding).

  To use this service you MUST use an access token from Speechly Identity API.
  The token MUST be passed in gRPC metadata with `Authorization` key and `Bearer $ACCESS_TOKEN` as value, e.g. in Go:

  ```
  ctx := context.Background()
  ctx = metadata.AppendToOutgoingContext(ctx, "Authorization", "Bearer "+accessToken)
  res, err := speechlyWLUClient.Text(ctx, req)
  ```
  """

  def Text(self, request, context):
    """Performs recognition of a text with specified language.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_WLUServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'Text': grpc.unary_unary_rpc_method_handler(
          servicer.Text,
          request_deserializer=speechly_dot_slu_dot_v1_dot_wlu__pb2.WLURequest.FromString,
          response_serializer=speechly_dot_slu_dot_v1_dot_wlu__pb2.WLUResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'speechly.slu.v1.WLU', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))

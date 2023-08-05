# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from speechly.slu.v1 import slu_pb2 as speechly_dot_slu_dot_v1_dot_slu__pb2


class SLUStub(object):
  """Service that implements Speechly SLU (Spoken Language Understanding) API.

  To use this service you MUST use an access token from Speechly Identity API.
  The token MUST be passed in gRPC metadata with `Authorization` key and `Bearer $ACCESS_TOKEN` as value, e.g. in Go:

  ```
  ctx := context.Background()
  ctx = metadata.AppendToOutgoingContext(ctx, "Authorization", "Bearer "+accessToken)
  stream, err := speechlySLUClient.Stream(ctx)
  ```
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.Stream = channel.stream_stream(
        '/speechly.slu.v1.SLU/Stream',
        request_serializer=speechly_dot_slu_dot_v1_dot_slu__pb2.SLURequest.SerializeToString,
        response_deserializer=speechly_dot_slu_dot_v1_dot_slu__pb2.SLUResponse.FromString,
        )


class SLUServicer(object):
  """Service that implements Speechly SLU (Spoken Language Understanding) API.

  To use this service you MUST use an access token from Speechly Identity API.
  The token MUST be passed in gRPC metadata with `Authorization` key and `Bearer $ACCESS_TOKEN` as value, e.g. in Go:

  ```
  ctx := context.Background()
  ctx = metadata.AppendToOutgoingContext(ctx, "Authorization", "Bearer "+accessToken)
  stream, err := speechlySLUClient.Stream(ctx)
  ```
  """

  def Stream(self, request_iterator, context):
    """Performs bidirectional streaming speech recognition: receive results while sending audio.

    First request MUST be an SLUConfig message with the configuration that describes the audio format being sent.

    This RPC can handle multiple logical audio segments with the use of `SLUEvent_START` and `SLUEvent_STOP` messages,
    which are used to indicate the beginning and the end of a segment.

    A typical call timeline will look like this:

    1. Client starts the RPC.
    2. Client sends `SLUConfig` message with audio configuration.
    3. Client sends `SLUEvent.START`.
    4. Client sends audio and receives responses from the server.
    5. Client sends `SLUEvent.STOP`.
    6. Client sends `SLUEvent.START`.
    7. Client sends audio and receives responses from the server.
    8. Client sends `SLUEvent.STOP`.
    9. Client closes the stream and receives responses from the server until EOF is received.

    NB: the client does not have to wait until the server acknowledges the start / stop events,
    this is done asynchronously. The client can deduplicate responses based on the audio context ID,
    which will be present in every response message.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_SLUServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'Stream': grpc.stream_stream_rpc_method_handler(
          servicer.Stream,
          request_deserializer=speechly_dot_slu_dot_v1_dot_slu__pb2.SLURequest.FromString,
          response_serializer=speechly_dot_slu_dot_v1_dot_slu__pb2.SLUResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'speechly.slu.v1.SLU', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))

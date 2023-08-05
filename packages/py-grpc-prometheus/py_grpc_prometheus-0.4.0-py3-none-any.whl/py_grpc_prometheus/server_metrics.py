from prometheus_client import Counter
from prometheus_client import Histogram

GRPC_SERVER_STARTED_COUNTER = Counter(
    "grpc_server_started_total",
    "Total number of RPCs started on the server.",
    ["grpc_type", "grpc_service", "grpc_method"])

GRPC_SERVER_STREAM_MSG_RECEIVED = Counter(
    "grpc_server_msg_received_total",
    "Total number of RPC stream messages received on the server.",
    ["grpc_type", "grpc_service", "grpc_method"])

GRPC_SERVER_STREAM_MSG_SENT = Counter(
    "grpc_server_msg_sent_total",
    "Total number of gRPC stream messages sent by the server.",
    ["grpc_type", "grpc_service", "grpc_method"])

GRPC_SERVER_HANDLED_HISTOGRAM = Histogram(
    "grpc_server_handling_seconds",
    "Histogram of response latency (seconds) of gRPC that had been application-level "
    "handled by the server.",
    ["grpc_type", "grpc_service", "grpc_method"])


# Legacy metrics for backward compatibility
def get_grpc_server_handled_counter(is_legacy):
  if is_legacy:
    return Counter(
        "grpc_server_handled_total",
        "Total number of RPCs completed on the server, regardless of success or failure.",
        ["grpc_type", "grpc_service", "grpc_method", "code"])
  return Counter(
      "grpc_server_handled_total",
      "Total number of RPCs completed on the server, regardless of success or failure.",
      ["grpc_type", "grpc_service", "grpc_method", "grpc_code"])


LEGACY_GRPC_SERVER_HANDLED_LATENCY_SECONDS = Histogram(
    "grpc_server_handled_latency_seconds",
    "Histogram of response latency (seconds) of gRPC that had been "
    "application-level handled by the server",
    ["grpc_type", "grpc_service", "grpc_method"])

import sys
import os

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/fraud_detection'))
sys.path.insert(0, utils_path)
import fraud_detection_pb2
import fraud_detection_pb2_grpc

import grpc
from concurrent import futures

class FraudDetectionServicer(fraud_detection_pb2_grpc.FraudDetectionServicer):
    def CheckFraud(self, request, context):
        total_amount = sum(request.order_amounts)
        if len(request.order_amounts) > 3 and total_amount > 500:  # Simple fraud detection logic
            return fraud_detection_pb2.FraudCheckResponse(is_fraudulent=True, reason="Multiple high-value orders")
        else:
            return fraud_detection_pb2.FraudCheckResponse(is_fraudulent=False, reason="No fraud detected")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    fraud_detection_pb2_grpc.add_FraudDetectionServicer_to_server(FraudDetectionServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
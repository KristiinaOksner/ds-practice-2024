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

class FraudDetectionServicer(fraud_detection_pb2_grpc.FraudDetectionServiceServicer):
    def CheckFraud(self, request, context):
        country = request.country
        city = request.city
        
        # Perform updated fraud detection logic based on country and city
        is_fraudulent, reason = self.detect_fraud(country, city)
        
        return fraud_detection_pb2.FraudDetectionResponse(is_fraudulent=is_fraudulent, reason=reason)

    def detect_fraud(self, country, city):
        # Updated fraud detection logic: Transactions from 'Thailand' and 'Bangkok' are considered fraudulent
        if country.lower() == 'thailand' and city.lower() == 'bangkok':
            return True, "Transactions from Bangkok, Thailand are considered fraudulent."
        
        return False, "Transaction is not considered fraudulent."

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    fraud_detection_pb2_grpc.add_FraudDetectionServiceServicer_to_server(
        FraudDetectionServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
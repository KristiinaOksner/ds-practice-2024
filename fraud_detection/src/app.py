import sys
import os
import logging

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
    def CheckFraudUser(self, request, context):
        if request.user.name.lower() in ['coco', 'alex', 'monica']:
            logging.info('User %s is considered fraudulent.', request.user.name)
            return fraud_detection_pb2.FraudDetectionResponse(is_fraudulent=True, reason='The user is considered fraudulent.')
        else:
            logging.info('User %s is not considered fraudulent.', request.user.name)
            return fraud_detection_pb2.FraudDetectionResponse(is_fraudulent=False, reason='The user is not fraudulent.')

    def CheckFraudCreditCard(self, request, context):
        if request.creditCard.number.count('8') == 6:
            logging.info('Credit card %s is considered fraudulent.', request.creditCard.number)
            return fraud_detection_pb2.FraudDetectionResponse(is_fraudulent=True, reason='The credit card is considered fraudulent.')
        else:
            logging.info('Credit card %s is not considered fraudulent.', request.creditCard.number)
            return fraud_detection_pb2.FraudDetectionResponse(is_fraudulent=False, reason='The credit card is not fraudulent.')

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    fraud_detection_pb2_grpc.add_FraudDetectionServiceServicer_to_server(FraudDetectionServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    logging.info("Fraud Detection Service started. Listening on port 50051.")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
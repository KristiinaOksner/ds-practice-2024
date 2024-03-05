# Importing necessary libraries
from concurrent import futures
import grpc
import sys
import os

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/transaction_verification'))
sys.path.insert(0, utils_path)
import transaction_verification_pb2
import transaction_verification_pb2_grpc

class TransactionVerificationService(transaction_verification_pb2_grpc.TransactionVerificationServiceServicer):
    def VerifyTransaction(self, request, context):
        items = request.items
        user = request.user
        credit_card = request.creditCard

        is_valid = True
        message = ""

        # check if credit card number is 16
        if len(credit_card.number) != 16:
            is_valid = False
            message = "Invalid credit card number length. Must be 16 digits."

        # check if credit card expirtation data is after 2025
        if credit_card.expirationDate < "25":
            is_valid = False
            message = "Invalid expiration date. Must be 25 or later."

        return transaction_verification_pb2.TransactionVerificationResponse(is_valid=is_valid, message=message)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    transaction_verification_pb2_grpc.add_TransactionVerificationServiceServicer_to_server(
        TransactionVerificationService(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
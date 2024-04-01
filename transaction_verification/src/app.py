# Importing necessary libraries
from ast import List
from concurrent import futures
import grpc
import sys
import os
import datetime
import logging

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/transaction_verification'))
sys.path.insert(0, utils_path)
import transaction_verification_pb2
import transaction_verification_pb2_grpc

import datetime

class TransactionVerificationService(transaction_verification_pb2_grpc.TransactionVerificationServiceServicer):
    def VerifyUser(self, request, context):
        user = request.user
        if not user.name or not user.contact:
            logging.info("User %s information is incomplete", user)
            return transaction_verification_pb2.TransactionVerificationResponse(is_valid=False, message="User information is incomplete")
        else:
            logging.info("User %s information is valid", user)
            return transaction_verification_pb2.TransactionVerificationResponse(is_valid=True, message="User information is valid")

    def VerifyCreditCard(self, request, context):
        credit_card = request.creditCard
        if not credit_card.number or not credit_card.expirationDate or not credit_card.cvv:
            logging.info("Credit card %s information is incomplete", credit_card)
            return transaction_verification_pb2.TransactionVerificationResponse(is_valid=False, message="Credit card information is incomplete")
        else:
            logging.info("Credit card %s information is valid", credit_card)
            return transaction_verification_pb2.TransactionVerificationResponse(is_valid=True, message="Credit card information is valid")

    def VerifyCreditCardInvalid(self, request, context):
        credit_card = request.creditCard.expirationDate
        exp_date = datetime.strptime(credit_card, "%Y-%m")
        if datetime.now().date() >= exp_date.date():
            logging.info("Credit card date %s has expired", exp_date)
            return transaction_verification_pb2.TransactionVerificationResponse(is_valid=False, message="Credit card has expired")
        else:
            logging.info("Credit card date %s is valid", exp_date)
            return transaction_verification_pb2.TransactionVerificationResponse(is_valid=True, message="Invalid credit card expiration date")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    transaction_verification_pb2_grpc.add_TransactionVerificationServiceServicer_to_server(TransactionVerificationService(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    logging.info("Transaction Verification Service started, running on port 50052")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
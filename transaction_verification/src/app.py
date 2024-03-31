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
<<<<<<< Updated upstream

    def _is_books_empty(self, items: List[transaction_verification_pb2.Item]) -> bool:
        return not items or len(items) == 0

    def _is_user_data_empty(self, user: transaction_verification_pb2.User) -> bool:
        return not user.name or not user.contact

    def _is_credit_card_format_correct(self, creditCard: transaction_verification_pb2.CreditCard) -> bool:
        return len(creditCard.number) > 0 and len(creditCard.expirationDate) > 0 and len(creditCard.cvv) > 0
    
    def IsBooksEmpty(self, request: transaction_verification_pb2.ListOfItems, context) -> transaction_verification_pb2.BoolResponse:
        is_empty = self._is_books_empty(request.items)
        return transaction_verification_pb2.BoolResponse(result=is_empty, message="")

    def IsUserDataEmpty(self, request: transaction_verification_pb2.User, context) -> transaction_verification_pb2.BoolResponse:
        is_empty = self._is_user_data_empty(request)
        return transaction_verification_pb2.BoolResponse(result=is_empty, message="")
    def IsCreditCardFormatCorrect(self, request: transaction_verification_pb2.CreditCard, context) -> transaction_verification_pb2.BoolResponse:
        is_correct = self._is_credit_card_format_correct(request)
        return transaction_verification_pb2.BoolResponse(result=is_correct, message="")
    def VerifyTransaction(self, request: transaction_verification_pb2.TransactionVerificationRequest, context) -> transaction_verification_pb2.TransactionVerificationResponse:

        if self._is_books_empty(request.items):
            return transaction_verification_pb2.TransactionVerificationResponse(is_valid=False, message="Book list cannot be empty.")

        if self._is_user_data_empty(request.user):
            return transaction_verification_pb2.TransactionVerificationResponse(is_valid=False, message="User data cannot be empty.")

        if not self._is_credit_card_format_correct(request.creditCard):
            return transaction_verification_pb2.TransactionVerificationResponse(is_valid=False, message="Invalid credit card format.")

        try:
            from datetime import datetime, timedelta
            exp_date = datetime.strptime(request.creditCard.expirationDate, "%Y-%m")
            if datetime.now().date() >= exp_date.date():
                return transaction_verification_pb2.TransactionVerificationResponse(is_valid=False, message="Credit card has expired.")
        except ValueError:
            return transaction_verification_pb2.TransactionVerificationResponse(is_valid=False, message="Invalid credit card expiration date format.")
        
        return transaction_verification_pb2.TransactionVerificationResponse(is_valid=True, message="Transaction verification successful.")
=======
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
>>>>>>> Stashed changes

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    transaction_verification_pb2_grpc.add_TransactionVerificationServiceServicer_to_server(
        TransactionVerificationService(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    logging.info("Transaction VerificationService running on port 50052")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
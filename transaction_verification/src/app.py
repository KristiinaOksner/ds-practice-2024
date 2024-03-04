# Importing necessary libraries
from concurrent import futures
import grpc
import transaction_verification_pb2
import transaction_verification_pb2_grpc

# Define the transaction verification service logic
class TransactionVerificationServicer(transaction_verification_pb2_grpc.TransactionVerificationServicer):
    def VerifyTransaction(self, request, context):
        # Simple logic to check if the transaction is valid
        if not request.items:
            return transaction_verification_pb2.TransactionVerificationResponse(
                is_valid=False,
                message="Items list is empty"
            )
        
        if not request.user.name or not request.user.contact or not request.credit_card.number:
            return transaction_verification_pb2.TransactionVerificationResponse(
                is_valid=False,
                message="Required user data or credit card information is missing"
            )

        # Perform credit card format validation (simple example)
        if not is_valid_credit_card(request.credit_card.number):
            return transaction_verification_pb2.TransactionVerificationResponse(
                is_valid=False,
                message="Invalid credit card number format"
            )

        # Other custom validation checks can be added here
        
        # If all checks pass, the transaction is considered valid
        return transaction_verification_pb2.TransactionVerificationResponse(
            is_valid=True,
            message="Transaction is valid"
        )

# Helper function to validate credit card number format
def is_valid_credit_card(card_number):
    # Simple implementation to check if the card number is 16 digits
    return len(card_number) == 16 and card_number.isdigit()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    transaction_verification_pb2_grpc.add_TransactionVerificationServicer_to_server(TransactionVerificationServicer(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
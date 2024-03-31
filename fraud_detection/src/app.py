import sys
import os

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/fraud_detection'))
sys.path.insert(0, utils_path)
import fraud_detection_pb2 as fraud_detection
import fraud_detection_pb2_grpc as fraud_detection_grpc

import grpc
from concurrent import futures

<<<<<<< Updated upstream
<<<<<<< Updated upstream
# Create a class to define the server functions, derived from
# fraud_detection_pb2_grpc.HelloServiceServicer
class HelloService(fraud_detection_grpc.HelloServiceServicer):
    # Create an RPC function to say hello
    def SayHello(self, request, context):
        # Create a HelloResponse object
        response = fraud_detection.HelloResponse()
        # Set the greeting field of the response object
        response.greeting = "Hello, " + request.name
        # Print the greeting message
        print(response.greeting)
        # Return the response object
        return response

def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    # Add HelloService
    fraud_detection_grpc.add_HelloServiceServicer_to_server(HelloService(), server)
    # Listen on port 50051
    port = "50051"
    server.add_insecure_port("[::]:" + port)
    # Start the server
=======
class FraudDetectionService(fraud_detection_pb2_grpc.FraudDetectionServiceServicer):

    def _is_user_data_fraudulent(self, user: fraud_detection_pb2.User) -> bool:
        fraudulent_names = ["alex", "coco", "monica"]
        return user.name.lower() in fraudulent_names

    def _is_credit_card_fraudulent(self, creditCard: fraud_detection_pb2.CreditCard) -> bool:
        return '8888' in creditCard.number
    def CheckFraud(self, request: fraud_detection_pb2.FraudDetectionRequest, context) -> fraud_detection_pb2.FraudDetectionResponse:
        fraudulent_user = self._is_user_data_fraudulent(request.user)
        fraudulent_card = self._is_credit_card_fraudulent(request.creditCard)

        is_bangkok_address = request.billingAddress.country == "Thailand" and request.billingAddress.city == "Bangkok"

        if fraudulent_user or fraudulent_card or is_bangkok_address:
            reason_message = ""
            if fraudulent_user:
                reason_message += "User data is flagged as fraudulent. "
            if fraudulent_card:
                reason_message += "Credit card data is flagged as fraudulent. "
            if is_bangkok_address:
                reason_message += "Billing address is in Bangkok, Thailand as fraudulent."

            return fraud_detection_pb2.FraudDetectionResponse(is_fraudulent=True, reason=reason_message)
        else:
            return fraud_detection_pb2.FraudDetectionResponse(is_fraudulent=False, reason="No fraud detected.")
=======
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
>>>>>>> Stashed changes

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    fraud_detection_pb2_grpc.add_FraudDetectionServiceServicer_to_server(
        FraudDetectionService(), server)
    server.add_insecure_port('[::]:50051')
>>>>>>> Stashed changes
    server.start()
    print("Server started. Listening on port 50051.")
    # Keep thread alive
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
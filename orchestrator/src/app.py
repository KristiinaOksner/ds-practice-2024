import asyncio
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
import sys
import os
import logging
import threading
import uuid

logging.basicConfig(level=logging.INFO)

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/fraud_detection'))
sys.path.insert(0, utils_path)
import fraud_detection_pb2
import fraud_detection_pb2_grpc
utils_path_tansactionverification = os.path.abspath(os.path.join(FILE, '../../../utils/pb/transaction_verification'))
sys.path.insert(0, utils_path_tansactionverification)
import transaction_verification_pb2
import transaction_verification_pb2_grpc
utils_path_booksuggestions = os.path.abspath(os.path.join(FILE, '../../../utils/pb/book_suggestions'))
sys.path.insert(0, utils_path_booksuggestions)
import book_suggestions_pb2
import book_suggestions_pb2_grpc

utils_path_orderexecutor = os.path.abspath(os.path.join(FILE, '../../../utils/pb/orderexecutor'))
sys.path.insert(0, utils_path_orderexecutor)
import orderexecutor_pb2
import orderexecutor_pb2_grpc
utils_path_orderqueue = os.path.abspath(os.path.join(FILE, '../../../utils/pb/orderqueue'))
sys.path.insert(0, utils_path_orderqueue)
import orderqueue_pb2
import orderqueue_pb2_grpc

import grpc
# code for checkpoint2
def generate_unique_order_id():
    return str(uuid.uuid4())

# establish gRPC connection with five service
fraud_stub = fraud_detection_pb2_grpc.FraudDetectionServiceStub(grpc.insecure_channel('fraud_detection:50051'))
transaction_stub = transaction_verification_pb2_grpc.TransactionVerificationServiceStub(grpc.insecure_channel('transaction_verification:50052'))
suggestion_stub = book_suggestions_pb2_grpc.BookSuggestionsServiceStub(grpc.insecure_channel('book_suggestions:50053'))
orderqueue_stub = orderqueue_pb2_grpc.OrderQueueServiceStub(grpc.insecure_channel('orderqueue:50054'))
orderexecutor_stub = orderexecutor_pb2_grpc.OrderExecutorStub(grpc.insecure_channel('orderexecutor:50055'))

def verify_user(order):
    logging.info(f"Get User verification request for order #{order['id']}")
    update_vector_clock(service='transaction_verification', order_id=order['id'])
    user_verification_response = transaction_stub.VerifyUser(transaction_verification_pb2.TransactionVerificationRequest(user=order["user"]))
    logging.info(f"User verification response for order #{order['id']}: {user_verification_response}")
    if not user_verification_response.is_valid:
        handle_failure(order["id"], "User verification failed")
    return user_verification_response

def verify_credit_card(order):
    logging.info(f"Get Credit card verification request for order #{order['id']}")
    update_vector_clock(service='transaction_verification', order_id=order['id'])
    credit_card_verification_response = transaction_stub.VerifyCreditCard(transaction_verification_pb2.TransactionVerificationRequest(creditCard=order["creditCard"]))
    logging.info(f"Credit card verification response for order #{order['id']}: {credit_card_verification_response}")
    if not credit_card_verification_response.is_valid:
        handle_failure(order["id"], "Credit card verification failed")
    return credit_card_verification_response

def check_fraud_user(order):
    logging.info(f"Get Fraud user check request for order #{order['id']}")
    update_vector_clock(service='fraud_detection', order_id=order['id'])
    fraud_user_response = fraud_stub.CheckFraudUser(fraud_detection_pb2.FraudDetectionRequest(user=order["user"]))
    logging.info(f"Fraud user check response for order #{order['id']}: {fraud_user_response}")
    if fraud_user_response.is_fraudulent:
        handle_failure(order["id"], "Fraud user detected")
    return fraud_user_response

def verify_credit_card_invalid(order):
    logging.info(f"Get Credit card invalid check request for order #{order['id']}")
    update_vector_clock(service='transaction_verification', order_id=order['id'])
    credit_card_invalid_response = transaction_stub.VerifyCreditCardInvalid(transaction_verification_pb2.TransactionVerificationRequest(creditCard=order["creditCard"]))
    logging.info(f"Credit card invalid check response for order #{order['id']}: {credit_card_invalid_response}")
    if not credit_card_invalid_response.is_valid:
        handle_failure(order["id"], "Invalid credit card expiration date")
    return credit_card_invalid_response

def check_fraud_credit_card(order):
    logging.info(f"Get Fraud user check request for order #{order['id']}")
    update_vector_clock(service='fraud_detection', order_id=order['id'])
    fraud_credit_card_response = fraud_stub.CheckFraudCreditCard(fraud_detection_pb2.FraudDetectionRequest(creditCard=order["creditCard"]))
    logging.info(f"Fraud credit card check response for order #{order['id']}: {fraud_credit_card_response}")
    if fraud_credit_card_response.is_fraudulent:
        handle_failure(order["id"], "Fraud credit card detected")
    return fraud_credit_card_response

def get_book_suggestions(order):
    logging.info(f"Get Book suggestions request for order #{order['id']}")
    update_vector_clock(service='book_suggestions', order_id=order['id'])
    book_suggestions_response = suggestion_stub.GetBookSuggestions(book_suggestions_pb2.BookSuggestionsRequest(books=order["items"]))
    logging.info(f"Book suggestions for order #{order['id']}: {book_suggestions_response}")
    return book_suggestions_response

def handle_failure(order_id, message):
    logging.info(f"handle failure: {message} for {order_id}")
    # You can send a failure notification to the Flask application here
    # Stop all threads and respond to the user
    stop_threads()

def stop_threads():
    # Stop all worker threads
    logging.info("stop all worker threads")
    for thread in threading.enumerate():
        if thread != threading.current_thread():
            thread.join()

# Initialize vector clock for each order in each service
order_vector_clocks = {
    'fraud_detection': {},
    'transaction_verification': {},
    'book_suggestions': {}
}

def update_vector_clock(service, order_id):
    if order_id not in order_vector_clocks[service]:
        order_vector_clocks[service][order_id] = 1
    else:
        order_vector_clocks[service][order_id] += 1

    logging.info(f"Current vector clock for order #{order_id} in {service}: {order_vector_clocks[service][order_id]}")

def trigger_clear_data():
    final_vector_clock = max([max(vc.values()) for vc in order_vector_clocks.values()])
    # Broadcast final vector clock to all services for comparison
    # Implement the logic to compare local vector clocks and clear data if conditions are met
    for service, local_vector_clock in order_vector_clocks.items():
        if all(value <= final_vector_clock for value in local_vector_clock.values()):
            # seed the message to three services
            broadcast_clear_data_message(service, final_vector_clock)
        else:
            logging.error(f"error: {service} --- local vector clock:{local_vector_clock} final_vector_clock: {final_vector_clock}")
def broadcast_clear_data_message(service, final_vector_clock):
    logging.info(f"Broadcasting clear data message to all services")

    if service == 'fraud_detection':
        pass
        #fraud_clear_data_message = fraud_detection_pb2.ClearDataRequest(vector_clock=final_vector_clock)
        #fraud_stub.ClearData(fraud_clear_data_message)
    elif service == 'transaction_verification':
        pass
        #transaction_clear_data_message = transaction_verification_pb2.ClearDataRequest(vector_clock=final_vector_clock)
        #transaction_stub.ClearData(transaction_clear_data_message)
    elif service == 'book_suggestions':
        pass
        #suggestion_clear_data_message = book_suggestions_pb2.ClearDataRequest(vector_clock=final_vector_clock)
        #suggestion_stub.ClearData(suggestion_clear_data_message)
    else:
        logging.error(f"Unknown service: {service}")

# Import Flask.
# Flask is a web framework for Python.
# It allows you to build a web application quickly.
# For more information, see https://flask.palletsprojects.com/en/latest/
from flask import Flask, request
from flask_cors import CORS

# Create a simple Flask app.
app = Flask(__name__)
# Enable CORS for the app.
CORS(app)

@app.route('/checkout', methods=['POST'])
def checkout():
    loop = asyncio.get_event_loop()
    data = request.json

    orderId = generate_unique_order_id
    data["id"] = orderId

    # Initialize vector clocks for the order in each service
    for service in order_vector_clocks:
        order_vector_clocks[service][orderId] = 0

    # Create a ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=6) as executor:
        # Submit tasks to the executor in the desired order
        future_user = executor.submit(verify_user, data, order_vector_clocks['transaction_verification'][orderId])
        future_credit_card = executor.submit(verify_credit_card, data, order_vector_clocks['transaction_verification'][orderId])
        future_fraud_user = executor.submit(check_fraud_user, data, order_vector_clocks['fraud_detection'][orderId])
        future_credit_card_invalid = executor.submit(verify_credit_card_invalid, data, order_vector_clocks['transaction_verification'][orderId])
        future_fraud_credit_card = executor.submit(check_fraud_credit_card, data, order_vector_clocks['fraud_detection'][orderId])
        future_book_suggestions = executor.submit(get_book_suggestions, data, order_vector_clocks['book_suggestions'][orderId])

        # Get results from the futures
        user_result = future_user.result()
        credit_card_result = future_credit_card.result()
        fraud_user_result = future_fraud_user.result()
        credit_card_invalid_result = future_credit_card_invalid.result()
        fraud_credit_card_result = future_fraud_credit_card.result()
        book_suggestions_result = future_book_suggestions.result()

        # Process the final order based on the results
        order_status_response = {
            'orderId': orderId,
            'status': 'Failed',
            'reason': "",
            'message': ""
        }

        if user_result[0] and credit_card_result[0] and not fraud_user_result[0] and credit_card_invalid_result[0] and not fraud_credit_card_result[0]:
            order_status_response['status'] = 'Success'
            order_status_response['suggestedBooks'] = book_suggestions_result
        else:

            if not user_result[0]:
                order_status_response['message'] = user_result[1]
            elif not credit_card_result[0]:
                order_status_response['message'] = credit_card_result[1]
            if not credit_card_invalid_result[0]:
                order_status_response['message'] = credit_card_invalid_result[1]

            if fraud_user_result[0]:
                order_status_response['reason'] = fraud_user_result[1]
            if fraud_credit_card_result[0]:
                order_status_response['reason'] = fraud_credit_card_result[1]
        
        # Call function to broadcast and clear data
        trigger_clear_data()

    logging.info("Checkout process completed. Order status response: %s", order_status_response)
    return jsonify(order_status_response)

if __name__ == '__main__':
    # Run the app in debug mode to enable hot reloading.
    # This is useful for development.
    # The default port is 5000.
    app.run(host='0.0.0.0')

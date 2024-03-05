import sys
import os
import logging

logging.basicConfig(level=logging.INFO)

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/fraud_detection'))
sys.path.insert(0, utils_path)
import fraud_detection_pb2
import fraud_detection_pb2_grpc
utils_path_transactionverfication = os.path.abspath(os.path.join(FILE, '../../../utils/pb/transaction_verification'))
sys.path.insert(0, utils_path_transactionverfication)
import transaction_verification_pb2
import transaction_verification_pb2_grpc
utils_path_booksuggestions = os.path.abspath(os.path.join(FILE, '../../../utils/pb/book_suggestions'))
sys.path.insert(0, utils_path_booksuggestions)
import book_suggestions_pb2
import book_suggestions_pb2_grpc

import grpc
from concurrent import futures
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=3)

# Establish gRPC connection with fraud_detection service
def detect_fraud(country, city):
    logging.info("Received request to check fraud for country: %s, city: %s", country, city)
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = fraud_detection_pb2_grpc.FraudDetectionServiceStub(channel)
        response = stub.CheckFraud(fraud_detection_pb2.FraudDetectionRequest(country=country, city=city))
        logging.info("Fraud check completed. Is fraudulent: %s, Reason: %s", response.is_fraudulent, response.reason)
        return response.is_fraudulent, response.reason

# Establish gRPC connection with transaction_verification service
def verify_transaction(items, user, credit_card):
    logging.info("Received request to verify transaction with items: %s, user: %s, credit card: %s", items, user, credit_card)
    with grpc.insecure_channel('localhost:50052') as channel:
        stub = transaction_verification_pb2_grpc.TransactionVerificationServiceStub(channel)
        response = stub.VerifyTransaction(transaction_verification_pb2.TransactionVerificationRequest(items=items, user=user, creditCard=credit_card))
        logging.info("Transaction verification completed. Is valid: %s, Message: %s", response.is_valid, response.message)
        return response.is_valid, response.message

# Establish gRPC connection with book_suggestions service
def get_book_suggestions(books):
    logging.info("Received request to get book suggestions for books: %s", books)
    with grpc.insecure_channel('localhost:50053') as channel:
        stub = book_suggestions_pb2_grpc.BookSuggestionsServiceStub(channel)
        books_pb = [book_suggestions_pb2.Book(title=book['title'], author=book['author']) for book in books]
        response = stub.GetBookSuggestions(book_suggestions_pb2.BookSuggestionsRequest(books=books_pb))
        logging.info("Book suggestions fetched successfully")
        return [book.title for book in response.suggestions]

# asynchronous run detect_fraud
def async_detect_fraud(country, city):
    return executor.submit(detect_fraud, country, city)

# asynchronous run verify_transaction 
def async_verify_transaction(items, user, credit_card):
    return executor.submit(verify_transaction, items, user, credit_card)

# asynchronous run get_book_suggestions 
def async_get_book_suggestions(books):
    return executor.submit(get_book_suggestions, books)

# Import Flask.
# Flask is a web framework for Python.
# It allows you to build a web application quickly.
# For more information, see https://flask.palletsprojects.com/en/latest/
from flask import Flask, request, jsonify
from flask_cors import CORS

# Create a simple Flask app.
app = Flask(__name__)
# Enable CORS for the app.
CORS(app)

# Define a POST endpoint.
@app.route('/checkout', methods=['POST'])
def checkout():
    data = request.json
    logging.info("Received checkout request with data: %s", data)

    country = data.get('country')
    city = data.get('city')
    fraud_future = async_detect_fraud(country, city)

    items = data.get('items', [])
    user = data.get('user')
    credit_card = data.get('creditCard')
    transaction_future = async_verify_transaction(items, user, credit_card)

    fraud_result = fraud_future.result()
    transaction_result = transaction_future.result()

    if transaction_result[0] and not fraud_result[0]:
        book_data = data.get('books', [])
        book_list = [{'title': book['title'], 'author': book['author']} for book in book_data]
        book_future = async_get_book_suggestions(book_list)
        book_recommendations = book_future.result()

        order_status_response = {
            'orderId': data.get('orderId'),
            'status': 'Success',
            'suggestedBooks': book_recommendations
        }
    else:
        order_status_response = {
            'orderId': data.get('orderId'),
            'status': 'Failed',
            'reason': fraud_result[1],
            'message': transaction_result[1]
        }

    logging.info("Checkout process completed. Order status response: %s", order_status_response)
    return jsonify(order_status_response)


if __name__ == '__main__':
    # Run the app in debug mode to enable hot reloading.
    # This is useful for development.
    # The default port is 5000.
    app.run(host='0.0.0.0')

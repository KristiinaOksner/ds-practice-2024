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

# Establish gRPC connection with fraud_detection service
def detect_fraud(country, city):
    with grpc.insecure_channel('fraud_detection:50051') as channel:
        stub = fraud_detection_pb2_grpc.FraudDetectionServiceStub(channel)
        response = stub.CheckFraud(fraud_detection_pb2.FraudDetectionRequest(country=country, city=city))
        return response.is_fraudulent, response.reason

# Establish gRPC connection with transaction_verification service
def verify_transaction(items, user, credit_card):
    with grpc.insecure_channel('transaction_verification:50052') as channel:
        stub = transaction_verification_pb2_grpc.TransactionVerificationServiceStub(channel)
        response = stub.VerifyTransaction(transaction_verification_pb2.TransactionVerificationRequest(items=items, user=user, creditCard=credit_card))
        return response.is_valid, response.message

# Establish gRPC connection with book_suggestions service
def get_book_suggestions(books):
    with grpc.insecure_channel('book_suggestions:50053') as channel:
        stub = book_suggestions_pb2_grpc.BookSuggestionsServiceStub(channel)
        books_pb = [book_suggestions_pb2.Book(title=book['title'], author=book['author']) for book in books]
        response = stub.GetBookSuggestions(book_suggestions_pb2.BookSuggestionsRequest(books=books_pb))
        return [book.title for book in response.suggestions]

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

    country = data.get('country')
    city = data.get('city')
    is_fraudulent, reason = detect_fraud(country, city)

    items = data.get('items', [])
    user = data.get('user')
    credit_card = data.get('creditCard')
    is_valid_transaction, transaction_message = verify_transaction(items, user, credit_card)

    if is_valid_transaction and not is_fraudulent:
        order_status_response = {
            'orderId': data.get('orderId'),
            'status': 'Failed',
            'reason': reason,
            'message': transaction_message
        }
    else:
        book_data = data.get('books', [])
        book_list = [{'title': book['title'], 'author': book['author']} for book in book_data]
        book_recommendations = get_book_suggestions(book_list)

        order_status_response = {
            'orderId': data.get('orderId'),
            'status': 'Success',
            'suggestedBooks': book_recommendations
        }

    return jsonify(order_status_response)


if __name__ == '__main__':
    # Run the app in debug mode to enable hot reloading.
    # This is useful for development.
    # The default port is 5000.
    app.run(host='0.0.0.0')

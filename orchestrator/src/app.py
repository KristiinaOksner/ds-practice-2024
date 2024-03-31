import asyncio
from collections import defaultdict
import sys
import os
<<<<<<< Updated upstream
=======
import logging
import threading
import uuid

logging.basicConfig(level=logging.INFO)
>>>>>>> Stashed changes

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/fraud_detection'))
sys.path.insert(0, utils_path)
import fraud_detection_pb2 as fraud_detection
import fraud_detection_pb2_grpc as fraud_detection_grpc

import grpc

<<<<<<< Updated upstream
def greet(name='you'):
    # Establish a connection with the fraud-detection gRPC service.
    with grpc.insecure_channel('fraud_detection:50051') as channel:
        # Create a stub object.
        stub = fraud_detection_grpc.HelloServiceStub(channel)
        # Call the service through the stub object.
        response = stub.SayHello(fraud_detection.HelloRequest(name=name))
    return response.greeting
=======
# code for checkpoint2
def generate_unique_order_id():
        return str(uuid.uuid4())

class VectorClock:
    def __init__(self):
        self.value = defaultdict(int)

    def increment(self, node_id):
        self.value[node_id] += 1

    def merge(self, other_clock):
        for node, timestamp in other_clock.value.items():
            if timestamp > self.value[node]:
                self.value[node] = timestamp

    def compare(self, other_clock):
        pass

    def __str__(self):
        return f"VectorClock({self.value})"

class OrderCoordinator:
    def __init__(self):
        self.orders = defaultdict(lambda: {"data": None, "vector_clock": VectorClock()})
        self.lock = threading.Lock()

    async def handle_order(self, order_id, data):
        async with self.lock:
            self.orders[order_id]["data"] = data
            self.orders[order_id]["vector_clock"].increment(order_id)

    async def get_order(self, order_id):
        return self.orders[order_id]

class OrderProcessingService:
    def __init__(self, coordinator, fraud_detection_stub, transaction_stub, suggestion_stub):
        self.coordinator = coordinator
        self.fraud_detection_stub = fraud_detection_stub
        self.transaction_stub = transaction_stub
        self.suggestion_stub = suggestion_stub

    async def process_order(self, order_id, data):
        await self.coordinator.handle_order(order_id, data)

        # 异步等待所有服务完成操作
        fraud_task = asyncio.ensure_future(self.check_fraud(order_id))
        transaction_task = asyncio.ensure_future(self.verify_transaction(order_id))
        suggestion_task = asyncio.ensure_future(self.get_book_suggestions(order_id))
        
        fraud_result, transaction_result, book_suggestions = await asyncio.gather(fraud_task, transaction_task, suggestion_task)
    
        # Store results in the order_data dictionary
        order_data = await self.coordinator.get_order(order_id)
        order_data["fraud_detection_result"] = fraud_result
        order_data["transaction_verification_result"] = transaction_result
        order_data["book_suggestions"] = book_suggestions

    async def check_fraud(self, order_id):
        order_data = await self.coordinator.get_order(order_id)
        country = order_data["data"]["billingAddress"]["country"]
        city = order_data["data"]["billingAddress"]["city"]
        response = await self.fraud_detection_stub.CheckFraud(fraud_detection_pb2.FraudDetectionRequest(country=country, city=city))
        is_fraudulent, reason = response.is_fraudulent, response.reason
        # 更新向量时钟
        order_data["vector_clock"].increment("fraud_detection")
        return is_fraudulent, reason

    async def verify_transaction(self, order_id):
        order_data = await self.coordinator.get_order(order_id)
        items = [item_pb2.Item(item=item) for item in order_data["data"]["items"]]
        user = user_pb2.User(user=order_data["data"]["user"])
        credit_card = credit_card_pb2.CreditCard(card=order_data["data"]["creditCard"]) # 假设这里有对应的 protobuf 消息结构体
        response = await self.transaction_stub.VerifyTransaction(transaction_verification_pb2.TransactionVerificationRequest(items=items, user=user, creditCard=credit_card))
        is_valid, message = response.is_valid, response.message
        # 更新向量时钟
        order_data["vector_clock"].increment("transaction_verification")
        return is_valid, message

    async def get_book_suggestions(self, order_id):
        order_data = await self.coordinator.get_order(order_id)
        book_list = [book_suggestions_pb2.Book(title=book["title"], author=book["author"]) for book in order_data["data"]["items"]]
        response = await self.suggestion_stub.GetBookSuggestions(book_suggestions_pb2.BookSuggestionsRequest(books=book_list))
        suggestions = [book.title for book in response.suggestions]
        # 更新向量时钟
        order_data["vector_clock"].increment("book_suggestions")
        return suggestions

fraud_stub = fraud_detection_pb2_grpc.FraudDetectionServiceStub(grpc.insecure_channel('fraud_detection:50051'))
transaction_stub = transaction_verification_pb2_grpc.TransactionVerificationServiceStub(grpc.insecure_channel('transaction_verification:50052'))
suggestion_stub = book_suggestions_pb2_grpc.BookSuggestionsServiceStub(grpc.insecure_channel('book_suggestions:50053'))
coordinator = OrderCoordinator()
service = OrderProcessingService(coordinator, fraud_stub, transaction_stub, suggestion_stub)

# code for checkpoint2
>>>>>>> Stashed changes

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

# Define a GET endpoint.
@app.route('/', methods=['GET'])
def index():
    """
    Responds with 'Hello, [name]' when a GET request is made to '/' endpoint.
    """
    # Test the fraud-detection gRPC service.
    response = greet(name='orchestrator')
    # Return the response.
    return response

@app.route('/checkout', methods=['POST'])
<<<<<<< Updated upstream
def checkout():
    """
    Responds with a JSON object containing the order ID, status, and suggested books.
    """
    # Print request object data
    print("Request Data:", request.json)

    # Dummy response following the provided YAML specification for the bookstore
    order_status_response = {
        'orderId': '12345',
        'status': 'Order Approved',
        'suggestedBooks': [
            {'bookId': '123', 'title': 'Dummy Book 1', 'author': 'Author 1'},
            {'bookId': '456', 'title': 'Dummy Book 2', 'author': 'Author 2'}
        ]
    }

    return order_status_response
=======
async def checkout():
    loop = asyncio.get_event_loop()
    data = request.json
    order_id = generate_unique_order_id()
    data["orderId"] = order_id

    await service.process_order(data["orderId"], data)

    order_data = await coordinator.get_order(data["orderId"])
    fraud_result, transaction_result = order_data["fraud_detection_result"], order_data["transaction_verification_result"]
    book_recommendations = order_data["book_suggestions"]

    if transaction_result[0] and not fraud_result[0]:
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
>>>>>>> Stashed changes


if __name__ == '__main__':
    # Run the app in debug mode to enable hot reloading.
    # This is useful for development.
    # The default port is 5000.
    app.run(host='0.0.0.0')

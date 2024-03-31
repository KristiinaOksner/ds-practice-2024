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

utils_path_orderexecutor = os.path.abspath(os.path.join(FILE, '../../../utils/pb/orderexecutor'))
sys.path.insert(0, utils_path_orderexecutor)
import orderexecutor_pb2
import orderexecutor_pb2_grpc
utils_path_orderqueue = os.path.abspath(os.path.join(FILE, '../../../utils/pb/orderqueue'))
sys.path.insert(0, utils_path_orderqueue)
import orderqueue_pb2
import orderqueue_pb2_grpc

import grpc

<<<<<<< Updated upstream
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
=======
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

<<<<<<< Updated upstream
    await service.process_order(data["orderId"], data)

    order_data = await coordinator.get_order(data["orderId"])
    fraud_result, transaction_result = order_data["fraud_detection_result"], order_data["transaction_verification_result"]
    book_recommendations = order_data["book_suggestions"]

    if transaction_result[0] and not fraud_result[0]:
=======
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
>>>>>>> Stashed changes
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
>>>>>>> Stashed changes

if __name__ == '__main__':
    # Run the app in debug mode to enable hot reloading.
    # This is useful for development.
    # The default port is 5000.
    app.run(host='0.0.0.0')

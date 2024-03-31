from concurrent import futures
import grpc
import time
import logging

import orderexecutor_pb2
import orderexecutor_pb2_grpc

import sys
import os

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/orderexecutor'))
sys.path.insert(0, utils_path)
import queue

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class OrderExecutorServicer(orderexecutor_pb2_grpc.OrderExecutorServicer):
    def ExecuteOrder(self, request, context):
        order_id = request.order_id
        logging.info(f"Received order execution request for order ID: {order_id}")
        return orderexecutor_pb2.OrderResponse(message=f"Order {order_id} is being executed...")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    orderexecutor_pb2_grpc.add_OrderExecutorServicer_to_server(OrderExecutorServicer(), server)
    server.add_insecure_port('[::]:50055')
    server.start()
    logging.info("Server started. Listening on port 50051...")
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    serve()
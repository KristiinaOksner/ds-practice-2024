import logging
import grpc
from concurrent import futures
import random
import time

import sys
import os

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/orderqueue'))
sys.path.insert(0, utils_path)
import orderqueue_pb2
import orderqueue_pb2_grpc
import queue

class OrderQueueServicer(orderqueue_pb2_grpc.OrderQueueServiceServicer):

    def __init__(self):
        self.priority_queue = queue.PriorityQueue()
        self.normal_queue = queue.Queue()

    def EnqueueOrder(self, request, context):
        order = request.order

        order_value = calculate_order_value(order)
        self.priority_queue.put((order_value, order))

        return orderqueue_pb2.EnqueueOrderResponse(message="Order enqueued successfully")

    def DequeueOrder(self, request, context):
        if not self.priority_queue.empty():
            priority_order = self.priority_queue.get()[1]
            return orderqueue_pb2.DequeueOrderResponse(message=f"Dequeued priority order: {priority_order}")
        elif not self.normal_queue.empty():
            normal_order = self.normal_queue.get()
            return orderqueue_pb2.DequeueOrderResponse(message=f"Dequeued normal order: {normal_order}")
        else:
            return orderqueue_pb2.DequeueOrderResponse(message="No orders in the queue")

def calculate_order_value(order):
    total_value = 0

    for book in order.books:
        total_value += book.quantity

    return total_value

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    orderqueue_pb2_grpc.add_OrderQueueServiceServicer_to_server(
        OrderQueueServicer(), server)
    server.add_insecure_port('[::]:50054')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()



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
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/order_queue'))
sys.path.insert(0, utils_path)
import order_queue_pb2
import order_queue_pb2_grpc



class OrderQueueService(order_queue_pb2_grpc.OrderQueueServiceServicer):
    def AddToQueue(self, request, context):
        is_valid = request.is_valid
        orderID = request.orderID
        queue = request.queue
        
        message=""
        is_in_queue=False
        if is_valid:
            queue.add(orderID)
            message="Order was added to the queue"
            is_in_queue=True
        
        else:
            message="Order was not added to the queue"
        
        return order_queue_pb2.OrderQueueResponse(is_in_queue=is_in_queue,message=message, queue = queue)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    order_queue_pb2_grpc.add_OrderQueueServiceServicer_to_server(OrderQueueService(), server)
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
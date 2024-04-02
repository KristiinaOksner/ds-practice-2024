from asyncio import Lock, Queue
from concurrent import futures
import grpc
import time
import logging

import orderexecutor_pb2
import orderexecutor_pb2_grpc

import sys
import os

from utils.leaderelection import LeaderElection, Request, Response
from utils.pb.orderexecutor.orderexecutor_pb2 import OrderRequest, OrderResponse

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/orderexecutor'))
sys.path.insert(0, utils_path)
import queue

class OrderExecutorServicer(orderexecutor_pb2_grpc.OrderExecutorServicer):

    def __init__(self, replica_id, replicas_info, max_workers=10):
        self.replica_id = replica_id
        self.replicas_info = replicas_info
        self.order_queue = Queue() 
        self.execution_lock = Lock()
        self.leader_election = LeaderElection(replica_id, replicas_info)
        self.executor = futures.ThreadPoolExecutor(max_workers=max_workers)

    def _execute_order(self, order_id):
        with self.execution_lock:
            if not self.leader_election.is_leader():
                return OrderResponse(message="Not the leader, cannot execute order.")

            try:
                order = self.order_queue.get_nowait()
                if order.order_id != order_id:
                    raise ValueError("Invalid order ID.")
                self.order_queue.task_done()

                # record_status(order_id, "received")
                pass

                # implement actual order_execution(order)
                print("oder is being executed")
                pass

                # update_order_status(order_id, "updated")
                pass
            
                return OrderResponse(message="Order executed successfully.")
            except queue.Empty:
                return OrderResponse(message="No order found in queue.")
            except Exception as e:
                return OrderResponse(message=f"Error executing order: {str(e)}")

    def ExecuteOrder(self, request: OrderRequest, context):
        future = self.executor.submit(self._execute_order, request.order_id)
        logging.info(f"Executing order with ID: {request.order_id}")
        return future.result()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    orderexecutor_pb2_grpc.add_OrderExecutorServicer_to_server(OrderExecutorServicer(), server)
    server.add_insecure_port('[::]:50055')
    server.start()
    logging.info("OrderExecutor Service started. Listening on port 50055")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
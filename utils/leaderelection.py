import time
import threading
from typing import Dict, List, Optional
from concurrent.futures import Future
from grpc import RpcContext

import sys
import os
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path_orderexecutor = os.path.abspath(os.path.join(FILE, '../../../utils/pb/orderexecutor'))
sys.path.insert(0, utils_path_orderexecutor)
import orderexecutor_pb2
import orderexecutor_pb2_grpc


class Request:
    def __init__(self, sender_id: int, timestamp: float):
        self.sender_id = sender_id
        self.timestamp = timestamp


class Response:
    def __init__(self, approved: bool):
        self.approved = approved


class LeaderElection:
    def __init__(self, replica_id: int, replicas_info: Dict[int, str]):
        self.replica_id = replica_id
        self.replicas_info = replicas_info
        self.local_requests: Dict[int, float] = {}  
        self.pending_requests: Dict[int, Future[Response]] = {} 
        self.lock = threading.Lock()
        self.current_leader: Optional[int] = None

    def request_to_lead(self) -> bool:
        with self.lock:
            if self.current_leader is not None and self.current_leader != self.replica_id:
                return False 
            
            local_request_timestamp = time.time()
            self.local_requests[self.replica_id] = local_request_timestamp

            approvals = {replica_id: False for replica_id in self.replicas_info.keys()}
            approvals[self.replica_id] = True

            # seed requests
            for replica_id, replica_address in self.replicas_info.items():
                if replica_id == self.replica_id:
                    continue

                future = self.send_request(replica_address, self.replica_id, local_request_timestamp)
                self.pending_requests[replica_id] = future

            # check responses
            while len(approvals) > 0:
                finished_futures, unfinished_futures = wait(
                    list(self.pending_requests.values()), timeout=1.0
                )
                for future in finished_futures:
                    replica_id = future.request_sender_id
                    response = future.result()
                    if response.approved:
                        approvals[replica_id] = True
                    del self.pending_requests[replica_id]

                if all(approvals.values()):
                    self.current_leader = self.replica_id
                    return True

        return False

    def send_request(self, replica_address: str, sender_id: int, timestamp: float) -> Future[Response]:

        def handle_response(response: Response, context: RpcContext):
            nonlocal future
            future.response = response
            future.set_result(response)

        future = Future()
        future.request_sender_id = sender_id
        request = Request(sender_id, timestamp)
        stub = orderexecutor_pb2_grpc.OrderExecutorStub(grpc.insecure_channel('orderexecutor:50055'))
        stub.ProcessRequest.future(request, metadata=(('sender-id', str(sender_id)),), callback=handle_response)
        return future

    def process_request(self, request: Request, context: RpcContext) -> Response:
        """
        deal with the request from other service
        """
        with self.lock:
            if request.sender_id == self.replica_id:
                return Response(False)  

            if request.timestamp < self.local_requests.get(request.sender_id, 0.0):
                return Response(False)  

            self.local_requests[request.sender_id] = request.timestamp
            return Response(True) 

    def is_leader(self) -> bool:
        """
        return whether the current replica is the leader
        """
        with self.lock:
            return self.current_leader == self.replica_id

    def release_leadership(self):
        """
        release leadership
        """
        with self.lock:
            self.current_leader = None
            self.local_requests.clear()
            self.pending_requests.clear()
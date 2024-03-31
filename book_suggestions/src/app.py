<<<<<<< Updated upstream
from ast import List
=======
import logging
>>>>>>> Stashed changes
import grpc
from concurrent import futures
import random
import time

import sys
import os

from utils.pb.book_suggestions.book_suggestions_pb2 import BookSuggestionsRequest, BookSuggestionsResponse, Item

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/book_suggestions'))
sys.path.insert(0, utils_path)
import book_suggestions_pb2
import book_suggestions_pb2_grpc

# Define a list of books
<<<<<<< Updated upstream
STATIC_BOOK_LIST = [
    Item(name="Harry Potter and the Philosopher's Stone"),
    Item(name="The Lord of the Rings"),
    Item(name="To Kill a Mockingbird")
]

class BookRecommendationService(book_suggestions_pb2_grpc.BookSuggestionsServiceServicer):
    def find_similar_books(self, target_book_name: str) -> List[Item]:
        similar_books = []
        for book in STATIC_BOOK_LIST:
            if target_book_name.lower() in book.name.lower():
                similar_books.append(book)
        return similar_books

    def GetBookSuggestions(self, request: BookSuggestionsRequest, context) -> BookSuggestionsResponse:
        max_quantity_book = max(request.books, key=lambda x: x.quantity)
        
        suggested_books = self.find_similar_books(max_quantity_book.name)

        response = BookSuggestionsResponse()
        response.suggestions.extend(suggested_books)
        return response
=======
static_books = [
    {"name": "Harry Potter and the Sorcerer's Stone", "quantity": 10},
    {"name": "The Great Gatsby", "quantity": 5},
    {"name": "To Kill a Mockingbird", "quantity": 8}
]

class BookRecommendationService(book_suggestions_pb2_grpc.BookSuggestionsServiceServicer):
    def GetBookSuggestions(self, request, context):
        suggested_books = []
        for book in static_books:
            for req_book in request.books:
                if req_book.name.lower() in book["name"].lower():
                    suggested_book = book_suggestions_pb2.Book(name=book["name"], quantity=book["quantity"])
                    suggested_books.append(suggested_book)
        logging.info("Book Suggestions Service: Suggested books: %s", suggested_books)
        return book_suggestions_pb2.BookSuggestionsResponse(suggestions=suggested_books)
>>>>>>> Stashed changes

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    book_suggestions_pb2_grpc.add_BookSuggestionsServiceServicer_to_server(BookRecommendationService(), server)
    server.add_insecure_port('[::]:50053')
    server.start()
    logging.info("Book Suggestions Service running on port 50053")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
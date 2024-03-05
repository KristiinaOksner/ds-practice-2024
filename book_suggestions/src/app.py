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
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/book_suggestions'))
sys.path.insert(0, utils_path)
import book_suggestions_pb2
import book_suggestions_pb2_grpc

# Define a list of books with title and author
books = [
    {"title": "Book A", "author": "Author X"},
    {"title": "Book B", "author": "Author Y"},
    {"title": "Book C", "author": "Author X"},
    {"title": "Book D", "author": "Author Z"}
]

class BookRecommendationService(book_suggestions_pb2_grpc.BookSuggestionsServiceServicer):
    def GetBookSuggestions(self, request, context):
        response = book_suggestions_pb2.BookSuggestionsResponse()
        
        for requested_book in request.books:
            requested_author = requested_book.author
            for book in books:
                if book["author"] == requested_author:
                    new_book = book_suggestions_pb2.Book(title=book["title"], author=book["author"])
                    response.suggestions.append(new_book)
        
        return response

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    book_suggestions_pb2_grpc.add_BookSuggestionsServiceServicer_to_server(BookRecommendationService(), server)
    server.add_insecure_port('[::]:50053')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
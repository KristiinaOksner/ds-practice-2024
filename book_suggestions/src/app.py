import grpc
import random
import time
import book_suggestions_pb2
import book_suggestions_pb2_grpc

class BookSuggestionsServicer(book_suggestions_pb2_grpc.BookSuggestionsServicer):
    def GetBookSuggestions(self, request, context):
        books = [
            {"title": "Book1", "author": "Author1"},
            {"title": "Book2", "author": "Author2"},
            {"title": "Book3", "author": "Author3"},
            {"title": "Book4", "author": "Author4"},
            {"title": "Book5", "author": "Author5"}
        ]
        
        num_suggestions = min(request.num_suggestions, len(books))
        suggestions = random.sample(books, num_suggestions)
        
        response = book_suggestions_pb2.BookSuggestionResponse()
        
        for book in suggestions:
            new_book = response.suggestions.add()
            new_book.title = book["title"]
            new_book.author = book["author"]
        
        return response

def serve():
    server = grpc.server(grpc.ThreadPoolExecutor(max_workers=10))
    book_suggestions_pb2_grpc.add_BookSuggestionsServicer_to_server(BookSuggestionsServicer(), server)
    server.add_insecure_port('[::]:50053')
    server.start()
    print("Server started. Listening on port 50053...")
    
    try:
        while True:
            time.sleep(86400)  # One day in seconds
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
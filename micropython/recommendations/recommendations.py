from concurrent import futures
import logging, os
import random

import grpc
from recommendations_pb2 import (
    BookCategory,
    BookRecommendation,
    RecommendationResponse,
)
import recommendations_pb2_grpc

import json

def read_json(filename: str) -> dict:
    f = open(filename)
    return json.load(f)

def convert_db(db_path: str) -> dict:
    # Import the database
    books_db = read_json(db_path)
    # Initialize output
    books_dict = {}
    # Trace lists of different length
    i = 1
    # Convertion loop
    for category, books in books_db["categories"].items():
        books_dict[books_db["mapping"].index(category)] = [
            BookRecommendation(id=i+j, title=book) for j, book in enumerate(books)
        ]
        i += len(books)
    return books_dict

class RecommendationService(recommendations_pb2_grpc.RecommendationsServicer):
    books_by_category = convert_db(os.getenv("DB_PATH"))

    @staticmethod
    def random_recommendation(books, n):
        return random.sample(books, n)

    @staticmethod
    def heuristic_recommendation(books, n):
        pass

    @staticmethod
    def personalized_recommendation(books, n):
        pass

    def Recommend(self, request, context):
        if request.category not in RecommendationService.books_by_category:
            context.abort(grpc.StatusCode.NOT_FOUND, "Category not found")

        books_for_category = RecommendationService.books_by_category[request.category]
        num_results        = min(request.max_results, len(books_for_category))
        books_to_recommend = RecommendationService.random_recommendation(books_for_category, num_results)

        return RecommendationResponse(recommendations = books_to_recommend)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    recommendations_pb2_grpc.add_RecommendationsServicer_to_server(RecommendationService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()

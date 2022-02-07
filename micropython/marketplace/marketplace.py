import os

from flask import Flask, render_template
import grpc

from recommendations_pb2 import BookCategory, RecommendationRequest
from recommendations_pb2_grpc import RecommendationsStub

app = Flask(__name__)

recommendations_host = os.getenv("RECOMMENDATIONS_HOST")
recommendations_channel = grpc.insecure_channel(
    f"{recommendations_host}:50051"
)
recommendations_client = RecommendationsStub(recommendations_channel)

@app.route("/")
def render_homepage():
    return render_template(
        "homepage.html"
    )

@app.route("/philosophy")
def render_philosophy():
    recommendations_request = RecommendationRequest(
        user_id=1, category=BookCategory.PHILOSOPHY, max_results=3
    )
    recommendations_response = recommendations_client.Recommend(
        recommendations_request
    )
    return render_template(
        "philosophy.html",
        recommendations=recommendations_response.recommendations,
    )

@app.route("/literature")
def render_literature():
    recommendations_request = RecommendationRequest(
        user_id=1, category=BookCategory.LITERATURE, max_results=3
    )
    recommendations_response = recommendations_client.Recommend(
        recommendations_request
    )
    return render_template(
        "literature.html",
        recommendations=recommendations_response.recommendations,
    )

@app.route("/science")
def render_science():
    recommendations_request = RecommendationRequest(
        user_id=1, category=BookCategory.SCIENCE, max_results=3
    )
    recommendations_response = recommendations_client.Recommend(
        recommendations_request
    )
    return render_template(
        "science.html",
        recommendations=recommendations_response.recommendations,
    )


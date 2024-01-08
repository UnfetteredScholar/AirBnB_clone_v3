#!/usr/bin/python3
"""
Review Blueprint definition
"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route("/places/<place_id>/reviews",
                 methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """Gets all reviews of a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return make_response(jsonify(reviews))


@app_views.route("/reviews/<review_id>", methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Gets a review by its ID"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return make_response(jsonify(review.to_dict()))


@app_views.route("/reviews/<review_id>",
                 methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """Deletes a review by its ID"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/places/<place_id>/reviews",
                 methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """Creates a review in a place"""
    review_data = request.get_json()
    if not review_data:
        abort(400, "Not a JSON")
    if "user_id" not in review_data:
        abort(400, "Missing user_id")
    if "text" not in review_data:
        abort(400, "Missing text")
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    user = storage.get(User, review_data['user_id'])
    if not user:
        abort(404)
    review_data["place_id"] = place_id
    new_review = Review(**review_data)
    storage.new(new_review)
    storage.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route("/reviews/<review_id>", methods=['PUT'], strict_slashes=False)
def modify_review(review_id):
    """Modifies a review by its ID"""
    review_data = request.get_json()
    if not review_data:
        abort(400, "Not a JSON")
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    for key, val in review_data.items():
        if key not in ['id', 'user_id',
                       'place_id', 'created_at', 'updated_at']:
            setattr(review, key, val)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)

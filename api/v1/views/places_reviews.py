#!/usr/bin/python3
"""reviews objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def get_place_reviews(place_id):
    """Retrieves a reviews from place object"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews])


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    """Retrieves a place object"""
    review = storage.get('Review', review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """delete a Review object"""
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """create a Review object"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'user_id' not in request.get_json():
        abort(400, 'Missing user_id')
    user = storage.get('User', request.get_json()['user_id'])
    if user is None:
        abort(404)
    if 'text' not in request.get_json():
        abort(400, 'Missing text')

    new_review = Review(place_id=place_id, **request.get_json())
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """update a review object"""
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    for key, value in request.get_json().items():
        if key not in [
            "id", "user_id", "place_id", "created_at", "updated_at"
        ]:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200

#!/usr/bin/python3
"""reviews objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from os import getenv


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def get_place_amenities(place_id):
    """Retrieves a amenities from place object"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    if getenv("HBNB_TYPE_STORAGE") == "db":
        amenities = [amenity.to_dict() for amenity in place.amenities]
    else:
        amenities = [
            storage.get('Amenity', amenity_id).to_dict()
            for amenity_id in place.amenity_ids
        ]
    return jsonify(amenities)


@app_views.route(
    '/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'])
def delete_places_amenity(place_id, amenity_id):
    """delete a amenity object"""
    place = storage.get('Place', place_id)
    amenity = storage.get('Amenity', amenity_id)
    if place is None or amenity is None:
        abort(404)
    if getenv("HBNB_TYPE_STORAGE") == "db":
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)
    storage.save()
    return jsonify({}), 200


@app_views.route(
    "/places/<place_id>/amenities/<amenity_id>", methods=["POST"],)
def create_amenity_to_place(place_id, amenity_id):
    """create amenity to place"""
    place = storage.get('Place', place_id)
    amenity = storage.get('Amenity', amenity_id)
    if place is None or amenity is None:
        abort(404)
    if getenv("HBNB_TYPE_STORAGE") == "db":
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenity_ids.append(amenity_id)
    storage.save()
    return jsonify(amenity.to_dict()), 201

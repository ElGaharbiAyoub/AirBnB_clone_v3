#!/usr/bin/python3
"""Places objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.user import User
from models.amenity import Amenity
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """Creates a Place"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")
    user = storage.get('User', request.get_json()['user_id'])
    if user is None:
        abort(404)
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    place = Place(city_id=city.id, **request.get_json())
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """Updates a Place object"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'])
def places_search():
    """
    Retrieves all Place objects depending on
    the JSON in the body of the request
    """
    headers = request.headers.get('Content-Type')
    if headers != 'application/json':
        abort(400, 'Not a JSON')

    data = request.get_json()

    if not data:
        return jsonify([
            place.to_dict() for place in storage.all('Place').values()
        ])

    states = []
    cities = []
    amenities = []
    places = []

    # Get all cities from states if 'states' are passed in the request
    if data.get('states'):
        for state_id in data.get('states'):
            state = storage.get('State', state_id)
            if state:
                for city in state.cities:
                    cities.append(city.id)

    # Add cities to the existing 'cities' list after looking through states
    if data.get('cities'):
        for city_id in data.get('cities'):
            if city_id not in cities:
                cities.append(city_id)

    # Create an amenities list if 'amenities' are passed
    if data.get('amenities'):
        for amenity_id in data.get('amenities'):
            if amenity_id not in cities:
                amenities.append(amenity_id)

    # Create a list of place IDs from all cities
    for place in storage.all('Place').values():
        if place.city_id in cities:
            places.append(place.id)

    # If 'places' is empty and 'amenities' is not empty
    if not places and amenities:
        remove = []
        res = []
        places = [place.id for place in storage.all('Place').values()]
        for place in places:
            get_place = storage.get('Place', place)
            for amenity in get_place.amenities:
                if amenity.id not in amenities:
                    if place not in remove:
                        remove.append(place)
        for place in places:
            if place not in remove:
                res.append(place)
        return jsonify([storage.get('Place', obj).to_dict()
                        for obj in res])

    # Filter places based on amenities
    if amenities:
        for place_id in places.copy():
            get_place = storage.get('Place', place_id)
            for amenity in amenities:
                if amenity not in get_place.amenities:
                    places.remove(place_id)
    # if amenities:
    #     amenities_obj = [storage.get(Amenity, amenity_id)
    #                      for amenity_id in amenities]
    #     places = [place for place in places if all(
    #         amenity in place.amenities for amenity in amenities_obj)]

    return jsonify([
        storage.get('Place', place_id).to_dict() for place_id in places
    ])

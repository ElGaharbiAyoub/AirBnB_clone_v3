#!/usr/bin/python3
"""City objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/cities', methods=['GET'])
def get_cities():
    """Retrieves the list of all City objects"""
    cities = [city.to_dict() for city in storage.all('City').values()]
    return jsonify(cities)


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_state_cities(state_id):
    """Retrieves a cities from state object"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """Retrieves a City object"""
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """update a City object"""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    for key, value in request.get_json().items():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """delete a City object"""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def post_city(state_id):
    """post a City object"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    new_city = City(state_id=state.id, **request.get_json())
    new_city.save()
    return jsonify(new_city.to_dict()), 201

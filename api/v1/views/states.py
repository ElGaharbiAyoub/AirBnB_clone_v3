#!/usr/bin/python3
"""State objects that handle all default RestFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'])
def get_states():
    """Retrieves the list of all State objects"""
    states = [state.to_dict() for state in storage.all('State').values()]
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """Retrieves a State object"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Deletes a State object"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'])
def create_state():
    """Creates a State"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    state = State(**request.get_json())
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """Updates a State object"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200

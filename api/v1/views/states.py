#!/usr/bin/python3
"""
States blueprint definition
"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """Retrieves all state objects"""
    states = storage.all("State").values()
    states = [state.to_dict() for state in states]
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state(state_id):
    """Retrieves state object matching the id"""
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    return abort(404)


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Deletes the state matching the id"""
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return make_response(jsonify({}), 200)
    return abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a State object"""
    state_data = request.get_json()
    if not state_data:
        abort(400, "Not a JSON")
    if "name" not in state_data:
        abort(400, "Missing name")
    new_state = State(**state_data)
    storage.new(new_state)
    storage.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def modify_state(state_id):
    """Modifies a State object"""
    state_data = request.get_json()
    if not state_data:
        abort(400, "Not a JSON")
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    for key, val in state_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, val)
    storage.save()
    return make_response(state.to_dict(), 200)

#!/usr/bin/python3
"""
City Blueprint definition
"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities",
                 methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """Gets all cities of a states"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return make_response(jsonify(cities))


@app_views.route("/cities/<city_id>", methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Gets a city by its ID"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return make_response(jsonify(city.to_dict()))


@app_views.route("/cities/<city_id>", methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Deletes a city by its ID"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states/<state_id>/cities",
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """Creates a city in a state"""
    city_data = request.get_json()
    if not city_data:
        abort(400, "Not a JSON")
    if "name" not in city_data:
        abort(400, "Missing name")
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    city_data["state_id"] = state_id
    new_city = City(**city_data)
    storage.new(new_city)
    storage.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route("/cities/<city_id>", methods=['PUT'], strict_slashes=False)
def modify_city(city_id):
    """Modifies a city by its ID"""
    city_data = request.get_json()
    if not city_data:
        abort(400, "Not a JSON")
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    for key, val in city_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city, key, val)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)

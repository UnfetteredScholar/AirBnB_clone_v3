#!/usr/bin/python3
"""
Place Blueprint definition
"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route("/cities/<city_id>/places",
                 methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """Gets all places of a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return make_response(jsonify(places))


@app_views.route("/places/<place_id>", methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Gets a place by its ID"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return make_response(jsonify(place.to_dict()))


@app_views.route("/places/<place_id>",
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes a place by its ID"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/cities/<city_id>/places",
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Creates a place in a city"""
    place_data = request.get_json()
    if not place_data:
        abort(400, "Not a JSON")
    if "user_id" not in place_data:
        abort(400, "Missing user_id")
    if "name" not in place_data:
        abort(400, "Missing name")
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    user = storage.get(User, place_data['user_id'])
    if not user:
        abort(404)
    place_data["city_id"] = city_id
    new_place = Place(**place_data)
    storage.new(new_place)
    storage.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route("/places/<place_id>", methods=['PUT'], strict_slashes=False)
def modify_place(place_id):
    """Modifies a place by its ID"""
    place_data = request.get_json()
    if not place_data:
        abort(400, "Not a JSON")
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    for key, val in place_data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, val)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)

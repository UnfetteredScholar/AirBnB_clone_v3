#!/usr/bin/python3
"""
Amenity blueprint definition
"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Retrieves all amenity objects"""
    amenities = storage.all(Amenity).values()
    amenities = [amenity.to_dict() for amenity in amenities]
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieves amenity object matching the id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    return abort(404)


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes the amenity matching the id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return make_response(jsonify({}), 200)
    return abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Creates an amenity object"""
    amenity_data = request.get_json()
    if not amenity_data:
        abort(400, "Not a JSON")
    if "name" not in amenity_data:
        abort(400, "Missing name")
    new_amenity = Amenity(**amenity_data)
    storage.new(new_amenity)
    storage.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def modify_amenity(amenity_id):
    """Modifies an amenity object"""
    amenity_data = request.get_json()
    if not amenity_data:
        abort(400, "Not a JSON")
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    for key, val in amenity_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, val)
    storage.save()
    return make_response(amenity.to_dict(), 200)

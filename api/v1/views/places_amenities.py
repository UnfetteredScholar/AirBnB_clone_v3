#!/usr/bin/python3
"""
Place-Amenity Blueprint definition
"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity
from models.place import Place
from models.user import User
from os import getenv


@app_views.route("/places/<place_id>/amenities",
                 methods=['GET'], strict_slashes=False)
def get_place_place_amenities(place_id):
    """Gets all amenities of a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        amenities = [amenity.to_dict() for amenity in place.amenities]
    else:
        amenities = [storage.get(Amenity, amenity_id).to_dict()
                     for amenity_id in place.amenity_ids]
    return make_response(jsonify(amenities))


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """Deletes a amenity by its ID"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if (amenity is None) or (place is None):
        abort(404)
    for amen_obj in place.amenities:
        if amen_obj.id == amenity.id:
            if getenv('HBNB_TYPE_STORAGE') == 'db':
                place.amenities.remove(amenity)
            else:
                place.amenity_ids.remove(amenity.id)
            storage.save()
            return make_response(jsonify({}), 200)
    abort(404)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=['POST'], strict_slashes=False)
def create_place_amenity(place_id, amenity_id):
    """Creates a amenity in a place"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        if amenity in place.amenities:
            return make_response(jsonify(amenity.to_dict()), 200)
        place.amenities.append(amenity)
    else:
        if amenity.id in place.amenity_ids:
            return make_response(jsonify(amenity.to_dict()), 201)
        place.amenity_ids.append(amenity.id)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)

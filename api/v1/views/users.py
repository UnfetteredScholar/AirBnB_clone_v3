#!/usr/bin/python3
"""
User blueprint definition
"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieves all user objects"""
    users = storage.all(User).values()
    users = [user.to_dict() for user in users]
    return jsonify(users)


@app_views.route('/users/<user_id>',
                 methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrieves user object matching the id"""
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    return abort(404)


@app_views.route('/users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes the user matching the id"""
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return make_response(jsonify({}), 200)
    return abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a user object"""
    user_data = request.get_json()
    if not user_data:
        abort(400, "Not a JSON")
    if "email" not in user_data:
        abort(400, "Missing email")
    if "password" not in user_data:
        abort(400, "Missing password")
    new_user = User(**user_data)
    storage.new(new_user)
    storage.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def modify_user(user_id):
    """Modifies a user object"""
    user_data = request.get_json()
    if not user_data:
        abort(400, "Not a JSON")
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    for key, val in user_data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, val)
    storage.save()
    return make_response(user.to_dict(), 200)

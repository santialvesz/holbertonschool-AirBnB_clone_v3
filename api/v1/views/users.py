#!/usr/bin/python3
"""View for Amenity objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def users():
    """Retrieves the list of all User objects"""
    my_list = [i.to_dict() for i in storage.all(User).values()]
    return jsonify(my_list)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def retrieve_user(user_id):
    """Retrieves a User object"""
    obj_user = storage.get(User, user_id)
    if not obj_user:
        abort(404)
    var = obj_user.to_dict()
    return jsonify(var)


app_views.route('/users/<user_id>', methods=['DELETE'],
                strict_slashes=False,)


def del_user(user_id):
    """Deletes a User object"""
    new_user = storage.get(User, user_id)
    if not new_user:
        abort(404)
    storage.delete(new_user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_users():
    """Creates a User"""
    new_user = request.get_json()
    if not new_user:
        abort(400, "Not a JSON")
    if "email" not in new_user:
        abort(400, "Missing email")
    if "password" not in new_user:
        abort(400, "Missing password")
    users = User(**new_user)
    storage.new(users)
    storage.save()
    return make_response(jsonify(users.to_dict()), 201)


@app_views.route('/users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """Updates a User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")

    for key, value in req.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)

    storage.save()
    return make_response(jsonify(user.to_dict()), 200)

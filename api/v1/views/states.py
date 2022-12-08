#!/usr/bin/python3
"""Create a new view for State objects that
handles all default RESTFul API actions"""

from api.v1.views import app_views
from flask import Flask, jsonify, abort, make_response, request
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def states():
    my_list = []
    for i in storage.all(State):
        my_list.append(i.to_dict())
    return jsonify(my_list)


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def retrieve_state_id(state_id):
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states', strict_slashes=False, methods=['DELETE'])
def delete_state(state_id):
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    state.delete()
    state.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def post_state():
    new_state = request.get_json()
    if not new_state:
        abort(400, "Not a JSON")
    if "name" not in new_state:
        abort(400, "Missing name")
    state = State(**new_state)
    storage.new(state)
    storage.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states', strict_slashes=False, methods=['PUT'])
def put_state(state_id):
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")
    for key, value in req.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)

#!/usr/bin/python3
"""Create a new view for State objects that
handles all default RESTFul API actions"""

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """Retrieves the list of all State obcjets"""
    my_list = [i.to_dict() for i in storage.all(State).values()]
    return jsonify(my_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def retrieve_state_id(state_id):
    """Retrieves a State object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    var = state.to_dict()
    return jsonify(var)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False,)
def delete_state(state_id):
    """Delete a State Object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """Create a state object"""
    new_state = request.get_json()
    if not new_state:
        abort(400, "Not a JSON")
    if "name" not in new_state:
        abort(400, "Missing name")
    state = State(**new_state)
    storage.new(state)
    storage.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """Updates a state object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    req = request.get_json()
    if req is None:
        abort(400, "Not a JSON")

    for key, value in req.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(state, key, value)

    storage.save()
    return make_response(jsonify(state.to_dict()), 200)

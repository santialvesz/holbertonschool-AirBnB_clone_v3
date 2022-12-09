#!/usr/bin/python3
"""View for Amenity objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def amenities():
    """Retrieves the list of all Amenity objects"""
    my_list = [i.to_dict() for i in storage.all(Amenity).values()]
    return jsonify(my_list)


@app_views.route('amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def retrieve_amenities(amenity_id):
    """Retrieves a Amenity object"""
    obj_amenity = storage.get(Amenity, amenity_id)
    if not obj_amenity:
        abort(404)
    var = obj_amenity.to_dict()
    return jsonify(var)


@app_views.route('amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False,)
def delete_amenities(amenity_id):
    """Deletes a Amenity object"""
    obj_amenity = storage.get(Amenity, obj_amenity)
    if obj_amenity is None:
        abort(404)
    storage.delete(obj_amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenities():
    """Creates a Amenity"""
    new_amenity = request.get_json()
    if not new_amenity:
        abort(400, "Not a JSON")
    if "name" not in new_amenity:
        abort(400, "Missing name")
    amenities = Amenity(**new_amenity)
    storage.new(amenities)
    storage.save()
    return make_response(jsonify(amenities.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def put_amenity(amenity_id):
    """Updates a Amenity object"""
    new_amenity = storage.get(Amenity, amenity_id)
    if not new_amenity:
        abort(404)
    req = request.get_json()
    if req is None:
        abort(400, "Not a JSON")

    for key, value in req.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(new_amenity, key, value)

    storage.save()
    return make_response(jsonify(new_amenity.to_dict()), 200)

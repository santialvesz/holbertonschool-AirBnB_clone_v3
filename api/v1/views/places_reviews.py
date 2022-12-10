#!/usr/bin/python3
""" places_reviews module """
from api.v1.views.__init__ import app_views
from flask import jsonify, abort, request, make_response
from models.__init__ import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route("/places/<string:place_id>/reviews", methods=["GET"])
def all_review_of_place(place_id):
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    list_of_review = []
    for rw in place.reviews:
        list_of_review.append(rw.to_dict())
    return jsonify(list_of_review)


@app_views.route("/reviews/<string:review_id>", methods=["GET"])
def get_review(review_id):
    review = storage.get(Review, review_id)

    if not review:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route("/reviews/<string:review_id>", methods=["DELETE"])
def delete_review(review_id):
    review = storage.get(Review, review_id)

    if not review:
        abort(404)

    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<string:place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """create a new review"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    kwargs = request.get_json()
    if 'user_id' not in kwargs:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    user = storage.get(User, kwargs['user_id'])
    if user is None:
        abort(404)
    if 'text' not in kwargs:
        return make_response(jsonify({'error': 'Missing text'}), 400)
    kwargs['place_id'] = place_id
    review = Review(**kwargs)
    review.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route("reviews/<review_id>", methods=["PUT"])
def update_review(review_id):
    review = storage.get(Review, review_id)
    httpDict = request.get_json()

    if not review:
        abort(404)

    if not httpDict or type(httpDict) != dict:
        abort(400, "Not a JSON")

    for key, value in httpDict.items():
        if key not in ["id",
                       "created_at",
                       "updated_at",
                       "user_id",
                       "place_id"]:
            setattr(review, key, value)
        storage.save()
        return jsonify(review.to_dict()), 200

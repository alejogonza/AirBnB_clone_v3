#!/usr/bin/python3
"""Create a new view for State objects RestFul API
"""
from flask import Flask, json, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_rplace(place_id):
    """ ® Get all the review by place
    """
    new_list = []
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    for key, values in storage.all("Review").items():
        if place_id == values.place_id:
            new_list.append(values.to_dict())

    return jsonify(new_list)


@app_views.route('/reviews/<review_id>',
                 methods=['GET'], strict_slashes=False)
def get_review_id(review_id):
    """get review by id
    """
    for key, values in storage.all("Review").items():
        if review_id == values.id:
            return jsonify(values.to_dict())
    abort(404)


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """delete review by id
    """
    for key, values in storage.all("Review").items():
        if review_id in key:
            storage.delete(values)
            storage.save()
            storage.close()
            return jsonify({}), 200
    abort(404)


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def post_rplaces(place_id):
    """ ††† method HTTP POST json
    """
    if request.is_json:
        new_dict = request.get_json()
    else:
        return jsonify({"error": "Not a JSON"}), 400

    if "user_id" not in new_dict:
        return jsonify({"error": "Missing user_id"}), 400
    if "text" not in new_dict:
        return jsonify({"error": "Missing text"}), 400
    user = storage.get("User", new_dict["user_id"])
    if user is None:
        abort(404)
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    new_review = Review()
    for k, v in new_dict.items():
        setattr(new_review, k, v)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def put_rplaces(review_id):
    """ ††† method HTTP PUT to update the City with id †††
    """
    if request.is_json:
        new_dict = request.get_json()
    else:
        return jsonify({"error": "Not a JSON"}), 400
    for key in ['id', 'created_at', 'updated_at', 'user_id', 'place_id']:
        if key in new_dict:
            del new_dict[key]
    for key, value in storage.all("Review").items():
        if review_id == value.id:
            for k, v in new_dict.items():
                setattr(value, k, v)
            storage.save()
            return jsonify(value.to_dict()), 200
    abort(404)

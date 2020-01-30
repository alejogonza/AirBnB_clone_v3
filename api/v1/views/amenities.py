#!/usr/bin/python3
"""Create  State objects that handles RestFul API
"""
from flask import Flask, json, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """get all amenities
    """
    tmp_list = []
    for key, value in storage.all("Amenity").items():
        tmp_list.append(value.to_dict())
    return jsonify(tmp_list)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity_by_id(amenity_id):
    """get Amenity by id
    """
    for key, value in storage.all("Amenity").items():
        if amenity_id == value.id:
            return jsonify(value.to_dict())
    abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """delete Amenity by id
    """
    for key, values in storage.all("Amenity").items():
        if amenity_id in key:
            storage.delete(values)
            storage.save()
            storage.close()
            return jsonify({}), 200
    abort(404)


@app_views.route('/amenities',  methods=['POST'], strict_slashes=False)
def post_amenity():
    """ ††† method HTTP POST json
    """
    if request.is_json:
        new_dict = request.get_json()
    else:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" in new_dict:
        new_amenity = Amenity()
        new_amenity.name = new_dict["name"]
        storage.new(new_amenity)
        storage.save()
        return jsonify(new_amenity.to_dict()), 201
    else:
        return jsonify({"error": "Missing name"}), 400


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def amenity(amenity_id):
    """ ††† method HTTP PUT to update the state with id †††
    """
    if request.is_json:
        new_dict = request.get_json()
    else:
        return jsonify({"error": "Not a JSON"}), 400
    for key in ['id', 'created_at', 'updated_at']:
        if key in new_dict:
            del new_dict[key]
    for key, value in storage.all("Amenity").items():
        if amenity_id == value.id:
            for k, v in new_dict.items():
                setattr(value, k, v)
            storage.save()
            return jsonify(value.to_dict()), 200
    abort(404)

#!/usr/bin/python3
"""Create a new view for State objects RestFul API
"""
from flask import Flask, json, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from models.place import Place


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """get all cities of a id State
    """
    new_list = []
    for skey, svalue in storage.all("City").items():
        if city_id == svalue.id:
            for key, value in storage.all("Place").items():
                if city_id == value.city_id:
                    new_list.append(value.to_dict())
    if len(new_list) > 0 or storage.get("City", city_id):
        return jsonify(new_list)
    else:
        abort(404)


@app_views.route('/places/<place_id>',
                 methods=['GET'], strict_slashes=False)
def get_place_id(place_id):
    """get city by id with verification of states
    """
    for key, values in storage.all("Place").items():
        if place_id == values.id:
            return jsonify(values.to_dict())
    abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_places(place_id):
    """delete city by id
    """
    for key, values in storage.all("Place").items():
        if place_id in key:
            for skey, svalue in storage.all("City").items():
                if values.city_id == svalue.id:
                    storage.delete(values)
                    storage.save()
                    storage.close()
                    return jsonify({}), 200
    abort(404)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def post_places(city_id):
    """ ††† method HTTP POST json
    """
    if request.is_json:
        new_dict = request.get_json()
    else:
        return jsonify({"error": "Not a JSON"}), 400
    for value in storage.all("City").values():
        if city_id == value.id:
            if "user_id" in new_dict and "name" in new_dict:
                for value in storage.all("User").values():
                    if new_dict["user_id"] == value.id:
                        new_city = Place()
                        new_city.name = new_dict["name"]
                        new_city.user_id = new_dict["user_id"]
                        new_city.city_id = city_id
                        storage.new(new_city)
                        storage.save()
                        storage.close()
                        return jsonify(new_city.to_dict()), 201
                abort(404)
            else:
                if "name" in new_dict:
                    return jsonify({"error": "Missing user_id"}), 400
                if "user_id" in new_dict:
                    return jsonify({"error": "Missing name"}), 400
    abort(404)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_places(place_id):
    """ ††† method HTTP PUT to update the City with id †††
    """
    if request.is_json:
        new_dict = request.get_json()
    else:
        return jsonify({"error": "Not a JSON"}), 400
    for key in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
        if key in new_dict:
            del new_dict[key]
    for key, value in storage.all("Place").items():
        if place_id == value.id:
            for skey, svalue in storage.all("City").items():
                if value.city_id == svalue.id:
                    for k, v in new_dict.items():
                        setattr(value, k, v)
                    storage.save()
                    storage.close()
                    return jsonify(value.to_dict()), 200
    abort(404)

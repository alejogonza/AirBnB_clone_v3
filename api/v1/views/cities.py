#!/usr/bin/python3
"""Create a new view for State objects that handles all default RestFul API
"""
from flask import Flask, json, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """get all cities of a id State
    """
    new_list = []
    for skey, svalue in storage.all("State").items():
        if state_id == svalue.id:
            for key, value in storage.all("City").items():
                if state_id == value.state_id:
                    new_list.append(value.to_dict())
    if len(new_list) > 0 or storage.get("State", state_id):
        return jsonify(new_list)
    else:
        abort(404)


@app_views.route('cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_cities_id(city_id):
    """get city by id with verification of states
    """
    for key, values in storage.all("City").items():
        if city_id == values.id:
            return jsonify(values.to_dict())
    abort(404)


@app_views.route('cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_cities(city_id):
    """delete city by id
    """
    for key, values in storage.all("City").items():
        if city_id in key:
            for skey, svalue in storage.all("State").items():
                if values.state_id == svalue.id:
                    storage.delete(values)
                    storage.save()
                    storage.close()
                    return jsonify({}), 200
    abort(404)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def post_cities(state_id):
    """ ††† method HTTP POST json
    """
    if request.is_json:
        new_dict = request.get_json()
    else:
        return jsonify({"error": "Not a JSON"}), 400
    for value in storage.all("State").values():
        if state_id == value.id:
            if "name" in new_dict:
                new_city = City()
                new_city.name = new_dict["name"]
                new_city.state_id = state_id
                storage.new(new_city)
                storage.save()
                storage.close()
                return jsonify(new_city.to_dict()), 201
            else:
                return jsonify({"error": "Missing name"}), 400
    abort(404)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_cities(city_id):
    """ ††† method HTTP PUT to update the City with id †††
    """
    if request.is_json:
        new_dict = request.get_json()
    else:
        return jsonify({"error": "Not a JSON"}), 400
    for key in ['id', 'created_at', 'updated_at', 'state_id']:
        if key in new_dict:
            del new_dict[key]
    for key, value in storage.all("City").items():
        if city_id == value.id:
            for skey, svalue in storage.all("State").items():
                if value.state_id == svalue.id:
                    for k, v in new_dict.items():
                        setattr(value, k, v)
                    storage.save()
                    storage.close()
                    return jsonify(value.to_dict()), 200
    abort(404)

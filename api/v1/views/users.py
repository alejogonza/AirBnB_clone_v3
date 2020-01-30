#!/usr/bin/python3
"""Create a new view for State objects RestFul API
"""
from flask import Flask, json, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """get all Users
    """
    tmp_list = []
    for key, value in storage.all("User").items():
        tmp_list.append(value.to_dict())
    return jsonify(tmp_list)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user_by_id(user_id):
    """get user by id
    """
    for key, value in storage.all("User").items():
        if user_id == value.id:
            return jsonify(value.to_dict())
    abort(404)


@app_views.route('users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """delete user by id
    """
    for key, values in storage.all("User").items():
        if user_id in key:
            storage.delete(values)
            storage.save()
            storage.close()
            return jsonify({}), 200
    abort(404)


@app_views.route('/users',  methods=['POST'], strict_slashes=False)
def post_users():
    """ ††† method HTTP POST json, create a user and save in db
    """
    if request.is_json:
        new_dict = request.get_json()
    else:
        return jsonify({"error": "Not a JSON"}), 400

    if "email" not in new_dict:
        return jsonify({"error": "Missing email"}), 400
    if "password" not in new_dict:
        return jsonify({"error": "Missing password"}), 400
    new_user = User()
    for k, v in new_dict.items():
        setattr(new_user, k, v)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """ ††† method HTTP PUT to update the state with id †††
    """
    if request.is_json:
        new_dict = request.get_json()
    else:
        return jsonify({"error": "Not a JSON"}), 400
    for key in ['id', 'created_at', 'updated_at', 'email']:
        if key in new_dict:
            del new_dict[key]
    for key, value in storage.all("User").items():
        if user_id == value.id:
            for k, v in new_dict.items():
                setattr(value, k, v)
            storage.save()
            return jsonify(value.to_dict()), 200
    abort(404)

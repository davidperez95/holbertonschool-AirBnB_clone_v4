#!/usr/bin/python3
"""
Module for amenities views
"""
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import abort, jsonify, make_response, request


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def all_amenities():
    """
    Returns all amenities
    """
    amenities = storage.all(Amenity).values()
    amenities_list = []

    for amenity in amenities:
        amenities_list.append(amenity.to_dict())

    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>/', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """
    Returns an amenity by its id
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """
    Deletes an amenity by its id
    """
    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    storage.delete(amenity)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """
    Creates an amenity
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    instance = Amenity(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """
    Updates an amenity
    """
    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(amenity, key, value)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)

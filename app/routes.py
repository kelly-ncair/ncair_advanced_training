from flask import Blueprint, request, jsonify
from .crud import *

bp = Blueprint('routes', __name__)

# ---- USER ROUTES ----
@bp.route('/users', methods=['POST'])
def add_user():
    data = request.json
    user = create_user(data['username'])
    return jsonify({"id": user.id, "username": user.username}), 201

@bp.route('/users/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    user = get_user(user_id)
    if user:
        return jsonify({"id": user.id, "username": user.username})
    return jsonify({"error": "User not found"}), 404

# ---- PROFILE ROUTES ----
@bp.route('/profiles', methods=['POST'])
def add_profile():
    data = request.json
    profile = create_profile(data['user_id'], data['bio'])
    return jsonify({"id": profile.id, "bio": profile.bio}), 201

@bp.route('/profiles/<int:profile_id>', methods=['GET'])
def get_one_profile(profile_id):
    profile = get_profile(profile_id)
    if profile:
        return jsonify({"id": profile.id, "bio": profile.bio})
    return jsonify({"error": "Profile not found"}), 404

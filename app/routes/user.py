from flask import Blueprint, request, jsonify, abort
from app.models import User
from app.extensions import db
from werkzeug.security import generate_password_hash
from app.decorators import check_access
from flasgger import swag_from

user_bp = Blueprint('users', __name__)


# GET user by id
@user_bp.route("/<int:user_id>", methods=["GET"])
@check_access(['Admin'])
@swag_from("app/swagger_config.yml", endpoint='get_user_by_id', methods=["GET"])
def get_user_by_id(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        abort(404, description="User not found")
    else:
        return jsonify(user.to_dict()), 200


# Get list of all users
@user_bp.route("/", methods=["GET"])
@check_access(['Admin'])
@swag_from("app/swagger_config.yml", endpoint='get_all_user', methods=["GET"])
def get_all_users():
    users = User.query.all()
    return jsonify({'users': [user.to_dict() for user in users]}), 200


# POST add a new user
@user_bp.route("/", methods=["POST"])
@check_access(roles=['Admin'])
@swag_from("app/swagger_config.yml", endpoint='add_new_user', methods=["GET"])
def add_new_user():
    if (
        not request.json
        or 'username' not in request.json
        or 'password' not in request.json
        or 'role' not in request.json
    ):
        abort(400, description="missing data for required fields")

    new_user = User(
        username=request.json['username'],
        password=generate_password_hash(request.json['password']),
        role=request.json['role']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201


# PUT update a user
@user_bp.route("/<int:user_id>", methods=["PUT"])
@check_access(roles=['Admin'])
@swag_from("app/swagger_config.yml", endpoint='update_user', methods=["PUT"])
def update_user(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        abort(404, description='User not found')

    if not request.json:
        abort(400, description="Missing data")

    user.username = request.json.get('username', user.username)
    user.role = request.json.get('role', user.role)

    password = request.json.get('password')

    if password:
        user.password = generate_password_hash(password)

    db.session.commit()

    return jsonify(user.to_dict()), 201


# DELETE user
@user_bp.route("/<int:user_id>", methods=["DELETE"])
@swag_from("app/swagger_config.yml", endpoint='delete_user', methods=["DELETE"])
@check_access(roles=['Admin'])
def delete_user(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        abort(404, description="User not found")

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User successfully deleted"}), 200


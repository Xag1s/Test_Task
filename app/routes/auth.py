from flask import Blueprint, request, jsonify, abort
from app.models import User
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from flasgger import swag_from

auth_bp = Blueprint('login', __name__)


# Login
@auth_bp.route("/", methods=["POST"])
@swag_from("app/swagger_config.yml", endpoint='login', methods=["POST"])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user is None or not check_password_hash(user.password, password):
        abort(401, description='Invalid username or password')

    access_token = create_access_token(identity=str(user.id))
    return jsonify({"access_token": access_token}), 200


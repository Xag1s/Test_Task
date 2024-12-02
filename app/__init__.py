from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os
from app.extensions import db, jwt
from app.commands import create_user, reset_db


def create_app():
    app = Flask(__name__)
    CORS(app)

    load_dotenv()

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "default_secret_key")

    db.init_app(app)
    jwt.init_app(app)

    app.cli.add_command(commands.create_user)
    app.cli.add_command(commands.reset_db)

    from .routes import register_routes
    register_routes(app)

    return app

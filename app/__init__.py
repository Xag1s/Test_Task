from flask import Flask
from flask_cors import CORS
from app.config import Config
from app.extensions import db, jwt, swagger
from app.commands import create_user, reset_db
from app.articles.article import article_bp
from app.auth.auth import auth_bp
from app.user.user import user_bp


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.register_blueprint(user_bp)
    app.register_blueprint(article_bp)
    app.register_blueprint(auth_bp)

    CORS(app)

    db.init_app(app)
    jwt.init_app(app)
    swagger.init_app(app)

    app.cli.add_command(commands.create_user)
    app.cli.add_command(commands.reset_db)

    return app

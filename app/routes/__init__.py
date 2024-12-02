from .user import user_bp
from .article import article_bp
from .auth import auth_bp


def register_routes(app):
    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(article_bp, url_prefix='/articles')
    app.register_blueprint(auth_bp, url_prefix='/login')

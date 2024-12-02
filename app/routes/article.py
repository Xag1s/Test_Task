from flask import Blueprint, request, jsonify, abort
from app.models import Articles, User
from app.extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity

article_bp = Blueprint("article", __name__)


# GET all articles
@article_bp.route("/", methods=["GET"])
def get_all_articles():
    articles = Articles.query.all()
    return jsonify({"Articles": [article.to_dict() for article in articles]}), 200


# POST new articles
@article_bp.route("/", methods=["POST"])
@jwt_required()
def add_new_articles():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not request.json or "title" not in request.json or "text" not in request.json:
        abort(400, description="Missing data for required fields")

    new_article = Articles(
        title=request.json["title"], text=request.json["text"], user_id=user.id
    )

    db.session.add(new_article)
    db.session.commit()

    return jsonify(new_article.to_dict()), 201


# Update articles
@article_bp.route("/<int:article_id>", methods=["PUT"])
@jwt_required()
def update_article(article_id):
    article = db.session.get(Articles, article_id)
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if user.role in ["Viewer"] and article.user_id != user.id:
        abort(403, description="You do not have permission to edit this article")

    if article is None:
        abort(404, description="Article not found")

    if not request.json:
        abort(400, description="Missing data")

    article.title = request.json.get("title", article.title)
    article.text = request.json.get("text", article.text)

    db.session.commit()

    return jsonify(article.to_dict()), 200


# The admin can delete any article, and the viewer, the editor can delete only their own articles
@article_bp.route("/<int:article_id>", methods=["DELETE"])
@jwt_required()
def delete_article(article_id):
    article = db.session.get(Articles, article_id)
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if user.role in ["Viewer", "Editor"] and article.user_id != user.id:
        abort(403, description="You do not have permission to edit this article")

    if article is None:
        abort(404, description="Article not found")

    db.session.delete(article)
    db.session.commit()

    return jsonify({"message": "Article successfully deleted"}), 200


# Search article by text
@article_bp.route("/search", methods=["GET"])
def search_by_text():
    if not request.json:
        abort(400, description="Missing data")

    text = request.json.get("text")

    results = db.session.query(Articles).filter(Articles.text.startswith(text)).all()

    return jsonify([result.to_dict() for result in results]), 200

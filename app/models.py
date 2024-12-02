from . import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    role = db.Column(db.String(300), nullable=False)
    articles = db.relationship("Articles", backref="user")

    def to_dict(self):
        return {"id": self.id,
                "username": self.username,
                "role": self.role}


class Articles(db.Model):
    __tablename__ = "articles"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "text": self.text,
            "author": self.user.username,
            "user_id": self.user_id,
        }

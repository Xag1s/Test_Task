import os
from sqlalchemy import text
from app import db
from run import app
from app.models import User
from werkzeug.security import generate_password_hash

result = os.scandir("sql_commands")


with app.app_context():

    user_admin = User(username='User-Admin', password=generate_password_hash('admin'), role='Admin')
    user_editor = User(username='User-Editor', password=generate_password_hash('editor'), role='Editor')
    user_viewer = User(username='User-Viewer', password=generate_password_hash('viewer'), role='Viewer')

    db.session.add_all([user_admin, user_editor, user_viewer])
    db.session.commit()

    for item in result:
        if item.is_file:
            sql = open(item.path, 'r')
            statement = sql.read()
            db.session.execute(text(statement))

    db.session.commit()

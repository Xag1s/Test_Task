import click
from flask.cli import with_appcontext, AppGroup
from werkzeug.security import generate_password_hash
from app.extensions import db
from app.models import User


user_cli = AppGroup('user', help="Create user")
reset_db = AppGroup('reset', help="Delete and create db")


@user_cli.command('create-user')
@click.argument("username")
@click.argument("password")
@click.argument("role")
@with_appcontext
def create_user(username, password, role):
    """ Pass the username, password and role to create user """
    click.echo("Creating user")
    user = User(username=username, password=generate_password_hash(password), role=role)

    db.session.add(user)
    db.session.commit()
    click.echo(f"User {username} created")


@reset_db.command("reset-db")
def reset_db():

    db.drop_all()
    db.create_all()



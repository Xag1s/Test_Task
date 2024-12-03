import pytest
from app import create_app
from app.extensions import db
import jwt
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token


@pytest.fixture()
def client():
    app = create_app()
    app.testing = True
    with app.test_client() as testclient:
        with app.app_context():
            db.create_all()
            yield testclient







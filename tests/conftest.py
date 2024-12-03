import pytest
from app import create_app
import jwt
from datetime import datetime, timedelta


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture
def auth_token(client):
    response = client.post('/login', data={
            "username": "User-Admin",
            "password": "admin"
            }, follow_redirects=True)

    token = response.json
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def auth_header(app):
    """
    Fixture для створення заголовка авторизації з JWT токеном.
    """
    def _get_auth_header(user_id=1):
        # Генерація токена
        payload = {
            "identity": user_id,
            "exp": datetime.utcnow() + timedelta(hours=1)  # Термін дії токена
        }
        token = jwt.encode(payload, app.config["SECRET_KEY"], algorithm="HS256")
        return {"Authorization": f"Bearer {token}"}

    return _get_auth_header



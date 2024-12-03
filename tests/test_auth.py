import json
import re
import pytest
from unittest.mock import Mock


def test_login(client):
    response = client.post('/login',
                           json={'username': 'User-Admin', 'password': 'admin'},
                           follow_redirects=True)

    assert response.status_code == 200

    assert 'access_token' in response.json

    token_pattern = r"^[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+$"
    access_token = response.json["access_token"]

    assert re.match(token_pattern, access_token)


def test_login_wrong_username_or_password(client):
    response = client.post('/login',
                           json={'username': 'User', 'password': '1111'},
                           follow_redirects=True)

    assert response.status_code == 401
    assert b'Invalid username or password' in response.data


import json
import re
import pytest
from unittest.mock import Mock


def test_get_all_users(client):

    response = client.post(
        "/login",
        json={"username": "User-Admin", "password": "admin"},
        follow_redirects=True,
    )
    token = response.json["access_token"]

    response = client.get(
        "/users", headers={"Authorization": f"Bearer {token}"}, follow_redirects=True
    )

    assert response.status_code == 200

    response_data = response.json
    assert "users" in response_data
    assert isinstance(response_data["users"], list)


def test_get_all_users_unauthorized(client):
    response = client.get("/users", follow_redirects=True)

    assert response.status_code == 401


def test_get_specific_user(client):

    response = client.post(
        "/login",
        json={"username": "User-Admin", "password": "admin"},
        follow_redirects=True,
    )
    token = response.json["access_token"]

    response = client.get(
        "/users/1", headers={"Authorization": f"Bearer {token}"}, follow_redirects=True
    )

    assert response.status_code == 200

    result = response.json
    assert "id" in result
    assert "username" in result
    assert "role" in result


def test_get_specific_user_not_found(client):

    response = client.post(
        "/login",
        json={"username": "User-Admin", "password": "admin"},
        follow_redirects=True,
    )
    token = response.json["access_token"]

    response = client.get(
        "/users/111",
        headers={"Authorization": f"Bearer {token}"},
        follow_redirects=True,
    )

    assert response.status_code == 404

    assert b"User not found" in response.data


def test_get_specific_user_unauthorized(client):
    response = client.get("/users/111", follow_redirects=True)

    assert response.status_code == 401

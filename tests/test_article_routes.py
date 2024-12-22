import json

import pytest
from unittest.mock import Mock


def test_get_all_articles(client):
    response = client.get("/articles", follow_redirects=True)

    assert response.status_code == 200

    response_data = response.json
    assert "Articles" in response_data
    assert isinstance(response_data["Articles"], list)

    assert any(
        article.get("title") == "Lorem ipsum dolor sit amet."
        for article in response_data["Articles"]
    )


def test_get_all_articles_failure(client):
    response = client.get("/articles", follow_redirects=True)

    expected_response = {"Articles": [{"Title": "tile", "text": "text"}]}
    assert response.status_code == 200
    assert response.json != expected_response


def test_get_article_by_text(client):
    response = client.get(
        "/articles/search",
        json={"text": "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Al"},

    )

    expected_response = ["Lorem ipsum dolor sit amet."]
    response_data = response.json
    result = [article["title"] for article in response_data]

    assert response.status_code == 200
    assert result == expected_response


def test_get_article_by_text_failure(client):
    response = client.get(
        "/articles/search",
        json={"text": "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Al"},
        follow_redirects=True,
    )

    expected_response = ["Text for test"]
    response_data = response.json
    result = [article["title"] for article in response_data]

    assert response.status_code == 200
    assert result != expected_response


def test_get_article_by_text_missing_data(client):
    response = client.get("/articles/search", json={}, follow_redirects=True)

    assert response.status_code == 400


def test_get_article_by_text_not_found(client):
    response = client.get("/articles/search", json={"text": 1}, follow_redirects=True)

    expected_response = []
    assert response.status_code == 200
    assert response.json == expected_response

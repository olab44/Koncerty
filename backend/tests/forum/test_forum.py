import pytest
from fastapi.testclient import TestClient
import os
from dotenv import load_dotenv
from src.main import app
import requests

BASE_URL = "http://localhost:8000"


def load_env():
    load_dotenv("TEST_TOKEN")
    TEST_TOKEN = os.getenv("TEST_TOKEN")
    return TEST_TOKEN


@pytest.fixture
def client():
    return TestClient(app)


def test_create_alert(client):
    """
    Test creating an alert with a valid group.
    """
    auth_header = {"Authorization": load_env()}
    response = client.post(
        f"{BASE_URL}/forum/createAlert",
        json={
            "title": "Test Alert",
            "content": "This is a test alert content",
            "parent_group": 1, 
            "group_id": 1 
        },
        headers=auth_header
    )

    assert response.status_code == 201
    data = response.json()
    assert "alert" in data
    assert "recipients" in data
    assert data["alert"]["title"] == "Test Alert"
    assert data["alert"]["content"] == "This is a test alert content"


def test_get_alerts(client):
    """
    Test retrieving alerts for a specific parent group.
    """
    auth_header = {"Authorization": load_env()}
    response = client.get(
        f"{BASE_URL}/forum/getAlerts?parent_group=1&user_id=1",
        headers=auth_header
    )
    assert response.status_code == 200


def test_create_alert_without_group(client):
    """
    Test creating an alert without specifying a group_id.
    """
    auth_header = {"Authorization": load_env()}
    response = client.post(
        f"{BASE_URL}/forum/createAlert",
        json={
            "title": "Test Alert Without Group",
            "content": "This alert has no group specified",
            "parent_group": 1
        },
        headers=auth_header
    )

    assert response.status_code == 404


def test_get_alerts_no_data(client):
    """
    Test retrieving alerts for a non-existent parent group.
    """
    auth_header = {"Authorization": load_env()}
    response = client.get(
        f"{BASE_URL}/forum/getAlerts?parent_group=999&user_id=1",
        headers=auth_header
    )

    assert response.status_code == 404

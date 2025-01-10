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
    auth_header = {"Authorization": load_env()}
    response = client.post(
        f"{BASE_URL}/createAlert",
        json={
            "title": "Test Alert",
            "content": "This is a test alert content",
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
    auth_header = {"Authorization": load_env()}

    response = client.get(
        f"{BASE_URL}/getAlerts?parent_group=1",
        headers=auth_header
    )

    assert response.status_code == 200
    data = response.json()
    assert "alerts" in data
    assert len(data["alerts"]) > 0
    assert data["alerts"][0]["title"] == "Test Alert"


def test_create_alert_without_group(client):
    auth_header = {"Authorization": load_env()}
    
    response = client.post(
        f"{BASE_URL}/createAlert",
        json={
            "title": "Test Alert Without Group",
            "content": "This alert has no group specified"
        },
        headers=auth_header
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "You must provide user_id or group_id to address the alert"}


def test_get_alerts_no_data(client):
    auth_header = {"Authorization": load_env()}

    response = client.get(
        f"{BASE_URL}/getAlerts?parent_group=999",  # Assuming this group does not exist
        headers=auth_header
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "User is not a member of the group"}


def test_alert_sends_email(client):
    auth_header = {"Authorization": load_env()}
    # Create a new alert
    response = client.post(
        f"{BASE_URL}/createAlert",
        json={
            "title": "Test Alert with Email",
            "content": "This is a test alert content with email notification",
            "group_id": 1
        },
        headers=auth_header
    )
    assert response.status_code == 201
    data = response.json()

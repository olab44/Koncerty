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
        f"{BASE_URL}/forum/createAlert",
        json={
            "title": "Test Alert",
            "content": "This is a test alert content",
            "group_id": 1
        },
        headers=auth_header
    )

    assert response.status_code == 201


def test_get_alerts(client):
    auth_header = {"Authorization": load_env()}

    response = client.get(
        f"{BASE_URL}/forum/getAlerts?parent_group=1",
        headers=auth_header
    )

    assert response.status_code == 200


def test_create_alert_without_group(client):
    auth_header = {"Authorization": load_env()}
    
    response = client.post(
        f"{BASE_URL}/forum/createAlert",
        json={
            "title": "Test Alert Without Group",
            "content": "This alert has no group specified"
        },
        headers=auth_header
    )

    assert response.status_code == 404


def test_get_alerts_no_data(client):
    auth_header = {"Authorization": load_env()}

    response = client.get(
        f"{BASE_URL}/forum/getAlerts?parent_group=999",
        headers=auth_header
    )

    assert response.status_code == 404

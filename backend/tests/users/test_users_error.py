import pytest
from fastapi.testclient import TestClient
import os
import json
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

def test_find_users_invalid_token(client):
    auth_header = {"Authorization": "123"}
    response = client.get(f"{BASE_URL}/findUsers?group_id=1", headers=auth_header)
    assert response.status_code == 403

def test_create_user_invalid_token(client):
    auth_header = {"Authorization": "123"}
    response = client.post(f"{BASE_URL}/createUser", json={
        "username": "new me"
    }, headers=auth_header)
    assert response.status_code == 400

def test_change_role_invalid_token(client):
    auth_header = {"Authorization": "123"}
    response = client.post(f"{BASE_URL}/changeRole", json={
        "group_id": 1,
        "user_email": "w@gmail.com",
        "new_role": "Kapelmistrz",
        "parent_group": -1

    }, headers=auth_header)
    assert response.status_code == 403

def test_change_role_not_member_of_group(client):
    auth_header = {"Authorization": load_env()}
    response = client.post(f"{BASE_URL}/changeRole", json={
        "group_id": 2,
        "user_email": "w@gmail.com",
        "new_role": "Kapelmistrz",
        "parent_group": 2

    }, headers=auth_header)
    assert response.status_code == 403

def test_remove_member_invalid_token(client):
    auth_header = {"Authorization": "123"}
    response = requests.delete(f"{BASE_URL}/removeMember", json={
        "group_id": 1,
        "user_email": "w@gmail.com",
        "new_role": "Kapelmistrz",
        "parent_group": 1

    }, headers=auth_header)
    assert response.status_code == 403

def test_remove_member_requesting_not_member(client):
    auth_header = {"Authorization": load_env()}
    response = requests.delete(f"{BASE_URL}/removeMember", json={
        "group_id": 2,
        "user_email": "w@gmail.com",
        "new_role": "Kapelmistrz",
        "parent_group": 2

    }, headers=auth_header)
    assert response.status_code == 403


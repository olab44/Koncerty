import requests
import os
from dotenv import load_dotenv


BASE_URL = "http://localhost:8000"
def load_env():
    load_dotenv("TEST_TOKEN")
    TEST_TOKEN = os.getenv("TEST_TOKEN")
    return TEST_TOKEN

def test_create_user_registered():
    auth_header = {"Authorization": load_env()}

    response = requests.post(f"{BASE_URL}/createUser", json={
        "username": "newuser"
    }, headers=auth_header)
    assert response.status_code == 400

def test_find_users():
    auth_header = {"Authorization": load_env()}
    response = requests.get(f"{BASE_URL}/findUsers?group_id=1", headers=auth_header)
    users = response.json()
    assert response.status_code == 200
    assert users[0]["id"] == 1
    assert users[0]["username"] == "Bilb"
    assert users[0]["email"] == "megalodony.pzsp2@gmail.com"
    assert users[0]["role"] == "Kapelmistrz"

def test_change_role():
    auth_header = {"Authorization": load_env()}

    response = requests.post(f"{BASE_URL}/changeRole", json={
        "group_id": 1,
        "user_email": "k@gmail.com",
        "new_role": "Kapelmistrz",
        "parent_group": 1
    }, headers=auth_header)
    assert response.status_code == 201
    response = requests.get(f"{BASE_URL}/findUsers?group_id=1", headers=auth_header)
    assert response.status_code == 200

def test_remove_member():
    auth_header = {"Authorization": load_env()}

    response = requests.delete(f"{BASE_URL}/removeMember", json={
        "group_id": 1,
        "user_email": "w@gmail.com",
        "parent_group": 1
    }, headers=auth_header)
    assert response.status_code == 200
    response = requests.get(f"{BASE_URL}/findUsers?group_id=1", headers=auth_header)
    assert response.status_code == 200


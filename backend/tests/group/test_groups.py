import requests
import pytest
from src.main import app 
from fastapi.testclient import TestClient
from users.test_users import BASE_URL, load_env

@pytest.fixture
def client():
    return TestClient(app)

def test_find_groups(client):
    auth_header = {"Authorization": load_env()}

    response = client.get(f"{BASE_URL}/groups/findGroups", headers=auth_header)
    assert response.status_code == 200
    info = response.json()
    assert info["username"] == "Bilb"
    assert info["group_structure"] == [
        {
            "group_id": 1,
            "group_name": "Grajkowie",
            "role": "Kapelmistrz",
            "extra_info": "Polub nas na instagramie LINK",
            "inv_code": "ASD12",
            "subgroups": [
                {
                    "subgroup_id": 3,
                    "subgroup_name": "Grajkowie:Strunowe",
                    "extra_info": "Polub nas na facebooku LINK",
                }
            ]
        }
    ]

def test_create_groups(client):
    auth_header = {"Authorization": load_env()}

    response = client.post(f"{BASE_URL}/groups/createGroup", json={
        "parent_group": -1,
        "name": "New name",
        "extra_info": "more info"
    }, headers=auth_header)
    assert response.status_code == 201

def test_join_group(client):
    auth_header = {"Authorization": load_env()}

    response = client.post(f"{BASE_URL}/groups/joinGroup", json={
        "inv_code": "123"
    }, headers=auth_header)
    assert response.status_code == 200

def test_create_subgroup(client):
    auth_header = {"Authorization": load_env()}

    response = client.post(f"{BASE_URL}/groups/createSubgroup", json={
        "parent_group": 1,
        "name": "podgrupa pierwszego",
        "extra_info": "więcej informacji",
        "members": [1, 3, 4]
    }, headers=auth_header)
    assert response.status_code == 201

def test_edit_group(client):
    auth_header = {"Authorization": load_env()}

    response = client.post(f"{BASE_URL}/groups/editGroup", json={
        "group_id": 4,
        "name": "Changed group",
        "extra_info": "changed extra",
        "parent_group": 4
    }, headers=auth_header)
    assert response.status_code == 201

def test_find_subgroups(client):
    auth_header = {"Authorization": load_env()}

    response = client.get(f"{BASE_URL}/groups/findSubgroups?group_id=4", headers=auth_header)
    info = response.json()
    assert response.status_code == 200
    assert info == []

def test_remove_subgroup(client):
    auth_header = {"Authorization": load_env()}

    response = client.post(f"{BASE_URL}/groups/deleteSubgroup", json={
        "group_id": 5,
        "parent_group": 1
    }, headers=auth_header)
    assert response.status_code == 200

def test_add_member(client):
    auth_header = {"Authorization": load_env()}

    response = client.post(f"{BASE_URL}/groups/addMember", json={
        "group_id": 3,
        "parent_group": 1,
        "user_id": 2
    }, headers=auth_header)
    assert response.status_code == 201
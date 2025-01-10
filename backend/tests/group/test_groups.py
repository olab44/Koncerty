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

def test_find_groups(client):
    auth_header = {"Authorization": load_env()}

    response = client.get(f"{BASE_URL}/groups/findGroups", headers=auth_header)
    assert response.status_code == 200
    info = response.json()
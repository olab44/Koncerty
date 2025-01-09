import requests
from users.test_users import BASE_URL, load_env

def test_assign_file_to_user():
    auth_header = {"Authorization": load_env()}

    response = requests.post(f"{BASE_URL}/files/assignFileToUser", json={
        "file_id": 1,
        "user_id": 1,
        "parent_group": 1
    }, headers=auth_header)
    assert response.status_code == 201
    info = response.json()
    assert info["assigned"]["user_id"] == 1
    assert info["assigned"]["file_id"] == 1

def test_assign_file_to_subgroup():
    auth_header = {"Authorization": load_env()}

    response = requests.post(f"{BASE_URL}/files/assignFileToSubgroup", json={
        "file_id": 1,
        "group_id": 1
    }, headers=auth_header)
    assert response.status_code == 201
    info = response.json()
    assert info["assigned"][0]["id"] == 3
    assert info["assigned"][0]["file_id"] == 1
    assert info["assigned"][0]["user_id"] == 2

def test_assign_file_to_composition():
    auth_header = {"Authorization": load_env()}

    response = requests.post(f"{BASE_URL}/files/assignFileToComposition", json={
        "file_id": 1,
        "composition_id": 1,
        "parent_group": 1
    }, headers=auth_header)
    assert response.status_code == 201

def test_deprive_user_of_file():
    auth_header = {"Authorization": load_env()}

    response = requests.delete(f"{BASE_URL}/files/depriveUserOfFile", json={
        "file_id": 1,
        "user_id": 1,
        "parent_group": 1
    }, headers=auth_header)
    assert response.status_code == 204

def test_deprive_subgroup_of_file():
    auth_header = {"Authorization": load_env()}

    response = requests.delete(f"{BASE_URL}/files/depriveSubgroupOfFile", json={
        "file_id": 1,
        "group_id": 1
    }, headers=auth_header)
    assert response.status_code == 204

def test_deprive_composition_of_file():
    auth_header = {"Authorization": load_env()}

    response = requests.delete(f"{BASE_URL}/files/depriveCompositionOfFile", json={
        "file_id": 1,
        "parent_group": 1
    }, headers=auth_header)
    assert response.status_code == 204


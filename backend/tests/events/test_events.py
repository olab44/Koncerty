import requests
from datetime import datetime
from src.main import app 
from fastapi.testclient import TestClient
import pytest
from users.test_users import BASE_URL, load_env


@pytest.fixture
def client():
    return TestClient(app)

def test_find_events(client):
    auth_header = {"Authorization": load_env()}

    response = client.get(f"{BASE_URL}/events/findEvents?group_id=1",
                              headers=auth_header)
    assert response.status_code == 200
    info = response.json()
    assert info[0]["event_id"] == 1
    assert info[0]["name"] == "Charetatywne granie"
    assert info[0]["location"] == "Mariot"
    assert info[0]["extra_info"] == "Badzcie"
    assert info[0]["set_list"] == [
            {
                "id": 1,
                "name": "Symphony no. 5",
                "author": "Ludwig van Beethoven"
            }
        ]
    assert info[0]["parent_group"] == 1
    assert info[0]["type"] == "proba"
    assert info[0]["participants"]== [
            {
                "id": 1,
                "username": "Bilb",
                "email": "megalodony.pzsp2@gmail.com"
            },
            {
                "id": 4,
                "username": "Wik",
                "email": "w@gmail.com"
            },
            {
                "id": 3,
                "username": "Kasia",
                "email": "k@gmail.com"
            }
        ]
    
def test_create_event(client):
    auth_header = {"Authorization": load_env()}

    date_start = datetime(2025, 12, 25, 10, 0, 0) 
    date_end = datetime(2025, 12, 25, 12, 0, 0)

    response = client.post(f"{BASE_URL}/events/createEvent", json={
        "name": "Testing",
        "date_start": date_start.isoformat(),
        "date_end": date_end.isoformat(),
        "location": "Testing location",
        "extra_info": "Testing extra",
        "parent_group": 1,
        "type": "proba",
        "user_emails": ["f@gmail.com"],
        "group_ids": [3],
        "composition_ids": [1]
    }, headers=auth_header,)
    assert response.status_code == 201
    info = response.json()
    
def test_edit_event(client):
    auth_header = {"Authorization": load_env()}

    date_start = datetime(2025, 12, 26, 10, 0, 0) 
    date_end = datetime(2025, 12, 26, 12, 0, 0)

    response = client.post(f"{BASE_URL}/events/editEvent", json={
        "event_id": 3,
        "name": "Edited",
        "date_start": date_start.isoformat(),
        "date_end": date_end.isoformat(),
        "location": "Edited location",
        "extra_info": "Edited extra",
        "parent_group": 1,
        "type": "koncert",
        "removed_participants": ["f@gmail.com"],
        "added_participants": ["w@gmail.com"],
        "removed_compositions": [1],
        "added_compositions": [1]
    }, headers=auth_header,)
    assert response.status_code == 201

import requests
from datetime import datetime

from users.test_users import BASE_URL, load_env

def test_find_events():
    auth_header = {"Authorization": load_env()}

    response = requests.get(f"{BASE_URL}/events/findEvents?group_id=1",
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
    
def test_create_event():
    auth_header = {"Authorization": load_env()}

    date_start = datetime(2025, 12, 25, 10, 0, 0) 
    date_end = datetime(2025, 12, 25, 12, 0, 0)

    response = requests.post(f"{BASE_URL}/events/createEvent", json={
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
    

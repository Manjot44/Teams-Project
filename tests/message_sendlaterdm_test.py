import requests
from src.config import url
import datetime

def test_normal_case(register_three_users, create_dm, return_current_time):
    dm_id = create_dm(register_three_users["token"][0], [register_three_users["id"][0]])
    unix_timestamp = return_current_time()

    response = requests.post(f"{url}/message/sendlaterdm/v1", json = {"token": register_three_users["token"][0], "dm_id": dm_id, "message": "manjot the slacker went to coffs", "time_sent": unix_timestamp + 60})
    assert response.status_code == 200

def test_invalid_dm_id(register_three_users, create_dm, return_current_time):
    dm_id = create_dm(register_three_users["token"][0], [register_three_users["id"][0]])
    unix_timestamp = return_current_time()

    response = requests.post(f"{url}/message/sendlaterdm/v1", json = {"token": register_three_users["token"][0], "dm_id": dm_id + 1, "message": "manjot the slacker went to coffs", "time_sent": unix_timestamp + 60})
    assert response.status_code == 400

def test_invalid_token(register_three_users, create_dm, return_current_time):
    dm_id = create_dm(register_three_users["token"][0], [register_three_users["id"][0]])

    unix_timestamp = return_current_time()

    response = requests.post(f"{url}/message/sendlaterdm/v1", json = {"token": "invalid token", "dm_id": dm_id, "message": "manjot the slacker went to coffs", "time_sent": unix_timestamp + 60})
    assert response.status_code == 403

def test_1000_characters(register_three_users, create_dm, return_current_time):
    dm_id = create_dm(register_three_users["token"][0], [register_three_users["id"][0]])
    unix_timestamp = return_current_time()

    response = requests.post(f"{url}/message/sendlaterdm/v1", json = {"token": register_three_users["token"][0], "dm_id": dm_id, "message": "manjot the slacker went to coffs"*1000, "time_sent": unix_timestamp + 60})
    assert response.status_code == 400

def test_time_sent(register_three_users, create_dm, return_current_time):
    dm_id = create_dm(register_three_users["token"][0], [register_three_users["id"][0]])
    unix_timestamp = return_current_time()

    response = requests.post(f"{url}/message/sendlaterdm/v1", json = {"token": register_three_users["token"][0], "dm_id": dm_id, "message": "manjot the slacker went to coffs", "time_sent": unix_timestamp - 60})
    assert response.status_code == 400

def test_not_in_dm(register_three_users, create_dm, return_current_time):
    dm_id = create_dm(register_three_users["token"][0], [register_three_users["id"][0]])
    unix_timestamp = return_current_time()

    response = requests.post(f"{url}/message/sendlaterdm/v1", json = {"token": register_three_users["token"][1], "dm_id": dm_id, "message": "manjot the slacker went to coffs", "time_sent": unix_timestamp + 60})
    assert response.status_code == 403
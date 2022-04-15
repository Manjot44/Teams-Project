import requests
from src.config import url
import datetime

def test_normal_case(register_three_users):
    response = requests.post(f"{url}/dm/create/v1", json = {"token": register_three_users["token"][0], "u_ids": [register_three_users["id"][0]]})
    assert response.status_code == 200
    response_data = response.json()
    dm_id = response_data["dm_id"]

    current_time = datetime.datetime.now(datetime.timezone.utc)
    utc_time = current_time.replace(tzinfo=datetime.timezone.utc)
    unix_timestamp = utc_time.timestamp()

    response = requests.post(f"{url}/message/sendlaterdm/v1", json = {"token": register_three_users["token"][0], "dm_id": dm_id, "message": "manjot the slacker went to coffs", "time_sent": unix_timestamp + 60})
    assert response.status_code == 200

def test_invalid_dm_id(register_three_users):
    response = requests.post(f"{url}/dm/create/v1", json = {"token": register_three_users["token"][0], "u_ids": [register_three_users["id"][0]]})
    assert response.status_code == 200
    response_data = response.json()
    dm_id = response_data["dm_id"]

    current_time = datetime.datetime.now(datetime.timezone.utc)
    utc_time = current_time.replace(tzinfo=datetime.timezone.utc)
    unix_timestamp = utc_time.timestamp()

    response = requests.post(f"{url}/message/sendlaterdm/v1", json = {"token": register_three_users["token"][0], "dm_id": dm_id + 1, "message": "manjot the slacker went to coffs", "time_sent": unix_timestamp + 60})
    assert response.status_code == 400

def test_invalid_token(register_three_users):
    response = requests.post(f"{url}/dm/create/v1", json = {"token": register_three_users["token"][0], "u_ids": [register_three_users["id"][0]]})
    assert response.status_code == 200
    response_data = response.json()
    dm_id = response_data["dm_id"]

    current_time = datetime.datetime.now(datetime.timezone.utc)
    utc_time = current_time.replace(tzinfo=datetime.timezone.utc)
    unix_timestamp = utc_time.timestamp()

    response = requests.post(f"{url}/message/sendlaterdm/v1", json = {"token": "invalid token", "dm_id": dm_id, "message": "manjot the slacker went to coffs", "time_sent": unix_timestamp + 60})
    assert response.status_code == 403

def test_1000_characters(register_three_users):
    response = requests.post(f"{url}/dm/create/v1", json = {"token": register_three_users["token"][0], "u_ids": [register_three_users["id"][0]]})
    assert response.status_code == 200
    response_data = response.json()
    dm_id = response_data["dm_id"]

    current_time = datetime.datetime.now(datetime.timezone.utc)
    utc_time = current_time.replace(tzinfo=datetime.timezone.utc)
    unix_timestamp = utc_time.timestamp()

    response = requests.post(f"{url}/message/sendlaterdm/v1", json = {"token": register_three_users["token"][0], "dm_id": dm_id, "message": "manjot the slacker went to coffs"*1000, "time_sent": unix_timestamp + 60})
    assert response.status_code == 400

def test_time_sent(register_three_users):
    response = requests.post(f"{url}/dm/create/v1", json = {"token": register_three_users["token"][0], "u_ids": [register_three_users["id"][0]]})
    assert response.status_code == 200
    response_data = response.json()
    dm_id = response_data["dm_id"]

    current_time = datetime.datetime.now(datetime.timezone.utc)
    utc_time = current_time.replace(tzinfo=datetime.timezone.utc)
    unix_timestamp = utc_time.timestamp()

    response = requests.post(f"{url}/message/sendlaterdm/v1", json = {"token": register_three_users["token"][0], "dm_id": dm_id, "message": "manjot the slacker went to coffs", "time_sent": unix_timestamp - 60})
    assert response.status_code == 400

def test_not_in_dm(register_three_users):
    response = requests.post(f"{url}/dm/create/v1", json = {"token": register_three_users["token"][0], "u_ids": [register_three_users["id"][0]]})
    assert response.status_code == 200
    response_data = response.json()
    dm_id = response_data["dm_id"]

    current_time = datetime.datetime.now(datetime.timezone.utc)
    utc_time = current_time.replace(tzinfo=datetime.timezone.utc)
    unix_timestamp = utc_time.timestamp()

    response = requests.post(f"{url}/message/sendlaterdm/v1", json = {"token": register_three_users["token"][1], "dm_id": dm_id, "message": "manjot the slacker went to coffs", "time_sent": unix_timestamp + 60})
    assert response.status_code == 403
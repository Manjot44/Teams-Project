import requests
from src.config import url
import datetime

def test_normal_case(register_three_users, create_channel, return_current_time):
    channel_id = create_channel(register_three_users["token"][0], 'CHANNEL_NAME', True)
    unix_timestamp = return_current_time()

    response = requests.post(f"{url}/message/sendlater/v1", json = {"token": register_three_users["token"][0], "channel_id": channel_id, "message": "manjot the slacker went to coffs", "time_sent": unix_timestamp + 60})
    assert response.status_code == 200

def test_invalid_channel_id(register_three_users, create_channel, return_current_time):
    channel_id = create_channel(register_three_users["token"][0], 'CHANNEL_NAME', True)
    unix_timestamp = return_current_time()

    response = requests.post(f"{url}/message/sendlater/v1", json = {"token": register_three_users["token"][0], "channel_id": channel_id + 1, "message": "manjot the slacker went to coffs", "time_sent": unix_timestamp + 60})
    assert response.status_code == 400

def test_invalid_token(register_three_users, create_channel, return_current_time):
    channel_id = create_channel(register_three_users["token"][0], 'CHANNEL_NAME', True)
    unix_timestamp = return_current_time()

    response = requests.post(f"{url}/message/sendlater/v1", json = {"token": "invalid token", "channel_id": channel_id, "message": "manjot the slacker went to coffs", "time_sent": unix_timestamp + 60})
    assert response.status_code == 403

def test_1000_characters(register_three_users, create_channel, return_current_time):
    channel_id = create_channel(register_three_users["token"][0], 'CHANNEL_NAME', True)
    unix_timestamp = return_current_time()

    response = requests.post(f"{url}/message/sendlater/v1", json = {"token": register_three_users["token"][0], "channel_id": channel_id, "message": "manjot"*1000, "time_sent": unix_timestamp + 60})
    assert response.status_code == 400

def test_time_sent(register_three_users, create_channel, return_current_time):
    channel_id = create_channel(register_three_users["token"][0], 'CHANNEL_NAME', True)
    unix_timestamp = return_current_time()

    response = requests.post(f"{url}/message/sendlater/v1", json = {"token": register_three_users["token"][0], "channel_id": channel_id, "message": "manjot", "time_sent": unix_timestamp - 60})
    assert response.status_code == 400

def test_not_in_channel(register_three_users, create_channel, return_current_time):
    channel_id = create_channel(register_three_users["token"][0], 'CHANNEL_NAME', True)
    unix_timestamp = return_current_time()

    response = requests.post(f"{url}/message/sendlater/v1", json = {"token": register_three_users["token"][1], "channel_id": channel_id, "message": "manjot the slacker went to coffs", "time_sent": unix_timestamp + 60})
    assert response.status_code == 403
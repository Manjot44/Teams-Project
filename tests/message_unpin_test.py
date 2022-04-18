import requests
from src.config import url

def test_invalid_message(register_three_users):
    response = requests.post(f"{url}/channels/create/v2", json = {"token": register_three_users["token"][0], "name": "channel_name", "is_public": True})
    assert response.status_code == 200
    response_data = response.json()
    channel_id = response_data["channel_id"]
    response = requests.post(f"{url}/message/send/v1", json = {"token": register_three_users["token"][0], "channel_id": channel_id, "message": "Hello Sanjam"})
    assert response.status_code == 200    
    response_data = response.json()
    message_id = response_data["message_id"]
    response = requests.post(f"{url}/message/pin/v1", json = {"token": register_three_users["token"][0], "message_id": message_id})
    assert response.status_code == 200
    response = requests.post(f"{url}/message/unpin/v1", json = {"token": register_three_users["token"][0], "message_id": message_id + 1})
    assert response.status_code == 400
    requests.delete(f"{url}/clear/v1")

def test_nothing_pinned(register_three_users):
    response = requests.post(f"{url}/channels/create/v2", json = {"token": register_three_users["token"][0], "name": "channel_name", "is_public": True})
    assert response.status_code == 200
    response_data = response.json()
    channel_id = response_data["channel_id"]
    response = requests.post(f"{url}/message/send/v1", json = {"token": register_three_users["token"][0], "channel_id": channel_id, "message": "Hello Sanjam"})
    assert response.status_code == 200    
    response_data = response.json()
    message_id = response_data["message_id"]
    response = requests.post(f"{url}/message/unpin/v1", json = {"token": register_three_users["token"][0], "message_id": message_id})
    assert response.status_code == 400
    requests.delete(f"{url}/clear/v1")

def test_not_owner(register_three_users):
    response = requests.post(f"{url}/dm/create/v1", json = {"token": register_three_users["token"][0], "u_ids": [register_three_users["id"][1]]})
    assert response.status_code == 200
    response_data = response.json()
    dm_id = response_data["dm_id"]
    response = requests.post(f"{url}/message/senddm/v1", json = {"token": register_three_users["token"][1], "dm_id": dm_id, "message": "Hello Sanjam"})
    assert response.status_code == 200    
    response_data = response.json()
    message_id = response_data["message_id"]
    response = requests.post(f"{url}/message/pin/v1", json = {"token": register_three_users["token"][0], "message_id": message_id})
    assert response.status_code == 200
    response = requests.post(f"{url}/message/unpin/v1", json = {"token": register_three_users["token"][1], "message_id": message_id})
    assert response.status_code == 403
    response = requests.post(f"{url}/message/unpin/v1", json = {"token": register_three_users["token"][0], "message_id": message_id})
    assert response.status_code == 200
    requests.delete(f"{url}/clear/v1")

def test_valid_pin(register_three_users):
    response = requests.post(f"{url}/channels/create/v2", json = {"token": register_three_users["token"][0], "name": "channel_name", "is_public": True})
    assert response.status_code == 200
    response_data = response.json()
    channel_id = response_data["channel_id"]
    response = requests.post(f"{url}/message/send/v1", json = {"token": register_three_users["token"][0], "channel_id": channel_id, "message": "Hello Sanjam"})
    assert response.status_code == 200    
    response_data = response.json()
    message_id = response_data["message_id"]
    message_param = {
        "token": register_three_users["token"][0],
        "channel_id": channel_id,
        "start": 0
    }
    response = requests.get(f"{url}/channel/messages/v2", params = message_param)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["messages"][0]["is_pinned"] == False
    response = requests.post(f"{url}/message/pin/v1", json = {"token": register_three_users["token"][0], "message_id": message_id})
    assert response.status_code == 200
    response = requests.get(f"{url}/channel/messages/v2", params = message_param)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["messages"][0]["is_pinned"] == True
    response = requests.post(f"{url}/message/unpin/v1", json = {"token": register_three_users["token"][0], "message_id": message_id})
    assert response.status_code == 200
    response = requests.get(f"{url}/channel/messages/v2", params = message_param)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["messages"][0]["is_pinned"] == False
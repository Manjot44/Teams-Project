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
    response = requests.post(f"{url}/message/react/v1", json = {"token": register_three_users["token"][0], "message_id": message_id + 1, "react_id": 1})
    assert response.status_code == 400
    requests.delete(f"{url}/clear/v1")

def test_valid_message_not_users(register_three_users):
    response = requests.post(f"{url}/channels/create/v2", json = {"token": register_three_users["token"][0], "name": "channel_name", "is_public": True})
    assert response.status_code == 200
    response_data = response.json()
    channel_id = response_data["channel_id"]
    response = requests.post(f"{url}/message/send/v1", json = {"token": register_three_users["token"][0], "channel_id": channel_id, "message": "Hello Sanjam"})
    assert response.status_code == 200    
    response_data = response.json()
    message_id = response_data["message_id"]
    response = requests.post(f"{url}/message/react/v1", json = {"token": register_three_users["token"][1], "message_id": message_id, "react_id": 1})
    assert response.status_code == 400
    requests.delete(f"{url}/clear/v1")

def test_invalid_reacts(register_three_users):
    response = requests.post(f"{url}/channels/create/v2", json = {"token": register_three_users["token"][0], "name": "channel_name", "is_public": True})
    assert response.status_code == 200
    response_data = response.json()
    channel_id = response_data["channel_id"]
    response = requests.post(f"{url}/message/send/v1", json = {"token": register_three_users["token"][0], "channel_id": channel_id, "message": "Hello Sanjam"})
    assert response.status_code == 200    
    response_data = response.json()
    message_id = response_data["message_id"]
    response = requests.post(f"{url}/message/react/v1", json = {"token": register_three_users["token"][0], "message_id": message_id, "react_id": 97812356891724365})
    assert response.status_code == 400
    response = requests.post(f"{url}/message/react/v1", json = {"token": register_three_users["token"][0], "message_id": message_id, "react_id": 1})
    assert response.status_code == 200
    response = requests.post(f"{url}/message/react/v1", json = {"token": register_three_users["token"][0], "message_id": message_id, "react_id": 1})
    assert response.status_code == 400
    requests.delete(f"{url}/clear/v1")

def test_valid_reacts(register_three_users):
    response = requests.post(f"{url}/channels/create/v2", json = {"token": register_three_users["token"][0], "name": "channel_name", "is_public": True})
    assert response.status_code == 200
    response_data = response.json()
    channel_id = response_data["channel_id"]
    response = requests.post(f"{url}/message/send/v1", json = {"token": register_three_users["token"][0], "channel_id": channel_id, "message": "Hello Sanjam"})
    assert response.status_code == 200    
    response_data = response.json()
    message_id = response_data["message_id"]
    response = requests.post(f"{url}/message/react/v1", json = {"token": register_three_users["token"][0], "message_id": message_id, "react_id": 1})
    assert response.status_code == 200
    message_param = {
        "token": register_three_users["token"][0],
        "channel_id": channel_id,
        "start": 0
    }
    response = requests.get(f"{url}/channel/messages/v2", params = message_param)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["messages"][0]["reacts"][0]["u_ids"][0] == register_three_users["id"][0]

def test_react_dm(register_three_users, create_dm, send_messagedm):
    dm_id = create_dm(register_three_users["token"][0], [register_three_users["id"][1]])
    message_id = send_messagedm(register_three_users["token"][0], dm_id, "Hello Sanjam")

    response = requests.post(f"{url}/message/react/v1", json = {"token": register_three_users["token"][0], "message_id": message_id, "react_id": 1})
    assert response.status_code == 200

    message_param = {
        "token": register_three_users["token"][0],
        "dm_id": dm_id,
        "start": 0
    }
    response = requests.get(f"{url}/dm/messages/v1", params = message_param)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["messages"][0]["reacts"][0]["u_ids"][0] == register_three_users["id"][0]

def test_invalid_react_dm(register_three_users, create_dm, send_messagedm):
    dm_id = create_dm(register_three_users["token"][0], [register_three_users["id"][1]])
    message_id = send_messagedm(register_three_users["token"][0], dm_id, "Hello Sanjam")

    response = requests.post(f"{url}/message/react/v1", json = {"token": register_three_users["token"][2], "message_id": message_id, "react_id": 1})
    assert response.status_code == 400
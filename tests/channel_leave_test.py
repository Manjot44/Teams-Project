import requests
import src.config

def test_valid_leave(register_three_users, create_channel, invite_to_channel):
    channel_id = create_channel(register_three_users["token"][0], "channel_name", True)

    invite_to_channel(register_three_users["token"][0], channel_id, register_three_users["id"][1])

    response = requests.post(f"{src.config.url}/channel/addowner/v1", json = {"token": register_three_users["token"][0], "channel_id": channel_id, "u_id": register_three_users["id"][1]})
    assert response.status_code == 200

    response = requests.post(f"{src.config.url}/channel/leave/v1", json = {"token": register_three_users["token"][1], "channel_id": channel_id})
    assert response.status_code == 200

    response = requests.get(f"{src.config.url}/channel/details/v2?token={register_three_users['token'][0]}&channel_id={channel_id}")
    assert response.status_code == 200
    response_data = response.json()
    owner_members = response_data["owner_members"]
    all_members = response_data["all_members"]
    
    for member in owner_members:
        assert member["u_id"] != register_three_users["id"][1]
    for member in all_members:
        assert member["u_id"] != register_three_users["id"][1]

def test_invalid_channel_id(register_three_users, create_channel):
    create_channel(register_three_users["token"][0], "channel_name", True)

    response = requests.post(f"{src.config.url}/channel/leave/v1", json = {"token": register_three_users["token"][0], "channel_id": None})
    assert response.status_code == 400

def test_non_member_leave(register_three_users, create_channel):
    channel_id = create_channel(register_three_users["token"][0], "channel_name", True)

    response = requests.post(f"{src.config.url}/channel/leave/v1", json = {"token": register_three_users["token"][1], "channel_id": channel_id})
    assert response.status_code == 403

def test_invalid_token_registered(register_three_users, create_channel):
    channel_id = create_channel(register_three_users["token"][0], "channel_name", True)

    response = requests.post(f"{src.config.url}/channel/leave/v1", json = {"token": None, "channel_id": channel_id})
    assert response.status_code == 403

def test_invalid_token_unregistered(reset):
    response = requests.post(f"{src.config.url}/channel/leave/v1", json = {"token": None, "channel_id": 0})
    assert response.status_code == 403

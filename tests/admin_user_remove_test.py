import pytest
from src.auth import auth_register_v1
from src.error import InputError, AccessError
from src.other import clear_v1
from src.data_store import data_store
import src.admin
import requests
from tests.conftest import register_three_users
from src.channels import channels_create_v1
from src.config import url

# Regular Test case where no errors occur - message gets sent to channel and not dm since senddm hasn't been implemented yet 
def test_valid_remove(register_three_users):
    response = requests.post(f"{url}/channels/create/v2", json = {"token": register_three_users["token"][1], "name": "channel_name", "is_public": True})
    assert response.status_code == 200
    response_data = response.json()
    channel_id = response_data["channel_id"]

    response = requests.post(f"{url}/channel/invite/v2", json = {"token": register_three_users["token"][1], "channel_id": channel_id, "u_id": register_three_users["id"][0]})
    response = requests.post(f"{url}/message/send/v1", json = {"token": register_three_users["token"][1], "channel_id": channel_id, "message": "Hello Sanjam"})
    assert response.status_code == 200
    response_data = response.json()

    response = requests.post(f"{url}/admin/userpermission/change/v1", json = {"token" : register_three_users["token"][0], "u_id" : register_three_users["id"][1], "permission_id" : 1})
    assert response.status_code == 200

    response = requests.delete(f"{url}/admin/user/remove/v1", json = {"token": register_three_users["token"][0], "u_id": register_three_users["id"][1]})

    assert response.status_code == 200

    response = requests.get(f"{url}/channel/messages/v2?token={register_three_users['token'][0]}&channel_id={channel_id}&start={0}")#, json = {"token": register_three_users["token"][0], "channel_id": channel_id, "start": 0})
    assert response.status_code == 200
    response_data = response.json()
    
    messages = response_data["messages"][0]["message"]
    
    assert messages == 'Removed user'

# auth_user who is trying to remove another user has an invalid token
def test_invalid_id(register_three_users):
    response = requests.post(f"{url}/channels/create/v2", json = {"token": register_three_users["token"][1], "name": "channel_name", "is_public": True})
    assert response.status_code == 200
    response_data = response.json()
    channel_id = response_data["channel_id"]

    response = requests.post(f"{url}/message/send/v1", json = {"token": register_three_users["token"][1], "channel_id": channel_id, "message": "Hello Sanjam"})
    assert response.status_code == 200
    response_data = response.json()

    response = requests.delete(f"{url}/admin/user/remove/v1", json = {"token": 'incorrect token', "u_id": register_three_users["id"][1]})

    assert response.status_code == 403

# uid is invalid
def test_invalid_uid(register_three_users):
    response = requests.post(f"{url}/channels/create/v2", json = {"token": register_three_users["token"][1], "name": "channel_name", "is_public": True})
    assert response.status_code == 200
    response_data = response.json()
    channel_id = response_data["channel_id"]

    response = requests.post(f"{url}/message/send/v1", json = {"token": register_three_users["token"][1], "channel_id": channel_id, "message": "Hello Sanjam"})
    assert response.status_code == 200
    response_data = response.json()

    response = requests.delete(f"{url}/admin/user/remove/v1", json = {"token": register_three_users["token"][0], "u_id": register_three_users["id"][1] + 50})

    assert response.status_code == 400

# Single global owner tries to remove themselves from Seams
def test_only_global_owner(register_three_users):
    response = requests.post(f"{url}/channels/create/v2", json = {"token": register_three_users["token"][1], "name": "channel_name", "is_public": True})
    assert response.status_code == 200
    response_data = response.json()
    channel_id = response_data["channel_id"]

    response = requests.post(f"{url}/message/send/v1", json = {"token": register_three_users["token"][1], "channel_id": channel_id, "message": "Hello Sanjam"})
    assert response.status_code == 200
    response_data = response.json()

    response = requests.delete(f"{url}/admin/user/remove/v1", json = {"token": register_three_users["token"][0], "u_id": register_three_users["id"][0]})

    assert response.status_code == 400

# non global owner tries to remove other user 
def test_non_global_owner_remove(register_three_users):
    response = requests.post(f"{url}/channels/create/v2", json = {"token": register_three_users["token"][0], "name": "channel_name", "is_public": True})
    assert response.status_code == 200
    response_data = response.json()
    channel_id = response_data["channel_id"]

    response = requests.post(f"{url}/message/send/v1", json = {"token": register_three_users["token"][0], "channel_id": channel_id, "message": "Hello Sanjam"})
    assert response.status_code == 200
    response_data = response.json()

    response = requests.delete(f"{url}/admin/user/remove/v1", json = {"token": register_three_users["token"][1], "u_id": register_three_users["id"][0]})

    assert response.status_code == 403

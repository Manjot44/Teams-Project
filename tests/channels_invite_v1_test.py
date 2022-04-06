import pytest
from src.auth import auth_register_v1
from src.channel import channel_details_v1, channel_join_v1, channel_invite_v1
from src.channels import channels_create_v1
from src.error import InputError, AccessError
from src.other import clear_v1
from tests.conftest import register_three_users
from src.config import url
import requests

'''
HTTP Wrapper Tests 

'''

# test if valid user is added to the channel after being invited - Public Channel
def test_add_user_public(register_three_users):
    token1 = register_three_users["token"][0]
    u_id2 = register_three_users["id"][1]

    response = requests.post(f"{url}/channels/create/v2", json = {"token" : token1, "name" : "channel1", "is_public" : True})
    response_channel = response.json()
    channel1_http = response_channel["channel_id"]
    response_channel_invite = requests.post(f"{url}/channel/invite/v2", json = {"token" : token1, "channel_id" : channel1_http, "u_id" : u_id2})

    assert response_channel_invite.status_code == 200

# test if valid user is added to the channel after being invited - Private Channel
def test_add_user_priv(register_three_users):
    token1 = register_three_users["token"][0]
    u_id2 = register_three_users["id"][1]

    response = requests.post(f"{url}/channels/create/v2", json = {"token" : token1, "name" : "channel1", "is_public" : False})
    response_channel = response.json()
    channel1_http = response_channel["channel_id"]
    response_channel_invite = requests.post(f"{url}/channel/invite/v2", json = {"token" : token1, "channel_id" : channel1_http, "u_id" : u_id2})

    assert response_channel_invite.status_code == 200

# User that is invited does not have a valid ID
def test_add_invalid_id(register_three_users):
    token1 = register_three_users["token"][0]
    u_id1 = register_three_users["id"][0]

    response = requests.post(f"{url}/channels/create/v2", json = {"token" : token1, "name" : "channel1", "is_public" : False})
    response_channel = response.json()
    channel1_http = response_channel["channel_id"]
    response_channel_invite = requests.post(f"{url}/channel/invite/v2", json = {"token" : token1, "channel_id" : channel1_http, "u_id" : u_id1 + 60})

    assert response_channel_invite.status_code == 400

# Test where auth_user tries to add someone to the channel who is already in the channel
def test_if_channel_member(register_three_users):
    token1 = register_three_users["token"][0]
    u_id2 = register_three_users["id"][1]

    response = requests.post(f"{url}/channels/create/v2", json = {"token" : token1, "name" : "channel1", "is_public" : True})
    response_channel = response.json()
    channel1_http = response_channel["channel_id"]
    response_channel_invite = requests.post(f"{url}/channel/invite/v2", json = {"token" : token1, "channel_id" : channel1_http, "u_id" : u_id2})
    
    assert response_channel_invite.status_code == 200

    response_channel_invite = requests.post(f"{url}/channel/invite/v2", json = {"token" : token1, "channel_id" : channel1_http, "u_id" : u_id2})
    assert response_channel_invite.status_code == 400

# Owner of the chat tries to invite themselves to the chat
def test_invite_chat_owner(register_three_users):
    token1 = register_three_users["token"][0]
    u_id1 = register_three_users["id"][0]
    
    response = requests.post(f"{url}/channels/create/v2", json = {"token" : token1, "name" : "channel1", "is_public" : True})
    response_channel = response.json()
    channel1_http = response_channel["channel_id"]
    response_channel_invite = requests.post(f"{url}/channel/invite/v2", json = {"token" : token1, "channel_id" : channel1_http, "u_id" : u_id1})
    
    assert response_channel_invite.status_code == 400

# auth_user_id who is trying to invite another user is not a member of the channel
def test_add_invalid_member(register_three_users):
    token1 = register_three_users["token"][0]
    token3 = register_three_users["token"][2]
    u_id2 = register_three_users["id"][1]

    # u_id1 creates the channel
    response = requests.post(f"{url}/channels/create/v2", json = {"token" : token1, "name" : "channel1", "is_public" : True})
    response_channel = response.json()
    channel1_http = response_channel["channel_id"]

    # u_id3 who isn't a member of the channel tries to invite u_id2 
    response_channel_invite = requests.post(f"{url}/channel/invite/v2", json = {"token" : token3, "channel_id" : channel1_http, "u_id" : u_id2})
    assert response_channel_invite.status_code == 403

# Test if an invalid channel_id is put in 
def test_input_invalid_channel(register_three_users):  
    token1 = register_three_users["token"][0]
    u_id2 = register_three_users["id"][1]

    response = requests.post(f"{url}/channels/create/v2", json = {"token" : token1, "name" : "channel1", "is_public" : True})
    response_channel = response.json()
    channel1_http = response_channel["channel_id"]
    response_channel_invite = requests.post(f"{url}/channel/invite/v2", json = {"token" : token1, "channel_id" : channel1_http + 1, "u_id" : u_id2})

    assert response_channel_invite.status_code == 400

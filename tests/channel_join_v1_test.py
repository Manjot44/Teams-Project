from src.config import url
import requests

''' 
HTTP Wrapper Tests 

'''
# Test if a person who successfully joines the channel is in the channel

def test_user_added(register_three_users):
    token1 = register_three_users["token"][0]
    token2 = register_three_users["token"][1]

    response = requests.post(f"{url}/channels/create/v2", json = {"token" : token1, "name" : "channel1", "is_public" : True})
    response_channel = response.json()
    channel1_http = response_channel["channel_id"]
    
    response_channel_join = requests.post(f"{url}/channel/join/v2", json = {"token" : token2, "channel_id" : channel1_http})
    
    assert response_channel_join.status_code == 200

# Test to make sure that when a user joins once, if they try joining they wont join again, where user is not channel or global owner
def test_add_user_twice(register_three_users):
    token1 = register_three_users["token"][0]
    token2 = register_three_users["token"][1]

    response = requests.post(f"{url}/channels/create/v2", json = {"token" : token1, "name" : "channel1", "is_public" : True})
    response_channel = response.json()
    channel1_http = response_channel["channel_id"]

    response_channel_join = requests.post(f"{url}/channel/join/v2", json = {"token" : token2, "channel_id" : channel1_http})
    response_channel_join = requests.post(f"{url}/channel/join/v2", json = {"token" : token2, "channel_id" : channel1_http})

    assert response_channel_join.status_code == 400

# Test to make sure that when a user joins once, if they try joining they wont join again, where user is the owner
def test_add_owner_twice(register_three_users):
    token1 = register_three_users["token"][0]

    response = requests.post(f"{url}/channels/create/v2", json = {"token" : token1, "name" : "channel1", "is_public" : True})
    response_channel = response.json()
    channel1_http = response_channel["channel_id"]

    response_channel_join = requests.post(f"{url}/channel/join/v2", json = {"token" : token1, "channel_id" : channel1_http})

    assert response_channel_join.status_code == 400

# If the channel is private, the user trying to join shouldn't be able to join it
def test_channel_priv(register_three_users):
    token1 = register_three_users["token"][0]
    token2 = register_three_users["token"][1]

    response = requests.post(f"{url}/channels/create/v2", json = {"token" : token1, "name" : "channel1", "is_public" : False})
    response_channel = response.json()
    channel1_http = response_channel["channel_id"]

    response_channel_join = requests.post(f"{url}/channel/join/v2", json = {"token" : token2, "channel_id" : channel1_http})

    assert response_channel_join.status_code == 403

# user tries to join invalid channel
def test_channel_invalid(register_three_users):
    token1 = register_three_users["token"][0]
    token2 = register_three_users["token"][1]

    response = requests.post(f"{url}/channels/create/v2", json = {"token" : token1, "name" : "channel1", "is_public" : True})
    response_channel = response.json()
    channel1 = response_channel["channel_id"]

    response_channel_join = requests.post(f"{url}/channel/join/v2", json = {"token" : token2, "channel_id" : channel1 + 1})

    assert response_channel_join.status_code == 400

# invalid user tries to join channel
def test_user_invalid(register_three_users):    
    token1 = register_three_users["token"][0]

    response = requests.post(f"{url}/channels/create/v2", json = {"token" : token1, "name" : "channel1", "is_public" : True})
    response_channel = response.json()
    channel1_http = response_channel["channel_id"]

    response_channel_join = requests.post(f"{url}/channel/join/v2", json = {"token" : 'incorrect token', "channel_id" : channel1_http + 1})

    assert response_channel_join.status_code == 403

# Global owner tries to join a private channel - Iqtidar is the global owner
def test_global_owner_http(register_three_users):
    token1 = register_three_users["token"][0]
    token2 = register_three_users["token"][1]

    response = requests.post(f"{url}/channels/create/v2", json = {"token" : token2, "name" : "channel1", "is_public" : False})
    response_channel = response.json()
    channel1_http = response_channel["channel_id"]

    response_channel_join = requests.post(f"{url}/channel/join/v2", json = {"token" : token1, "channel_id" : channel1_http})

    assert response_channel_join.status_code == 200

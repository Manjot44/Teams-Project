import requests
import src.config

def test_valid_logout(register_three_users, create_channel):
    user = {}
    user['email'] = "aBc123._%+-@aBc123.-.Co"
    user['password'] = "123456"
    response = requests.post(f"{src.config.url}/auth/login/v2", json = user)
    response_data = response.json()
    second_token = response_data["token"]
    
    create_channel(second_token, "channel_name", True)
    create_channel(register_three_users["token"][0], "channel_name", True)

    response = requests.post(f"{src.config.url}/auth/logout/v1", json = {"token": second_token})
    assert response.status_code == 200

    response = requests.post(f"{src.config.url}/channels/create/v2", json = {"token": second_token, "name": "channel_name", "is_public": True})
    assert response.status_code == 403
    create_channel(register_three_users["token"][0], "channel_name", True)

def test_invalid_token_registered(register_three_users):
    response = requests.post(f"{src.config.url}/auth/logout/v1", json = {"token": None})
    assert response.status_code == 403

def test_invalid_token_unregistered(reset):
    response = requests.post(f"{src.config.url}/auth/logout/v1", json = {"token": None})
    assert response.status_code == 403

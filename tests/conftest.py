from urllib import response
import pytest
import requests
import src.config

@pytest.fixture
def reset():
    requests.delete(f"{src.config.url}/clear/v1")

@pytest.fixture
def register_user():
    def generate_user(email, password, name_first, name_last):
        user = {
            "email": email,
            "password": password,
            "name_first": name_first,
            "name_last": name_last,
        }

        response = requests.post(f"{src.config.url}/auth/register/v2", json = user)

        return response
    
    return generate_user


@pytest.fixture
def register_three_users(reset, register_user):
    user_info = {
        "id": [],
        "token": []
    }

    new_user = register_user("aBc123._%+-@aBc123.-.Co", "123456", "A", "A")
    assert new_user.status_code == 200
    response_data = new_user.json()
    user_info["id"].append(response_data["auth_user_id"])
    user_info["token"].append(response_data["token"])

    new_user = register_user(".@..Ml", "a>?:1#", "1234567890!@#$%^&*()<>?:|_+PqwertyuiPMhsDFtaVclikg", "1234567890!@#$%^&*()<>?:|_+PqwertyuiPMhsDFtaVclikg")
    assert new_user.status_code == 200
    response_data = new_user.json()
    user_info["id"].append(response_data["auth_user_id"])
    user_info["token"].append(response_data["token"])

    new_user = register_user("abc@gmail.com", "thisIsPass13./", "Jerry", "Lin")
    assert new_user.status_code == 200
    response_data = new_user.json()
    user_info["id"].append(response_data["auth_user_id"])
    user_info["token"].append(response_data["token"])

    return user_info

@pytest.fixture
def create_channel():
    def make_channel(token, name, is_public):
        channel_info = {
            "token": token,
            "name": name,
            "is_public": is_public,
        }

        response = requests.post(f"{src.config.url}/channels/create/v2", json = channel_info)
        assert response.status_code == 200
        response_data = response.json()

        return response_data["channel_id"]

    return make_channel

@pytest.fixture
def invite_to_channel():
    def inviting(token, channel_id, u_id):
        info = {
            "token": token,
            "channel_id": channel_id,
            "u_id": u_id,
        }

        response = requests.post(f"{src.config.url}/channel/invite/v2", json = info)

        return response

    return inviting

@pytest.fixture
def create_dm():
    def make_dm(token, u_ids):
        dm_info = {
            'token': token,
            'u_ids': u_ids
        }
        
        response = requests.post(f"{src.config.url}/dm/create/v1", json = dm_info)
        assert response.status_code == 200
        response_data = response.json()

        return response_data['dm_id']

    return make_dm 

from re import A
import pytest
import requests

BASE_ADDRESS = 'http://127.0.0.1'
BASE_PORT = 8080
BASE_URL = f"{BASE_ADDRESS}:{BASE_PORT}"

@pytest.fixture
def register_three_users():
    requests.delete(f"{BASE_URL}/clear/v1")
    new_id = []
    
    user = {
        "email": "aBc123._%+-@aBc123.-.Co",
        "password": "123456",
        "name_first": "A",
        "name_last": "A"
    }

    response = requests.post(f"{BASE_URL}/auth/register/v2", json = user)
    assert response.status_code == 200
    response_data = response.json()
    new_id.append(response_data['auth_user_id'])

    
    user['email'] = ".@..Ml"
    user['password'] = "a>?:1#"
    user['name_first'] = "1234567890!@#$%^&*()<>?:|_+PqwertyuiPMhsDFtaVclikg"
    user['name_last'] = "1234567890!@#$%^&*()<>?:|_+PqwertyuiPMhsDFtaVclikg"

    response = requests.post(f"{BASE_URL}/auth/register/v2", json = user)
    assert response.status_code == 200
    response_data = response.json()
    new_id.append(response_data['auth_user_id'] )


    user['email'] = "abc@gmail.com"
    user['password'] = "thisIsPass13./"
    user['name_first'] = "Jerry"
    user['name_last'] = "Lin"

    response = requests.post(f"{BASE_URL}/auth/register/v2", json = user)
    assert response.status_code == 200
    response_data = response.json()
    new_id.append(response_data['auth_user_id'] )

    return new_id

@pytest.fixture
def user_init():
    user = {
        "email": "abc@gmail.com",
        "password": "thisIsPass13./",
        "name_first": "Jerry",
        "name_last": "Lin"
    }
    return user

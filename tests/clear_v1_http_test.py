import requests
import pytest

BASE_ADDRESS = 'http://127.0.0.1'
BASE_PORT = 8080
BASE_URL = f"{BASE_ADDRESS}:{BASE_PORT}"

def test_clear_v1_1():
    requests.delete(f"{BASE_URL}/clear/v1")

    response = requests.post(f"{BASE_URL}/auth/register/v2", json={"email": "jerrylin@gmail.com", "password": "JerrYlin4", "name_first": "Jerry", "name_last": "Lin"})
    token1 = response.json()["token"]

    requests.delete(f"{BASE_URL}/clear/v1")

    response3 = requests.post(f"{BASE_URL}/channels/create/v2", json={"token": token1, "name": "foo", "is_public": True})
    assert response3.status_code == 403

def test_clear_v1_2():
    requests.delete(f"{BASE_URL}/clear/v1")
    response = requests.delete(f"{BASE_URL}/clear/v1")
    assert response.status_code == 200






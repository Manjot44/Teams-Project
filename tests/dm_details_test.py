import requests

BASE_ADDRESS = 'http://127.0.0.1'
BASE_PORT = 8080
BASE_URL = f"{BASE_ADDRESS}:{BASE_PORT}"


def test_invalid_token():
    requests.delete(f"{BASE_URL}/clear/v1")
    input = {
        "token": "invalidtoken",
        "dm_id": 0
    }
    response = requests.get(f"{BASE_URL}/dm/details/v1", params=input)
    assert response.status_code == 403

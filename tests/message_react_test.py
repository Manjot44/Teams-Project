import requests
from src.config import url

def test_invalid_message(reset, register_user):
    auth_response = requests.post(f"{url}/auth/register/v2", json = {"email": "j@g.com","password": "thisIsPass13./", "name_first": "Je","name_last": "L"})
    auth_data = auth_response.json()
    assert "token" in auth_data
    response = requests.post(f"{url}/channels/create/v2", json = {"token": token, "name": "channel_name", "is_public": True})
    assert response.status_code == 200
    response_data = response.json()
    channel_id = response_data["channel_id"]

    response = requests.post(f"{url}/message/send/v1", json = {"token": token, "channel_id": channel_id, "message": "Hello Sanjam"})
    assert response.status_code == 200    
    response_data = response.json()
    message_id = response_data["message_id"]
    response = requests.post(f"{url}/message/react/v1", json = {"token": token, "message_id": message_id + 1, react_id: 1})
    assert response.status_code == 400
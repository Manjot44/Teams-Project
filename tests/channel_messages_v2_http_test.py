import requests
from src.config import url

def test_invalid_channel_id():
    requests.delete(f"{url}/clear/v1")

    response = requests.post(f"{url}/auth/register/v2", json={"email": "jerrylin@gmail.com", "password": "JerrYlin4", "name_first": "Jerry", "name_last": "Lin"})
    token1 = response.json()['token']

    input = {
        "token": token1,
        "name": "foo",
        "is_public": True
    }

    response2 = requests.post(f"{url}/channels/create/v2", json=input)
    assert response2.status_code == 200
    invalid_channel_id = 10

    response3 = requests.get(f"{url}/channel/messages/v2?token={token1}&channel_id={invalid_channel_id}&start={0}")
    assert response3.status_code == 400

def test_user_invalid():  
    requests.delete(f"{url}/clear/v1")

    response = requests.post(f"{url}/auth/register/v2", json={"email": "jerrylin@gmail.com", "password": "JerrYlin4", "name_first": "Jerry", "name_last": "Lin"})
    token1 = response.json()["token"]
    response2 = requests.post(f"{url}/auth/register/v2", json={"email": "manjotbhathal@gmail.com", "password": "ManJoTBhathAl4", "name_first": "Manjot", "name_last": "Bhathal"})    
    token2 = response2.json()["token"]
   
    input = {
        "token": token1,
        "name": "channel_jerry",
        "is_public": True
    }

    response3 = requests.post(f"{url}/channels/create/v2", json=input)
    channel_id1 = response3.json()['channel_id']

    response4 = requests.get(f"{url}/channel/messages/v2?token={token2}&channel_id={channel_id1}&start={0}")
    assert response4.status_code == 403

def test_valid_start_no_messages():
    requests.delete(f"{url}/clear/v1")

    response = requests.post(f"{url}/auth/register/v2", json={"email": "jerrylin@gmail.com", "password": "JerrYlin4", "name_first": "Jerry", "name_last": "Lin"})
    token1 = response.json()["token"]

    input = {
        "token": token1,
        "name": "foo",
        "is_public": True
    }

    response2 = requests.post(f"{url}/channels/create/v2", json=input)
    channel_id = response2.json()['channel_id']

    response3 = requests.get(f"{url}/channel/messages/v2?token={token1}&channel_id={channel_id}&start={10}")
    assert response3.status_code == 400

def test_valid_start():
    requests.delete(f"{url}/clear/v1")

    response = requests.post(f"{url}/auth/register/v2", json={"email": "jerrylin@gmail.com", "password": "JerrYlin4", "name_first": "Jerry", "name_last": "Lin"})
    token1 = response.json()["token"]

    input = {
        "token": token1,
        "name": "foo",
        "is_public": True
    }

    response2 = requests.post(f"{url}/channels/create/v2", json=input)
    channel_id = response2.json()['channel_id']

    response3 = requests.get(f"{url}/channel/messages/v2?token={token1}&channel_id={channel_id}&start={0}")
    assert response3.status_code == 200

    messagesreturn = {
        'messages': [],
        'start': 0, 
        'end': -1
    } 

    response_data = response3.json()
    assert response_data == messagesreturn

def test_user_registered():  
    requests.delete(f"{url}/clear/v1")

    response = requests.post(f"{url}/auth/register/v2", json={"email": "jerrylin@gmail.com", "password": "JerrYlin4", "name_first": "Jerry", "name_last": "Lin"})
    token1 = response.json()["token"]
    unregistered_token = "unregistered_user" 
    input = {
        "token": token1,
        "name": "foo",
        "is_public": True
    }

    response2 = requests.post(f"{url}/channels/create/v2", json=input)
    channel_id = response2.json()['channel_id']

    response3 = requests.get(f"{url}/channel/messages/v2?token={unregistered_token}&channel_id={channel_id}&start={0}")
    assert response3.status_code == 403

def test_invalid_token():
    requests.delete(f"{url}/clear/v1")   

    response = requests.post(f"{url}/auth/register/v2", json={"email": "jerrylin@gmail.com", "password": "JerrYlin4", "name_first": "Jerry", "name_last": "Lin"})
    token1 = response.json()["token"]
    invalid_token = "invalid_token"
    input = {
        "token": token1,
        "name": "foo",
        "is_public": True
    }

    response2 = requests.post(f"{url}/channels/create/v2", json=input)
    channel_id = response2.json()['channel_id']

    response3 = requests.get(f"{url}/channel/messages/v2?token={invalid_token}&channel_id={channel_id}&start={0}")
    assert response3.status_code == 403 

def test_send_50_messages():
    requests.delete(f"{url}/clear/v1")   

    response = requests.post(f"{url}/auth/register/v2", json={"email": "jerrylin@gmail.com", "password": "JerrYlin4", "name_first": "Jerry", "name_last": "Lin"})
    token1 = response.json()["token"]
    input = {
        "token": token1,
        "name": "foo",
        "is_public": True
    }

    response2 = requests.post(f"{url}/channels/create/v2", json=input)
    channel_id = response2.json()['channel_id']

    i = 0
    while i < 60:
        response = requests.post(f"{url}/message/send/v1", json = {"token": token1, "channel_id": channel_id, "message": "lolthony ecsdee"})
        assert response.status_code == 200
        i += 1

    response3 = requests.get(f"{url}/channel/messages/v2?token={token1}&channel_id={channel_id}&start={0}")
    assert response3.status_code == 200
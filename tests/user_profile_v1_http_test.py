import requests
import src.config

def test_invalid_uid():
    requests.delete(f"{src.config.url}/clear/v1")

    response = requests.post(f"{src.config.url}/auth/register/v2", json = {"email": "jerrylin@gmail.com", "password": "JerrYlin4", "name_first": "Jerry", "name_last": "Lin"})
    user = response.json()

    response2 = requests.get(f"{src.config.url}/user/profile/v1", params = {"token": user['token'], "u_id": 10})
    assert response2.status_code == 400


def test_invalid_token():
    requests.delete(f"{src.config.url}/clear/v1")

    response = requests.post(f"{src.config.url}/auth/register/v2", json = {"email": "jerrylin@gmail.com", "password": "JerrYlin4", "name_first": "Jerry", "name_last": "Lin"})
    user = response.json()

    response2 = requests.get(f"{src.config.url}/user/profile/v1", params = {"token": -1, "u_id": user['auth_user_id']})
    assert response2.status_code == 403

def test_correct_return():
    requests.delete(f"{src.config.url}/clear/v1")

    response = requests.post(f"{src.config.url}/auth/register/v2", json = {"email": "jerrylin@gmail.com", "password": "JerrYlin4", "name_first": "Jerry", "name_last": "Lin"})
    user = response.json()

    response2 = requests.get(f"{src.config.url}/user/profile/v1", params = {"token": user['token'], "u_id": user['auth_user_id']}) 
    assert response2.status_code == 200
    
    assert response2.json() == {'user': {
                                    'u_id': user['auth_user_id'], 
                                    'email': "jerrylin@gmail.com", 
                                    'name_first': 'Jerry', 
                                    'name_last': 'Lin', 
                                    'handle_str': 'jerrylin',
                                    'profile_img_url': None
    }}

def test_correct_return_removed_user(): 
    requests.delete(f"{src.config.url}/clear/v1")

    response = requests.post(f"{src.config.url}/auth/register/v2", json = {"email": "jerrylin@gmail.com", "password": "JerrYlin4", "name_first": "Jerry", "name_last": "Lin"})
    user = response.json()
    
    response1 = requests.post(f"{src.config.url}/auth/register/v2", json = {"email": "manjot@gmail.com", "password": "ManYlin4", "name_first": "Manjot", "name_last": "Bhathal"})
    user2 = response1.json()

    requests.post(f"{src.config.url}/admin/userpermission/change/v1", json = {"token": user['token'], "u_id": user2['auth_user_id'], "permission_id": 1})

    response2 = requests.delete(f"{src.config.url}/admin/user/remove/v1", json = {"token": user['token'], "u_id": user['auth_user_id']})
    assert response2.status_code == 200

    response3 = requests.get(f"{src.config.url}/user/profile/v1", params = {"token": user2['token'], "u_id": user['auth_user_id']}) 
    assert response3.status_code == 200

    assert response3.json() == {'user': {
                                    'u_id': user['auth_user_id'], 
                                    'email': None, 
                                    'name_first': 'Removed', 
                                    'name_last': 'user', 
                                    'handle_str': None,
                                    'profile_img_url': None
    }}
import requests
import src.config

def test_correct_output():
    requests.delete(f"{src.config.url}/clear/v1")

    response = requests.post(f"{src.config.url}/auth/register/v2", json = {"email": "jerrylin@gmail.com", "password": "JerrYlin4", "name_first": "Jerry", "name_last": "Lin"})
    user = response.json()
    
    response2 =  requests.put(f"{src.config.url}/user/profile/setname/v1", json= {"token": user['token'], "name_first": "Monta", "name_last": "Jree"})  
    assert response2.status_code == 200

    response3 = requests.get(f"{src.config.url}/user/profile/v1", params = {"token": user['token'], "u_id": user['auth_user_id']}) 

    return_val = response3.json()
    assert return_val == {'user': {
                                    'u_id': user['auth_user_id'], 
                                    'email': "jerrylin@gmail.com", 
                                    'name_first': 'Monta', 
                                    'name_last': 'Jree', 
                                    'handle_str': 'jerrylin',
                                    'profile_img_url': f'{src.config.url}src/static/default.jpg'
    }}

def test_invalid_first_name1():
    requests.delete(f"{src.config.url}/clear/v1")

    response = requests.post(f"{src.config.url}/auth/register/v2", json = {"email": "jerrylin@gmail.com", "password": "JerrYlin4", "name_first": "Jerry", "name_last": "Lin"})
    user1 = response.json()

    response2 = requests.put(f"{src.config.url}/user/profile/setname/v1", json = {"token": user1["token"], "name_first": "Montamontamontamontamontamontamontamontamontamontamonta", "name_last": "Jree"})
    assert response2.status_code == 400   

def test_invalid_first_name2():  
    requests.delete(f"{src.config.url}/clear/v1")

    response = requests.post(f"{src.config.url}/auth/register/v2", json = {"email": "jerrylin@gmail.com", "password": "JerrYlin4", "name_first": "Jerry", "name_last": "Lin"})
    user1 = response.json()

    response2 = requests.put(f"{src.config.url}/user/profile/setname/v1", json = {"token": user1["token"], "name_first": "", "name_last": "Jree"})
    assert response2.status_code == 400  

def test_invalid_last_name1():
    requests.delete(f"{src.config.url}/clear/v1")

    response = requests.post(f"{src.config.url}/auth/register/v2", json = {"email": "jerrylin@gmail.com", "password": "JerrYlin4", "name_first": "Jerry", "name_last": "Lin"})
    user1 = response.json()

    response2 = requests.put(f"{src.config.url}/user/profile/setname/v1", json = {"token": user1["token"], "name_first": "Monta", "name_last": "Jreemontamontamontamontamontamontamontamontamontamontamontamonta"})
    assert response2.status_code == 400  

def test_invalid_last_name2():
    requests.delete(f"{src.config.url}/clear/v1")

    response = requests.post(f"{src.config.url}/auth/register/v2", json = {"email": "jerrylin@gmail.com", "password": "JerrYlin4", "name_first": "Jerry", "name_last": "Lin"})
    user1 = response.json()

    response2 = requests.put(f"{src.config.url}/user/profile/setname/v1", json = {"token": user1["token"], "name_first": "Monta", "name_last": ""})
    assert response2.status_code == 400 

def test_invalid_token():
    requests.delete(f"{src.config.url}/clear/v1")

    response = requests.post(f"{src.config.url}/auth/register/v2", json = {"email": "jerrylin@gmail.com", "password": "JerrYlin4", "name_first": "Jerry", "name_last": "Lin"})
    assert response.status_code == 200
    response2 = requests.put(f"{src.config.url}/user/profile/setname/v1", json = {"token": -1, "name_first": "Monta", "name_last": "Jree"})
    assert response2.status_code == 403   
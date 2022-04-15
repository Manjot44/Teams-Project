import requests
import src.config

def test_authlog_valid(register_three_users):
    user = {}
    user['email'] = "aBc123._%+-@aBc123.-.Co"
    user['password'] = "123456"
    response = requests.post(f"{src.config.url}/auth/login/v2", json = user)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['auth_user_id'] == register_three_users["id"][0]

    user['email'] = ".@..Ml"
    user['password'] = "a>?:1#"
    response = requests.post(f"{src.config.url}/auth/login/v2", json = user)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['auth_user_id'] == register_three_users["id"][1]

def test_incorrect_details(register_three_users):
    user = {}
    user['email'] = "aBc12._%+-@aBc123.-.Co"
    user['password'] = "123456"
    response = requests.post(f"{src.config.url}/auth/login/v2", json = user)
    assert response.status_code == 400

    user['email'] = "aBc123._%+-@aBc123.-.Co"
    user['password'] = "1234576"
    response = requests.post(f"{src.config.url}/auth/login/v2", json = user)
    assert response.status_code == 400                 

def test_empty(register_three_users):
    user = {}
    user['email'] = ""
    user['password'] = "123456"
    response = requests.post(f"{src.config.url}/auth/login/v2", json = user)
    assert response.status_code == 400

    user['email'] = "aBc123._%+-@aBc123.-.Co"
    user['password'] = ""   
    response = requests.post(f"{src.config.url}/auth/login/v2", json = user)
    assert response.status_code == 400                        

def test_mixed_password(register_three_users):
    user = {}
    user['email'] = "aBc123._%+-@aBc123.-.Co"
    user['password'] = "a>?:1#"   
    response = requests.post(f"{src.config.url}/auth/login/v2", json = user)
    assert response.status_code == 400                        
    
    user['email'] = ".@..Ml"
    user['password'] = "123456"   
    response = requests.post(f"{src.config.url}/auth/login/v2", json = user)
    assert response.status_code == 400                                                            

def test_no_registered_user(reset):
    user = {}
    user['email'] = "abc@gmail.com"
    user['password'] = "thisIsPass13./"
    response = requests.post(f"{src.config.url}/auth/login/v2", json = user)
    assert response.status_code == 400

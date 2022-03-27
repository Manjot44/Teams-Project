import src.auth
import src.channels
import src.channel
import pytest 
import requests

BASE_ADDRESS = 'http://127.0.0.1'
BASE_PORT = 8080
BASE_URL = f"{BASE_ADDRESS}:{BASE_PORT}"

def test_authreg_valid(register_three_users):
    for id in register_three_users["id"]:
        assert isinstance(id, int)
    
    assert register_three_users["id"][0] != register_three_users["id"][1]
    assert register_three_users["id"][0] != register_three_users["id"][2] 
    assert register_three_users["id"][1] != register_three_users["id"][2]

def test_email_missing_element(user_init):
    requests.delete(f"{BASE_URL}/clear/v1")
    user_init['email'] = "abcgmail.com"
    response = requests.post(f"{BASE_URL}/auth/register/v2", json = user_init)
    assert response.status_code == 400
   
    user_init['email'] = "abc@gmailcom"
    response = requests.post(f"{BASE_URL}/auth/register/v2", json = user_init)
    assert response.status_code == 400
     
    user_init['email'] = "abc@gmail.M"
    response = requests.post(f"{BASE_URL}/auth/register/v2", json = user_init)
    assert response.status_code == 400     

def test_email_repeat(user_init):
    requests.delete(f"{BASE_URL}/clear/v1")
    requests.post(f"{BASE_URL}/auth/register/v2", json = user_init) 
    response = requests.post(f"{BASE_URL}/auth/register/v2", json = user_init)
    assert response.status_code == 400 

def test_email_invalid_char(user_init):
    requests.delete(f"{BASE_URL}/clear/v1")
    user_init['email'] = "abc%^@gmail.com"
    response = requests.post(f"{BASE_URL}/auth/register/v2", json = user_init)
    assert response.status_code == 400

    user_init['email'] = "abc@gmail.+.com"
    response = requests.post(f"{BASE_URL}/auth/register/v2", json = user_init)
    assert response.status_code == 400

    user_init['email'] = "abc@gmail.co2"
    response = requests.post(f"{BASE_URL}/auth/register/v2", json = user_init)
    assert response.status_code == 400

    user_init['email'] = "abc@gmail.co.*"
    response = requests.post(f"{BASE_URL}/auth/register/v2", json = user_init)
    assert response.status_code == 400 

def test_email_empty_section(user_init):
    requests.delete(f"{BASE_URL}/clear/v1")
    user_init['email'] = "@gmail.com"
    response = requests.post(f"{BASE_URL}/auth/register/v2", json = user_init)
    assert response.status_code == 400

    user_init['email'] = "abc@.com"
    response = requests.post(f"{BASE_URL}/auth/register/v2", json = user_init)
    assert response.status_code == 400

    user_init['email'] = "abc@gmail."
    response = requests.post(f"{BASE_URL}/auth/register/v2", json = user_init)
    assert response.status_code == 400

    user_init['email'] = ""
    response = requests.post(f"{BASE_URL}/auth/register/v2", json = user_init)
    assert response.status_code == 400                

def test_password_invalid(user_init):
    requests.delete(f"{BASE_URL}/clear/v1")
    user_init['password'] = "1>;[g"
    response = requests.post(f"{BASE_URL}/auth/register/v2", json = user_init)
    assert response.status_code == 400
    
    user_init['password'] = ""
    response = requests.post(f"{BASE_URL}/auth/register/v2", json = user_init)
    assert response.status_code == 400     
            
def test_names_empty(user_init):
    requests.delete(f"{BASE_URL}/clear/v1")
    user_init['name_last'] = ""
    response = requests.post(f"{BASE_URL}/auth/register/v2", json = user_init)
    assert response.status_code == 400

    user_init['name_first'] = ""
    response = requests.post(f"{BASE_URL}/auth/register/v2", json = user_init)
    assert response.status_code == 400

def test_names_long(user_init):
    requests.delete(f"{BASE_URL}/clear/v1")
    user_init['name_last'] = "1234567890!@#$%^&*()<>?:|_+PqwertyuiPMhsDFtaVclikg8"
    response = requests.post(f"{BASE_URL}/auth/register/v2", json = user_init)
    assert response.status_code == 400

    user_init['name_first'] = "1234567890!@#$%^&*()<>?:|_+PqwertyuiPMhsDFtaVclikg8"
    response = requests.post(f"{BASE_URL}/auth/register/v2", json = user_init)
    assert response.status_code == 400
               



def test_handle_normal(user_init):
    requests.delete(f"{BASE_URL}/clear/v1")
    response = requests.post(f"{BASE_URL}/auth/register/v2", json = user_init)
    assert response.status_code == 200
    response_data = response.json()
    token = response_data["token"]

    response = requests.post(f"{BASE_URL}/channels/create/v2", json = {"token": token, "name": "channel_name", "is_public": True})
    assert response.status_code == 200
    response_data = response.json()
    channel_id = response_data["channel_id"]

    response = requests.get(f"{BASE_URL}/channel/details/v2?token={token}&channel_id={channel_id}")
    assert response.status_code == 200
    response_data = response.json()
    generated_handle = response_data["all_members"][0]["handle_str"]

    expected_handle = "jerrylin"
    assert generated_handle == expected_handle

def test_border_handle_long(user_init):
    requests.delete(f"{BASE_URL}/clear/v1")
    user_init["name_first"] = "Iamthegreatest"
    user_init["name_last"] = "JerryL"

    response = requests.post(f"{BASE_URL}/auth/register/v2", json = user_init)
    assert response.status_code == 200
    response_data = response.json()
    token = response_data["token"]

    response = requests.post(f"{BASE_URL}/channels/create/v2", json = {"token": token, "name": "channel_name", "is_public": True})
    assert response.status_code == 200
    response_data = response.json()
    channel_id = response_data["channel_id"]

    response = requests.get(f"{BASE_URL}/channel/details/v2?token={token}&channel_id={channel_id}")
    assert response.status_code == 200
    response_data = response.json()
    generated_handle = response_data["all_members"][0]["handle_str"]

    expected_handle = "iamthegreatestjerryl"
    assert generated_handle == expected_handle

    
    
    requests.delete(f"{BASE_URL}/clear/v1")
    user_init["name_last"] = "JerryLi"

    response = requests.post(f"{BASE_URL}/auth/register/v2", json = user_init)
    assert response.status_code == 200
    response_data = response.json()
    token = response_data["token"]

    response = requests.post(f"{BASE_URL}/channels/create/v2", json = {"token": token, "name": "channel_name", "is_public": True})
    assert response.status_code == 200
    response_data = response.json()
    channel_id = response_data["channel_id"]

    response = requests.get(f"{BASE_URL}/channel/details/v2?token={token}&channel_id={channel_id}")
    assert response.status_code == 200
    response_data = response.json()
    generated_handle = response_data["all_members"][0]["handle_str"]

    assert generated_handle == expected_handle

def test_handle_repeat(user_init):
    requests.delete(f"{BASE_URL}/clear/v1")
    
    response = requests.post(f"{BASE_URL}/auth/register/v2", json = user_init)
    assert response.status_code == 200

    user_init['email'] = "jerrylin@gmail.com"
    response = requests.post(f"{BASE_URL}/auth/register/v2", json = user_init)
    assert response.status_code == 200
    response_data = response.json()
    token = response_data["token"]

    response = requests.post(f"{BASE_URL}/channels/create/v2", json = {"token": token, "name": "channel_name", "is_public": True})
    assert response.status_code == 200
    response_data = response.json()
    channel_id = response_data["channel_id"]

    response = requests.get(f"{BASE_URL}/channel/details/v2?token={token}&channel_id={channel_id}")
    assert response.status_code == 200
    response_data = response.json()
    generated_handle = response_data["all_members"][0]["handle_str"]

    expected_handle = "jerrylin0"
    assert generated_handle == expected_handle

def test_long_handle_repeat(user_init):
    requests.delete(f"{BASE_URL}/clear/v1")
    user_init["name_first"] = "Iamthegreatest"
    user_init["name_last"] = "JerryLi"

    response = requests.post(f"{BASE_URL}/auth/register/v2", json = user_init)
    assert response.status_code == 200

    user_init["email"] = "jerrylin@gmail.com"
    response = requests.post(f"{BASE_URL}/auth/register/v2", json = user_init)
    assert response.status_code == 200
    response_data = response.json()
    token = response_data["token"]

    response = requests.post(f"{BASE_URL}/channels/create/v2", json = {"token": token, "name": "channel_name", "is_public": True})
    assert response.status_code == 200
    response_data = response.json()
    channel_id = response_data["channel_id"]

    response = requests.get(f"{BASE_URL}/channel/details/v2?token={token}&channel_id={channel_id}")
    assert response.status_code == 200
    response_data = response.json()
    generated_handle = response_data["all_members"][0]["handle_str"]

    expected_handle = "iamthegreatestjerryl0"
    assert generated_handle == expected_handle

def test_handle_double_repeat(user_init):
    requests.delete(f"{BASE_URL}/clear/v1")
    user_init["name_first"] = "abc"
    user_init["name_last"] = "def"

    response = requests.post(f"{BASE_URL}/auth/register/v2", json = user_init)
    assert response.status_code == 200

    user_init["email"] = "jerrylin@gmail.com"
    user_init["name_last"] = "def0"
    response = requests.post(f"{BASE_URL}/auth/register/v2", json = user_init)
    assert response.status_code == 200

    user_init["email"] = "jerry@gmail.com"
    user_init["name_last"] = "def"
    response = requests.post(f"{BASE_URL}/auth/register/v2", json = user_init)
    assert response.status_code == 200
    response_data = response.json()
    token = response_data["token"]

    response = requests.post(f"{BASE_URL}/channels/create/v2", json = {"token": token, "name": "channel_name", "is_public": True})
    assert response.status_code == 200
    response_data = response.json()
    channel_id = response_data["channel_id"]

    print(channel_id)
    
    response = requests.get(f"{BASE_URL}/channel/details/v2?token={token}&channel_id={channel_id}")
    assert response.status_code == 200
    response_data = response.json()
    generated_handle = response_data["all_members"][0]["handle_str"]

    expected_handle = "abcdef1"
    assert generated_handle == expected_handle

import src.auth
import src.channels
import src.channel
import pytest 
import requests

BASE_ADDRESS = 'http://127.0.0.1'
BASE_PORT = 8080
BASE_URL = f"{BASE_ADDRESS}:{BASE_PORT}"

def test_authreg_valid(register_three_users):
    for id in register_three_users:
        assert isinstance(id, int)
    
    assert register_three_users[0] != register_three_users[1]
    assert register_three_users[0] != register_three_users[2] 
    assert register_three_users[1] != register_three_users[2]

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
               



# def test_handle_normal():
#     clear_v1()
#     user_id = src.auth.auth_register_v1("jerrylin@gmail.com", "123456", "Jerry", "Lin")["auth_user_id"]
#     channel_id = src.channels.channels_create_v1(user_id, "new channel", True)["channel_id"]
#     generated_handle = src.channel.channel_details_v1(user_id, channel_id)["all_members"][0]["handle_str"]

#     expected_handle = "jerrylin"
#     assert generated_handle == expected_handle

# def test_border_handle_long():
#     clear_v1()
#     user_id = src.auth.auth_register_v1("jerrylin@gmail.com", "123456", "Iamthegreatest", "JerryL")["auth_user_id"]
#     channel_id = src.channels.channels_create_v1(user_id, "new channel", True)["channel_id"]
#     generated_handle = src.channel.channel_details_v1(user_id, channel_id)["all_members"][0]["handle_str"]

#     expected_handle = "iamthegreatestjerryl"
#     assert generated_handle == expected_handle

#     clear_v1()
#     user_id = src.auth.auth_register_v1("jerrylin@gmail.com", "123456", "Iamthegreatest", "JerryLi")["auth_user_id"]
#     channel_id = src.channels.channels_create_v1(user_id, "new channel", True)["channel_id"]
#     generated_handle = src.channel.channel_details_v1(user_id, channel_id)["all_members"][0]["handle_str"]

#     assert generated_handle == expected_handle

# def test_handle_repeat():
#     clear_v1()
#     src.auth.auth_register_v1("jerrylin@gmail.com", "123456", "Jerry", "Lin")
#     user_id = src.auth.auth_register_v1("jerry@gmail.com", "123456", "Jerry", "Lin")["auth_user_id"]
#     channel_id = src.channels.channels_create_v1(user_id, "new channel", True)["channel_id"]
#     generated_handle = src.channel.channel_details_v1(user_id, channel_id)["all_members"][0]["handle_str"]

#     expected_handle = "jerrylin0"
#     assert generated_handle == expected_handle

# def test_long_handle_repeat():
#     clear_v1()
#     src.auth.auth_register_v1("jerrylin@gmail.com", "123456", "Iamthegreatest", "JerryLi")
#     user_id = src.auth.auth_register_v1("jerry@gmail.com", "123456", "Iamthegreatest", "JerryLi")["auth_user_id"]
#     channel_id = src.channels.channels_create_v1(user_id, "new channel", True)["channel_id"]
#     generated_handle = src.channel.channel_details_v1(user_id, channel_id)["all_members"][0]["handle_str"]

#     expected_handle = "iamthegreatestjerryl0"
#     assert generated_handle == expected_handle

# def test_handle_double_repeat():
#     clear_v1()
#     src.auth.auth_register_v1("jerrylin@gmail.com", "123456", "abc", "def")
#     src.auth.auth_register_v1("jerryl@gmail.com", "123456", "abc", "def0")
#     user_id = src.auth.auth_register_v1("jerry@gmail.com", "123456", "abc", "def")
#     channel_id = src.channels.channels_create_v1(user_id, "new channel", True)["channel_id"]
#     generated_handle = src.channel.channel_details_v1(user_id, channel_id)["all_members"][0]["handle_str"]

#     expected_handle = "abcdef1"
#     assert generated_handle == expected_handle

import requests
import src.config

def test_authreg_valid(register_three_users):
    for id in register_three_users["id"]:
        assert isinstance(id, int)
    
    assert len(register_three_users["id"]) == len(set(register_three_users["id"]))

def test_email_missing_element(reset, register_user):
    response = register_user("abcgmail.com", "thisIsPass13./", "Jerry", "Lin")
    assert response.status_code == 400

    response = register_user("abc@gmailcom", "thisIsPass13./", "Jerry", "Lin")
    assert response.status_code == 400
    
    response = register_user("abc@gmail.M", "thisIsPass13./", "Jerry", "Lin")
    assert response.status_code == 400 

def test_email_repeat(reset, register_user):
    register_user("abc@gmail.com", "thisIsPass13./", "Jerry", "Lin")
    response = register_user("abcgmail.com", "thisIsPass13./", "Jerry", "Lin")
    assert response.status_code == 400 

def test_email_invalid_char(reset, register_user):
    response = register_user("abc%^@gmail.com", "thisIsPass13./", "Jerry", "Lin")
    assert response.status_code == 400
    
    response = register_user("abc@gmail.+.com", "thisIsPass13./", "Jerry", "Lin")
    assert response.status_code == 400

    response = register_user("abc@gmail.co2", "thisIsPass13./", "Jerry", "Lin")
    assert response.status_code == 400

    response = register_user("abc@gmail.co.*", "thisIsPass13./", "Jerry", "Lin")
    assert response.status_code == 400

def test_email_empty_section(reset, register_user):
    response = register_user("@gmail.com", "thisIsPass13./", "Jerry", "Lin")
    assert response.status_code == 400

    response = register_user("abc@.com", "thisIsPass13./", "Jerry", "Lin")
    assert response.status_code == 400

    response = register_user("abc@gmail.", "thisIsPass13./", "Jerry", "Lin")
    assert response.status_code == 400

    response = register_user("", "thisIsPass13./", "Jerry", "Lin")
    assert response.status_code == 400               

def test_password_invalid(reset, register_user):
    response = register_user("abc@gmail.com", "1>;[g", "Jerry", "Lin")
    assert response.status_code == 400

    response = register_user("abc@gmail.com", "", "Jerry", "Lin")
    assert response.status_code == 400
            
def test_names_empty(reset, register_user):
    response = register_user("abc@gmail.com", "thisIsPass13./", "Jerry", "")
    assert response.status_code == 400

    response = register_user("abc@gmail.com", "thisIsPass13./", "", "Lin")
    assert response.status_code == 400

def test_names_long(reset, register_user):
    response = register_user("abc@gmail.com", "thisIsPass13./", "Jerry", "1234567890!@#$%^&*()<>?:|_+PqwertyuiPMhsDFtaVclikg8")
    assert response.status_code == 400

    response = register_user("abc@gmail.com", "thisIsPass13./", "1234567890!@#$%^&*()<>?:|_+PqwertyuiPMhsDFtaVclikg8", "Lin")
    assert response.status_code == 400
               



def test_handle_normal(reset, register_user):
    response = register_user("abc@gmail.com", "thisIsPass13./", "Jerry", "Lin")
    assert response.status_code == 200
    response_data = response.json()
    token = response_data["token"]
    u_id = response_data["auth_user_id"]

    response = requests.get(f"{src.config.url}/user/profile/v1?token={token}&u_id={u_id}")
    assert response.status_code == 200
    response_data = response.json()
    generated_handle = response_data["user"]["handle_str"]

    expected_handle = "jerrylin"
    assert generated_handle == expected_handle

def test_border_handle_20_len(reset, register_user):
    response = register_user("abc@gmail.com", "thisIsPass13./", "Iamthegreatest", "JerryL")
    assert response.status_code == 200
    response_data = response.json()
    token = response_data["token"]
    u_id = response_data["auth_user_id"]

    response = requests.get(f"{src.config.url}/user/profile/v1?token={token}&u_id={u_id}")
    assert response.status_code == 200
    response_data = response.json()
    generated_handle = response_data["user"]["handle_str"]

    expected_handle = "iamthegreatestjerryl"
    assert generated_handle == expected_handle
    
def test_border_handle_21_len(reset, register_user):
    response = register_user("abc@gmail.com", "thisIsPass13./", "Iamthegreatest", "JerryLi")
    assert response.status_code == 200
    response_data = response.json()
    token = response_data["token"]
    u_id = response_data["auth_user_id"]

    response = requests.get(f"{src.config.url}/user/profile/v1?token={token}&u_id={u_id}")
    assert response.status_code == 200
    response_data = response.json()
    generated_handle = response_data["user"]["handle_str"]

    expected_handle = "iamthegreatestjerryl"
    assert generated_handle == expected_handle
    
def test_handle_repeat(reset, register_user):
    response = register_user("abc@gmail.com", "thisIsPass13./", "Jerry", "Lin")
    assert response.status_code == 200
    
    response = register_user("jerrylin@gmail.com", "thisIsPass13./", "Jerry", "Lin")
    assert response.status_code == 200
    response_data = response.json()
    token = response_data["token"]
    u_id = response_data["auth_user_id"]

    response = requests.get(f"{src.config.url}/user/profile/v1?token={token}&u_id={u_id}")
    assert response.status_code == 200
    response_data = response.json()
    generated_handle = response_data["user"]["handle_str"]

    expected_handle = "jerrylin0"
    assert generated_handle == expected_handle

def test_long_handle_repeat(reset, register_user):
    response = register_user("abc@gmail.com", "thisIsPass13./", "Iamthegreatest", "JerryLi")
    assert response.status_code == 200
    
    response = register_user("jerrylin@gmail.com", "thisIsPass13./", "Iamthegreatest", "JerryLi")
    assert response.status_code == 200
    response_data = response.json()
    token = response_data["token"]
    u_id = response_data["auth_user_id"]

    response = requests.get(f"{src.config.url}/user/profile/v1?token={token}&u_id={u_id}")
    assert response.status_code == 200
    response_data = response.json()
    generated_handle = response_data["user"]["handle_str"]

    expected_handle = "iamthegreatestjerryl0"
    assert generated_handle == expected_handle

def test_handle_double_repeat_special(reset, register_user):
    response = register_user("abc@gmail.com", "thisIsPass13./", "abc", "def")
    assert response.status_code == 200

    response = register_user("jerrylin@gmail.com", "thisIsPass13./", "abc", "def0")
    assert response.status_code == 200

    response = register_user("jerry@gmail.com", "thisIsPass13./", "abc", "def")
    assert response.status_code == 200
    response_data = response.json()
    token = response_data["token"]
    u_id = response_data["auth_user_id"]

    response = requests.get(f"{src.config.url}/user/profile/v1?token={token}&u_id={u_id}")
    assert response.status_code == 200
    response_data = response.json()
    generated_handle = response_data["user"]["handle_str"]

    expected_handle = "abcdef1"
    assert generated_handle == expected_handle

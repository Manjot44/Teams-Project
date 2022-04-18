import requests
import src.config
import src.persistence

def test_pwdreset_request_sanity(register_three_users):
    response = requests.post(f"{src.config.url}/auth/passwordreset/request/v1", json = {"email": "abc@gmail.com"})
    assert response.status_code == 200

    response = requests.post(f"{src.config.url}/auth/passwordreset/request/v1", json = {"email": "randomemail@gmail.com"})
    assert response.status_code == 200

def test_whitebox_correct_reset_code(register_three_users):
    requests.post(f"{src.config.url}/auth/passwordreset/request/v1", json = {"email": "abc@gmail.com"})
    
    store = src.persistence.get_pickle()
    expected_reset_code = store["users"][2]["reset_codes"][0]
    response = requests.post(f"{src.config.url}/auth/passwordreset/reset/v1", json = {"reset_code": expected_reset_code, "new_password": "validpass"})
    assert response.status_code == 200

    response = requests.post(f"{src.config.url}/auth/login/v2", json = {"email": "abc@gmail.com", "password": "validpass"})
    assert response.status_code == 200

def test_whitebox_short_password(register_three_users):
    requests.post(f"{src.config.url}/auth/passwordreset/request/v1", json = {"email": "abc@gmail.com"})
    
    store = src.persistence.get_pickle()
    expected_reset_code = store["users"][2]["reset_codes"][0]
    response = requests.post(f"{src.config.url}/auth/passwordreset/reset/v1", json = {"reset_code": expected_reset_code, "new_password": "short"})
    assert response.status_code == 400

def test_invalid_code(register_three_users):
    requests.post(f"{src.config.url}/auth/passwordreset/request/v1", json = {"email": "abc@gmail.com"})
    response = requests.post(f"{src.config.url}/auth/passwordreset/reset/v1", json = {"reset_code": "invalidcode", "new_password": "short"})
    assert response.status_code == 400

def test_whitebox_multiple_reset_codes(register_three_users):
    requests.post(f"{src.config.url}/auth/passwordreset/request/v1", json = {"email": "abc@gmail.com"})
    requests.post(f"{src.config.url}/auth/passwordreset/request/v1", json = {"email": "abc@gmail.com"})

    store = src.persistence.get_pickle()
    expected_reset_code = store["users"][2]["reset_codes"][1]
    response = requests.post(f"{src.config.url}/auth/passwordreset/reset/v1", json = {"reset_code": expected_reset_code, "new_password": "validpass"})
    assert response.status_code == 200

    response = requests.post(f"{src.config.url}/auth/login/v2", json = {"email": "abc@gmail.com", "password": "validpass"})
    assert response.status_code == 200

    response = requests.post(f"{src.config.url}/auth/passwordreset/reset/v1", json = {"reset_code": expected_reset_code, "new_password": "validpass"})
    assert response.status_code == 400

    expected_reset_code = store["users"][2]["reset_codes"][0]
    response = requests.post(f"{src.config.url}/auth/passwordreset/reset/v1", json = {"reset_code": expected_reset_code, "new_password": "validpass"})
    assert response.status_code == 200

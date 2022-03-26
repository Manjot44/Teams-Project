import pytest
from src.auth import auth_register_v1
from src.error import InputError, AccessError
from src.other import clear_v1
from src.data_store import data_store
import src.admin
import requests

BASE_ADDRESS = 'http://127.0.0.1'
BASE_PORT = 8080
BASE_URL = f"{BASE_ADDRESS}:{BASE_PORT}"

# Test if user has been promoted to a global owner
def test_promote():
    clear_v1()
    auth_user1 = auth_register_v1("Iqtidar@gmail.com", "amazingpassword1", "Iqtidar", "Rahman")
    auth_user2 = auth_register_v1("Manjot@gmail.com", "amazingpassword2", "Manjot", "Singh")

    id2 = auth_user2["auth_user_id"]
    token1 = auth_user1["token"]

    src.admin.admin_userpermission_change(token1, id2, 1)

    store = data_store.get()
    assert store['users'][id2]['perm_id'] == 1
        
# Test Invalid Token 
def test_invalid_token():
    clear_v1()
    auth_user2 = auth_register_v1("Manjot@gmail.com", "amazingpassword2", "Manjot", "Singh")["auth_user_id"]

    with pytest.raises(AccessError):
        src.admin.admin_userpermission_change("invalid token", auth_user2, 1)

# Test Invalid permission id - 3 is invalid 
def test_invalid_permission_id():
    clear_v1()
    auth_user1 = auth_register_v1("Iqtidar@gmail.com", "amazingpassword1", "Iqtidar", "Rahman")["auth_user_id"]
    auth_user2 = auth_register_v1("Manjot@gmail.com", "amazingpassword2", "Manjot", "Singh")["auth_user_id"]

    store = data_store.get()
    token1 = store['users'][auth_user1]['valid_tokens'][0]

    with pytest.raises(InputError):
        src.admin.admin_userpermission_change(token1, auth_user2, 3)

# Global owner is the only one and tries to get demoted to a user
def test_only_global_owner():
    clear_v1()
    auth_user1 = auth_register_v1("Iqtidar@gmail.com", "amazingpassword1", "Iqtidar", "Rahman")["auth_user_id"]

    store = data_store.get()
    token1 = store['users'][auth_user1]['valid_tokens'][0]

    with pytest.raises(InputError):
        src.admin.admin_userpermission_change(token1, auth_user1, 2)

# User being promoted to a global owner is already a global owner
def test_already_global_owner():
    clear_v1()
    auth_user1 = auth_register_v1("Iqtidar@gmail.com", "amazingpassword1", "Iqtidar", "Rahman")["auth_user_id"]
    auth_user2 = auth_register_v1("Manjot@gmail.com", "amazingpassword2", "Manjot", "Singh")["auth_user_id"]

    store = data_store.get()
    token1 = store['users'][auth_user1]['valid_tokens'][0]

    src.admin.admin_userpermission_change(token1, auth_user2, 1)

    with pytest.raises(InputError):
        src.admin.admin_userpermission_change(token1, auth_user2, 1)

# User being demoted to a regular user is already a regular user 
def test_already_user():
    clear_v1()
    auth_user1 = auth_register_v1("Iqtidar@gmail.com", "amazingpassword1", "Iqtidar", "Rahman")["auth_user_id"]
    auth_user2 = auth_register_v1("Manjot@gmail.com", "amazingpassword2", "Manjot", "Singh")["auth_user_id"]

    store = data_store.get()
    token1 = store['users'][auth_user1]['valid_tokens'][0]

    with pytest.raises(InputError):
        src.admin.admin_userpermission_change(token1, auth_user2, 2)

# auth_user is not a global owner
def test_auth_not_global_owner():
    clear_v1()
    auth_user1 = auth_register_v1("Iqtidar@gmail.com", "amazingpassword1", "Iqtidar", "Rahman")["auth_user_id"]
    auth_user2 = auth_register_v1("Manjot@gmail.com", "amazingpassword2", "Manjot", "Singh")["auth_user_id"]

    store = data_store.get()
    token2 = store['users'][auth_user2]['valid_tokens'][0]

    with pytest.raises(AccessError):
        src.admin.admin_userpermission_change(token2, auth_user1, 2)

# Assume that u_id is an invalid ID
def test_invalid_id():
    clear_v1()
    auth_user1 = auth_register_v1("Iqtidar@gmail.com", "amazingpassword1", "Iqtidar", "Rahman")["auth_user_id"]
    auth_user2 = auth_register_v1("Manjot@gmail.com", "amazingpassword2", "Manjot", "Singh")["auth_user_id"]

    store = data_store.get()
    token1 = store['users'][auth_user1]['valid_tokens'][0]

    with pytest.raises(AccessError):
        src.admin.admin_userpermission_change(token1, auth_user2 + 1, 1)

'''
HTTP Wrapper Tests

'''
# Test if user has been promoted to a global owner
def test_promote_http(register_three_users):
    token1 = register_three_users["token"][0]
    id2 = register_three_users["id"][1]

    response = requests.post(f"{BASE_URL}/admin/userpermission/change/v1", json = {"token" : token1, "u_id" : id2, "permission_id" : 1})
    assert response.status_code == 200

# Test Invalid Token 
def test_invalid_token_http(register_three_users):
    id2 = register_three_users["id"][1]

    response = requests.post(f"{BASE_URL}/admin/userpermission/change/v1", json = {"token" : 'incorrect token', "u_id" : id2, "permission_id" : 1})
    assert response.status_code == 403

# Test Invalid permission id - 3 is invalid 
def test_invalid_permission_id_http(register_three_users):
    token1 = register_three_users["token"][0]
    id2 = register_three_users["id"][1]

    response = requests.post(f"{BASE_URL}/admin/userpermission/change/v1", json = {"token" : token1, "u_id" : id2, "permission_id" : 3})
    assert response.status_code == 400

# Global owner is the only one and tries to get demoted to a user
def test_only_global_owner_http(register_three_users):
    token1 = register_three_users["token"][0]
    id1 = register_three_users["id"][0]

    response = requests.post(f"{BASE_URL}/admin/userpermission/change/v1", json = {"token" : token1, "u_id" : id1, "permission_id" : 2})
    assert response.status_code == 400

# User being promoted to a global owner is already a global owner
def test_already_global_owner_http(register_three_users):
    token1 = register_three_users["token"][0]
    id2 = register_three_users["id"][1]

    response = requests.post(f"{BASE_URL}/admin/userpermission/change/v1", json = {"token" : token1, "u_id" : id2, "permission_id" : 1})
    assert response.status_code == 200
    response = requests.post(f"{BASE_URL}/admin/userpermission/change/v1", json = {"token" : token1, "u_id" : id2, "permission_id" : 1})
    assert response.status_code == 400

# User being demoted to a regular user is already a regular user 
def test_already_user_http(register_three_users):
    token1 = register_three_users["token"][0]
    id2 = register_three_users["id"][1]

    response = requests.post(f"{BASE_URL}/admin/userpermission/change/v1", json = {"token" : token1, "u_id" : id2, "permission_id" : 2})
    assert response.status_code == 400

# auth_user is not a global owner
def test_auth_not_global_owner_http(register_three_users):
    token2 = register_three_users["token"][1]
    id1 = register_three_users["id"][0]

    response = requests.post(f"{BASE_URL}/admin/userpermission/change/v1", json = {"token" : token2, "u_id" : id1, "permission_id" : 2})
    assert response.status_code == 403

# Assume that u_id is an invalid ID
def test_invalid_id_http(register_three_users):
    token1 = register_three_users["token"][0]
    id2 = register_three_users["id"][1]

    response = requests.post(f"{BASE_URL}/admin/userpermission/change/v1", json = {"token" : token1, "u_id" : id2 + 5, "permission_id" : 1})
    assert response.status_code == 403
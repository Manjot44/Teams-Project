import pytest
from src.auth import auth_register_v1
from src.error import InputError, AccessError
from src.other import clear_v1
from src.data_store import data_store
import src.admin
import requests
from src.config import url

'''
HTTP Wrapper Tests

'''
# Test if user has been promoted to a global owner
def test_promote_http(register_three_users):
    token1 = register_three_users["token"][0]
    id2 = register_three_users["id"][1]

    response = requests.post(f"{url}/admin/userpermission/change/v1", json = {"token" : token1, "u_id" : id2, "permission_id" : 1})
    assert response.status_code == 200

# Test Invalid Token 
def test_invalid_token_http(register_three_users):
    id2 = register_three_users["id"][1]

    response = requests.post(f"{url}/admin/userpermission/change/v1", json = {"token" : 'incorrect token', "u_id" : id2, "permission_id" : 1})
    assert response.status_code == 403

# Test Invalid permission id - 3 is invalid 
def test_invalid_permission_id_http(register_three_users):
    token1 = register_three_users["token"][0]
    id2 = register_three_users["id"][1]

    response = requests.post(f"{url}/admin/userpermission/change/v1", json = {"token" : token1, "u_id" : id2, "permission_id" : 3})
    assert response.status_code == 400

# Global owner is the only one and tries to get demoted to a user
def test_only_global_owner_http(register_three_users):
    token1 = register_three_users["token"][0]
    id1 = register_three_users["id"][0]

    response = requests.post(f"{url}/admin/userpermission/change/v1", json = {"token" : token1, "u_id" : id1, "permission_id" : 2})
    assert response.status_code == 400

# User being promoted to a global owner is already a global owner
def test_already_global_owner_http(register_three_users):
    token1 = register_three_users["token"][0]
    id2 = register_three_users["id"][1]

    response = requests.post(f"{url}/admin/userpermission/change/v1", json = {"token" : token1, "u_id" : id2, "permission_id" : 1})
    assert response.status_code == 200
    response = requests.post(f"{url}/admin/userpermission/change/v1", json = {"token" : token1, "u_id" : id2, "permission_id" : 1})
    assert response.status_code == 400

# User being demoted to a regular user is already a regular user 
def test_already_user_http(register_three_users):
    token1 = register_three_users["token"][0]
    id2 = register_three_users["id"][1]

    response = requests.post(f"{url}/admin/userpermission/change/v1", json = {"token" : token1, "u_id" : id2, "permission_id" : 2})
    assert response.status_code == 400

# auth_user is not a global owner
def test_auth_not_global_owner_http(register_three_users):
    token2 = register_three_users["token"][1]
    id1 = register_three_users["id"][0]

    response = requests.post(f"{url}/admin/userpermission/change/v1", json = {"token" : token2, "u_id" : id1, "permission_id" : 2})
    assert response.status_code == 403

# Assume that u_id is an invalid ID
def test_invalid_id_http(register_three_users):
    token1 = register_three_users["token"][0]
    id2 = register_three_users["id"][1]

    response = requests.post(f"{url}/admin/userpermission/change/v1", json = {"token" : token1, "u_id" : id2 + 5, "permission_id" : 1})
    assert response.status_code == 400

# demoting an owner to a member
def test_demote(register_three_users):
    response = requests.post(f"{url}/admin/userpermission/change/v1", json = {"token" : register_three_users["token"][0], "u_id" : register_three_users["id"][1], "permission_id" : 1})
    assert response.status_code == 200
    response = requests.post(f"{url}/admin/userpermission/change/v1", json = {"token" : register_three_users["token"][1], "u_id" : register_three_users["id"][0], "permission_id" : 2})
    assert response.status_code == 200
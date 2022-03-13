import src.auth
import pytest
from src.other import clear_v1
from src.error import InputError

def test_authlog_valid(register_three_users):
    assert src.auth.auth_login_v1("aBc123._%+-@aBc123.-.Co", "123456")['auth_user_id'] == register_three_users[0]
    assert src.auth.auth_login_v1(".@..Ml", "a>?:1#")['auth_user_id'] == register_three_users[1]

def test_incorrect_details(register_three_users):
    with pytest.raises(InputError):
        src.auth.auth_login_v1("aBc12._%+-@aBc123.-.Co", "123456")                      
    with pytest.raises(InputError):
        src.auth.auth_login_v1("aBc123._%+-@aBc123.-.Co", "1234576")                   

def test_empty(register_three_users):
    with pytest.raises(InputError):
        src.auth.auth_login_v1("", "123456")                                       
    with pytest.raises(InputError):
        src.auth.auth_login_v1("aBc123._%+-@aBc123.-.Co", "")                           

def test_mixed_password(register_three_users):
    with pytest.raises(InputError):
        src.auth.auth_login_v1("aBc123._%+-@aBc123.-.Co", "a>?:1#")                     
    with pytest.raises(InputError):
        src.auth.auth_login_v1(".@..Ml", "123456")                                      

def test_no_registered_user():
    clear_v1()
    with pytest.raises(InputError):
        src.auth.auth_login_v1("anything@gmail.com", "password1$^")  
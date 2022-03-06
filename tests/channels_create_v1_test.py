import pytest
from src.channels import channels_create_v1
from src.error import AccessError, InputError
from src.other import clear_v1
from src.auth import auth_register_v1

#Testing for valid user ID
def test_valid_user():
    clear_v1()
    #No user has been added to the user list, so this should be an error
    with pytest.raises(AccessError):
        channels_create_v1("userone", "new_channel1", True)["channel_id"]
    #Even though a user has been added, since the user_id input is different it should be an error
    user_id = auth_register_v1("aBc123._%+-@aBc123.-.Co", "123456", "A", "A")["auth_user_id"]
    with pytest.raises(AccessError):
        channels_create_v1("userone", "new_channel1", True)["channel_id"]

#Testing for correct channel_id if one channel is created
def test_normal_single():
    clear_v1()
    user_id = auth_register_v1("aBc123._%+-@aBc123.-.Co", "123456", "A", "A")["auth_user_id"]
    assert channels_create_v1(user_id, "new_channel", True)["channel_id"] == 1

#Testing for correct channel_id if multiple channels are created
def test_normal_multiple():
    clear_v1()
    user_id = auth_register_v1("aBc123._%+-@aBc123.-.Co", "123456", "A", "A")["auth_user_id"]
    assert channels_create_v1(user_id, "new_channel1", True)["channel_id"] == 1
    assert channels_create_v1(user_id, "new_channel2", False)["channel_id"] == 2
    assert channels_create_v1(user_id, "new_channel3", True)["channel_id"] == 3

#Tests border cases for the exception
def test_border():
    clear_v1()
    user_id = auth_register_v1("aBc123._%+-@aBc123.-.Co", "123456", "A", "A")["auth_user_id"]
    assert channels_create_v1(user_id, "a", True)["channel_id"] == 1
    assert channels_create_v1(user_id, "abcdefghijklmnopqrst", True)["channel_id"] == 2

#Tests for exception
def test_edge():
    clear_v1()
    user_id = auth_register_v1("aBc123._%+-@aBc123.-.Co", "123456", "A", "A")["auth_user_id"]
    with pytest.raises(InputError):
        channels_create_v1(user_id, "", True)["channel_id"]
        channels_create_v1(user_id, "abcdefghijklmnopqrst0", True)["channel_id"]
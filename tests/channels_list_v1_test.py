from src.channels import channels_list_v1, channels_create_v1
from src.other import clear_v1
from src.error import AccessError
from src.auth import auth_register_v1
import pytest

#Testing for valid user ID
def test_valid_user():
    clear_v1()
    #Even though a user has been added, since the user_id input is different it should be an error
    user_id = auth_register_v1("aBc123._%+-@aBc123.-.Co", "123456", "A", "A")
    channels_create_v1(user_id, "new_channel1", True)
    with pytest.raises(AccessError):
        channels_list_v1(user_id + 1)

#Testing that name and channel_id are correct for one channel 
def test1obj():
    clear_v1()
    user_id = auth_register_v1("aBc123._%+-@aBc123.-.Co", "123456", "A", "A")["auth_user_id"]
    channels_create_v1(user_id, "channel1", True)
    assert channels_list_v1(user_id)["channels"][0]["channel_id"] == 1
    assert channels_list_v1(user_id)["channels"][0]["name"] == 'channel1'

#Testing for name and channel_id are correct for two channels 
def test2obj():
    clear_v1()
    user_id = auth_register_v1("aBc123._%+-@aBc123.-.Co", "123456", "A", "A")["auth_user_id"]
    channels_create_v1(user_id, "channel1", True)
    channels_create_v1(user_id, "channel2", True)
    assert channels_list_v1(user_id)["channels"][0]["channel_id"] == 1
    assert channels_list_v1(user_id)["channels"][0]["name"] == 'channel1'
    assert channels_list_v1(user_id)["channels"][1]["channel_id"] == 2
    assert channels_list_v1(user_id)["channels"][1]["name"] == 'channel2'
    
#Testing to show only channels the user is part of show up
def testuserchannels():
    clear_v1()
    user_id1 = auth_register_v1("aBc123._%+-@aBc123.-.Co", "123456", "A", "A")["auth_user_id"]
    user_id2 = auth_register_v1("abc@gmail.com", "thisIsPass13./", "Jerry", "Lin")["auth_user_id"]
    channels_create_v1(user_id1, "channel1", True)
    channels_create_v1(user_id2, "channel2", True)
    channels_create_v1(user_id1, "channel3", True)
    assert channels_list_v1(user_id1)["channels"][0]["channel_id"] == 1
    assert channels_list_v1(user_id1)["channels"][0]["name"] == 'channel1'
    assert channels_list_v1(user_id1)["channels"][1]["channel_id"] == 3
    assert channels_list_v1(user_id1)["channels"][1]["name"] == 'channel3'
    assert channels_list_v1(user_id2)["channels"][0]["channel_id"] == 2
    assert channels_list_v1(user_id2)["channels"][0]["name"] == 'channel2'

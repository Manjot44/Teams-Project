import pytest
from src.auth import auth_register_v1
from src.channel import channel_details_v1, channel_join_v1
from src.channels import channels_create_v1
from src.error import InputError, AccessError
from src.other import clear_v1

# Test that the person being added is successfully added 
def test_if_person_is_added():
    clear_v1()
    auth_user1 = auth_register_v1("Iqtidar@gmail.com", "amazingpassword1", "Iqtidar", "Rahman")["auth_user_id"]
    auth_user2 = auth_register_v1("Manjot@gmail.com", "amazingpassword2", "Manjot", "Singh")["auth_user_id"]
    channel1 = channels_create_v1(auth_user1, "channel1", True)["channel_id"]
    channel_join_v1(auth_user2, channel1)
    
    details = channel_details_v1(auth_user2, channel1)

    user_joined = False 

    for user in details["all_members"]:
        if user["u_id"] == auth_user2:
            user_joined = True
            break

    assert user_joined == True

# Test to make sure that when a user joins once, if they try joining they wont join again, where user is not owner
def test_add_twice():
    clear_v1()
    auth_user1 = auth_register_v1("Iqtidar@gmail.com", "amazingpassword1", "Iqtidar", "Rahman")["auth_user_id"]
    auth_user2 = auth_register_v1("Manjot@gmail.com", "amazingpassword2", "Manjot", "Singh")["auth_user_id"]

    channel1 = channels_create_v1(auth_user1, "channel1", True)["channel_id"]
    channel_join_v1(auth_user2, channel1)
    with pytest.raises(InputError):
        channel_join_v1(auth_user2, channel1) 

# Test to make sure that when a user joins once, if they try joining they wont join again, where user is the owner
def test_add_twice2():    
    clear_v1()
    auth_user2 = auth_register_v1("Manjot@gmail.com", "amazingpassword2", "Manjot", "Singh")["auth_user_id"]
    channel1 = channels_create_v1(auth_user2, "channel1", True)["channel_id"]
    
    with pytest.raises(InputError):
        channel_join_v1(auth_user2, channel1) 
    
# If the channel is private, the user trying to join shouldn't be able to join it 
def test_channel_private():
    clear_v1()
    auth_user1 = auth_register_v1("Iqtidar@gmail.com", "amazingpassword1", "Iqtidar", "Rahman")["auth_user_id"]
    auth_user2 = auth_register_v1("Manjot@gmail.com", "amazingpassword2", "Manjot", "Singh")["auth_user_id"]

    channel1 = channels_create_v1(auth_user1, "channel1", False)["channel_id"]
    with pytest.raises(AccessError):
        channel_join_v1(auth_user2, channel1) 

# user tries to join invalid channel
def test_invld_chnnl():
    clear_v1()
    auth_user1 = auth_register_v1("Iqtidar@gmail.com", "amazingpassword1", "Iqtidar", "Rahman")["auth_user_id"]
    auth_user2 = auth_register_v1("Manjot@gmail.com", "amazingpassword2", "Manjot", "Singh")["auth_user_id"]
    channel1 = channels_create_v1(auth_user1, "channel1", True)["channel_id"]
    with pytest.raises(InputError):
        channel_join_v1(auth_user2, channel1 + 1)

# invalid user tries to join channel
def test_invalid_user():    
    clear_v1()
    auth_user1 = auth_register_v1("Iqtidar@gmail.com", "amazingpassword1", "Iqtidar", "Rahman")["auth_user_id"]
    channel1 = channels_create_v1(auth_user1, "channel1", True)["channel_id"]
    with pytest.raises(AccessError):
        channel_join_v1(auth_user1 + 1, channel1)

import pytest
from src.auth import auth_register_v1
from src.channel import channel_details_v1, channel_join_v1, channel_invite_v1
from src.channels import channels_create_v1
from src.error import InputError, AccessError
from src.other import clear_v1

# test if valid user is added to the channel after being invited - Public Channel
def test_valid_user1():
    clear_v1()
    auth_user1 = auth_register_v1("Iqtidar@gmail.com", "amazingpassword1", "Iqtidar", "Rahman")["auth_user_id"]
    auth_user2 = auth_register_v1("Manjot@gmail.com", "amazingpassword2", "Manjot", "Singh")["auth_user_id"]

    channel1 = channels_create_v1(auth_user1, "Channel1", True)["channel_id"]
    channel_invite_v1(auth_user1, channel1, auth_user2)

    details = channel_details_v1(auth_user1, channel1)

    user_joined = False 

    for user in details["all_members"]:
        if user["u_id"] == auth_user2:
            user_joined = True
            break

    assert user_joined == True

# test if valid user is added to the channel after being invited - Private Channel
def test_valid_user_private():   
    clear_v1()
    auth_user1 = auth_register_v1("Iqtidar@gmail.com", "amazingpassword1", "Iqtidar", "Rahman")["auth_user_id"]
    auth_user2 = auth_register_v1("Manjot@gmail.com", "amazingpassword2", "Manjot", "Singh")["auth_user_id"]

    channel1 = channels_create_v1(auth_user1, "Channel1", False)["channel_id"]
    channel_invite_v1(auth_user1, channel1, auth_user2)

    details = channel_details_v1(auth_user1, channel1)

    user_joined = False 

    for user in details["all_members"]:
        if user["u_id"] == auth_user2:
            user_joined = True
            break

    assert user_joined == True

# User that is invited does not have a valid ID
def test_invalid_userid1():
    clear_v1()
    auth_user1 = auth_register_v1("Iqtidar@gmail.com", "amazingpassword1", "Iqtidar", "Rahman")["auth_user_id"]

    channel1 = channels_create_v1(auth_user1, "Channel1", True)["channel_id"]
    with pytest.raises(InputError):
        channel_invite_v1(auth_user1, channel1, auth_user1 + 1) # Should InputError here, thus not adding 'auth_user2'

# User that is inviting does not have a valid ID
def test_invalid_userid2():
    clear_v1()
    auth_user1 = auth_register_v1("Iqtidar@gmail.com", "amazingpassword1", "Iqtidar", "Rahman")["auth_user_id"]

    channel1 = channels_create_v1(auth_user1, "Channel1", False)["channel_id"]
    with pytest.raises(AccessError):
        channel_invite_v1(auth_user1 + 1, channel1, auth_user1) # Should AccessError here, thus not adding 'auth_user1'

# Test where auth_user tries to add someone to the channel who is already in the channel
def test_channel_is_member():
    clear_v1()
    auth_user1 = auth_register_v1("Iqtidar@gmail.com", "amazingpassword1", "Iqtidar", "Rahman")["auth_user_id"]
    auth_user2 = auth_register_v1("Manjot@gmail.com", "amazingpassword2", "Manjot", "Singh")["auth_user_id"]

    channel1 = channels_create_v1(auth_user1, "Channel1", True)["channel_id"]
    channel_invite_v1(auth_user1, channel1, auth_user2) # Manjot is added to the channel
    with pytest.raises(InputError):
        channel_invite_v1(auth_user1, channel1, auth_user2) # Should InputError here, thus not adding Manjot for a second time

# Owner of the chat tries to invite themselves to the chat
def test_invite_oneself():
    clear_v1()
    auth_user1 = auth_register_v1("Iqtidar@gmail.com", "amazingpassword1", "Iqtidar", "Rahman")["auth_user_id"]
    auth_register_v1("Manjot@gmail.com", "amazingpassword2", "Manjot", "Singh")["auth_user_id"]

    channel1 = channels_create_v1(auth_user1, "Channel1", True)["channel_id"]
    with pytest.raises(InputError):
        channel_invite_v1(auth_user1, channel1, auth_user1) # Owner tries to add themselves to the chat 

# auth_user_id who is trying to invite another user is not a member of the channel
def test_invalid_member():
    clear_v1()
    auth_user1 = auth_register_v1("Iqtidar@gmail.com", "amazingpassword1", "Iqtidar", "Rahman")["auth_user_id"]
    auth_user2 = auth_register_v1("Manjot@gmail.com", "amazingpassword2", "Manjot", "Singh")["auth_user_id"]
    auth_user3 = auth_register_v1("Doctorsureshkumar@gmail.com", "smartpassword1", "Ashwin", "Sureshkumar")["auth_user_id"]

    channel1 = channels_create_v1(auth_user1, "Channel1", True)["channel_id"]
    with pytest.raises(AccessError):
        channel_invite_v1(auth_user3, channel1, auth_user2) # auth_user3 who is not in channel1 tries to invite auth_user2. Should AccessError

# Test if an invalid channel_id is put in 
def test_invalid_channel_id():    
    clear_v1()
    auth_user1 = auth_register_v1("Iqtidar@gmail.com", "amazingpassword1", "Iqtidar", "Rahman")["auth_user_id"]
    auth_user2 = auth_register_v1("Manjot@gmail.com", "amazingpassword2", "Manjot", "Singh")["auth_user_id"]

    channel1 = channels_create_v1(auth_user1, "Channel1", True)["channel_id"]
    with pytest.raises(InputError):
        channel_invite_v1(auth_user1, channel1 + 1, auth_user2)

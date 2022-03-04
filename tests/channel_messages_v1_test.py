import src.channel
import src.auth
import src.channels

import pytest 

from src.other import clear_v1
from src.error import AccessError, InputError


def test_invalid_channel_id():
    clear_v1()
# channel_id does not refer to a valid channel ---> InputError
    with pytest.raises(InputError):
        channel_messages_v1(auth_user_id, "invalid_channel_id", 0)

def test_user_invalid():  
    clear_v1()
# channel_id is valid and the authorised user is not a member of the channel ---> AccessError  
    with pytest.raises(AccessError):
        channel_messages_v1("invalid_auth_user_id", channel_id, 0)

def test_valid_start_no_messages():
    clear_v1()
# start is greater than the total number of messages in the channel
    with pytest.raises(InputError): 
        channel_messages_v1(auth_user_id, channel_id, 10)       

def test_valid_start():
    clear_v1()
# tests if start is less than the total number of messages
    assert channel_messages_v1(auth_user_id, channel_id, 0)

def test_valid_return_no_messages():
    clear_v1()
# to ensure that function returns -1 in "end"
    vaid_end_return = False
    
    if end < -1 or end > -1:
        valid_end_return = True
    
    assert valid_end_return


def test_valid_no_messages():
    clear_v1()
# tests that start value and end value is correct

    user1 = auth_register_v1("simon@simon.com", "wefweweqfqwefqef", "simon", "simon2")
    u_id = user1["auth_user_id"]

    channel1 = channels_create_v1(u_id, "foo", True)
    ch_id = channel1["channel_id"]

    ch_messages = channel_messages_v1(u_id, ch_id, 0)

    assert ch_messages["messages"] == []
    assert ch_messages["end"] == -1   






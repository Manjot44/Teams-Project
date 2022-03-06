from src.channel import channel_messages_v1
from src.auth import auth_register_v1
from src.channels import channels_create_v1

import pytest 

from src.other import clear_v1
from src.error import AccessError, InputError


def test_invalid_channel_id():
    clear_v1()
# channel_id does not refer to a valid channel ---> InputError

    user1 = auth_register_v1("simon@simon.com", "wefweweqfqwefqef", "simon", "simon2")['auth_user_id']
    channel1 = channels_create_v1(user1, "foo", True)["channel_id"]

    with pytest.raises(InputError):
        channel_messages_v1(user1, channel1 + 1, 0)

def test_user_invalid():  
    clear_v1()
    
    user1 = auth_register_v1("simon@simon.com", "wefweweqfqwefqef", "simon", "simon2")['auth_user_id']
    user2 = auth_register_v1("jerrylin@jerry.com", "wefweweqfqwefqef", "simon", "simon2")['auth_user_id']
    channel1 = channels_create_v1(user1, "foo", True)['channel_id']

# channel_id is valid and the authorised user is not a member of the channel ---> AccessError  
    with pytest.raises(AccessError):
        channel_messages_v1(user2, channel1, 0)

def test_valid_start_no_messages():
    clear_v1()
    # raises error if start is greater than the total number of messages in the channel
    
    user1 = auth_register_v1("simon@simon.com", "wefweweqfqwefqef", "simon", "simon2")['auth_user_id']
    channel1 = channels_create_v1(user1, "foo", True)['channel_id']

    with pytest.raises(InputError): 
        channel_messages_v1(user1, channel1, 10)       

def test_valid_start():
    clear_v1()
    # tests if return outputs (messages, start, end) are valid

    user1 = auth_register_v1("simon@simon.com", "wefweweqfqwefqef", "simon", "simon2")['auth_user_id']
    channel1 = channels_create_v1(user1, "foo", True)['channel_id']

    messagesreturn = {
        'messages': [],
        'start': 0, 
        'end': -1
    }   
   
    assert channel_messages_v1(user1, channel1, 0) == messagesreturn

def test_user_registered():  
    clear_v1()
    # authorised user is not a member of the channel ---> AccessError  

    user1 = auth_register_v1("simon@simon.com", "wefweweqfqwefqef", "simon", "simon2")['auth_user_id']
    channel1 = channels_create_v1(user1, "foo", True)['channel_id']

    with pytest.raises(AccessError):
        channel_messages_v1(user1 + 1, channel1, 0)



import src.channel
import src.auth
import src.channels

import pytest 

from src.other import clear_v1()
from src.error import AccessError, InputError


def test_invalid_channel_id:
# channel_id does not refer to a valid channel ---> InputError
    with pytest.raises(InputError)
        channel_messages_v1(auth_user_id, None, 0)

def test_user_invalid:  
# channel_id is valid and the authorised user is not a member of the channel ---> AccessError  
    with pytest.raises(AccessError)
        channel_messages_v1(None, channel_id, 0)

def test_invalid_start:
# start is greater than the total number of messages in the channel
    with pytest.raises(InputError) 
        assert start < 0       

def test_invalid_return:
# to ensure that function returns -1 in "end"
    assert end != -1
                

import pytest

from src import auth, channel, channels, error, other

def test_listall_one_public_channel():
    other.clear_v1()
    user_id = auth.auth_register_v1('sanjamsingh@gmail.com', 'password', 'sanjam', 'singh')
    channel_id = channels.channels_create_v1(user_id, 'sanjam_channel', True)
    channel_list = channels.channels_listall_v1(user_id)

    assert channel_list['channels']['channel_id'] == channel_id
    assert channel_list['channels']['name'] == 'sanjam_channel'

def test_listall_two_public_channel():
    other.clear_v1()
    user_id = auth.auth_register_v1('sanjamsingh@gmail.com', 'password', 'sanjam', 'singh')
    channel_id1 = channels.channels_create_v1(user_id, 'sanjam_channel1', True)
    channel_id2 = channels.channels_create_v1(user_id, 'sanjam_channel2', True)
    channel_list = channels.channels_listall_v1(user_id)

    for ch in channel_list['channels']:
        assert ch['channel_id'] == channel_id & ch['name'] == 'sanjam_channel'


'''
What to test:
Listing no channels
Listing 1 public channel
Listing 3 public channels
Listing 1 private channel
Listing 2 private channels
Listing a mixture of public and private channels
Listing with invalid id??

Other:
Use a fixture; for clear_v1(), auth.auth_register (?)
'''
import pytest
from src import auth, channel, channels, error, other
# from src.auth import auth_register_v1
# from src.channel import channel_details_v1
# from src.channels import channels_create_v1
# from src.other import clear_v1

def test_details_invalid_auth_user_id():
    other.clear_v1()
    valid_user_id = auth.auth_register_v1('sanjamsingh@gmail.com', 'password', 'sanjam', 'singh')['auth_user_id']
    invalid_user_id = None
    valid_channel_id = channels.channels_create_v1(valid_user_id, 'sanjam_channel', True)['channel_id']
    with pytest.raises(error.AccessError):
        # tests for invalid user id for a channel id
        channel.channel_details_v1(invalid_user_id, valid_channel_id)

def test_details_invalid_channel_id():
    other.clear_v1()
    user_id = auth.auth_register_v1('sanjamsingh@gmail.com', 'password', 'sanjam', 'singh')['auth_user_id']
    with pytest.raises(error.InputError):
        channel.channel_details_v1(user_id, None)                                          # channel id is non existant

def test_details_invalid_channel_access():
    other.clear_v1()
    user_id1 = auth.auth_register_v1('sanjamsingh@gmail.com', 'password', 'sanjam', 'singh')['auth_user_id']        # user id 1
    user_id2 = auth.auth_register_v1('jerrylin@gmail.com', 'password', 'jerry', 'lin')['auth_user_id']             # user id 2
    channels.channels_create_v1(user_id1, 'sanjam_channel', True)['channel_id']                     # create channel 1
    channel_id2 = channels.channels_create_v1(user_id2, 'jerry_channel', True)['channel_id']                      # create channel 2
    with pytest.raises(error.AccessError):                                                                # details(user 1, channel 2)
        channel.channel_details_v1(user_id1, channel_id2)                                   # raise access error 

def test_details_user_of_created_channel():
    other.clear_v1()
    user_id = auth.auth_register_v1('sanjamsingh@gmail.com', 'password', 'sanjam', 'singh')['auth_user_id']
    handle = 'sanjamsingh'
    channel_id = channels.channels_create_v1(user_id, 'sanjam_channel', True)['channel_id']
    details = channel.channel_details_v1(user_id, channel_id)
    assert details['name'] == 'sanjam_channel'

    assert details['is_public'] == True

    for members in details['owner_members']:
        assert members['u_id'] == user_id
        assert members['email'] == 'sanjamsingh@gmail.com'
        assert members['name_first'] == 'sanjam'
        assert members['name_last'] == 'singh'
        assert members['handle_str'] == handle

    for members in details['all_members']:
        assert members['u_id'] == user_id
        assert members['email'] == 'sanjamsingh@gmail.com'
        assert members['name_first'] == 'sanjam'
        assert members['name_last'] == 'singh'
        assert members['handle_str'] == handle


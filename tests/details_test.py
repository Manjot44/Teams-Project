import pytest
from src import auth, channel, channels, error, other

def test_details_invalid_auth_user_id():
    other.clear_v1()
    valid_token = auth.auth_register_v1('sanjamsingh@gmail.com', 'password', 'sanjam', 'singh')['token']
    invalid_token = None
    valid_channel_id = channels.channels_create_v1(valid_token, 'sanjam_channel', True)['channel_id']
    with pytest.raises(error.AccessError):
        channel.channel_details_v1(invalid_token, valid_channel_id)

def test_details_invalid_channel_id():
    other.clear_v1()
    token = auth.auth_register_v1('sanjamsingh@gmail.com', 'password', 'sanjam', 'singh')['token']
    with pytest.raises(error.InputError):
        channel.channel_details_v1(token, None)                                          

def test_details_invalid_channel_access():
    other.clear_v1()
    token1 = auth.auth_register_v1('sanjamsingh@gmail.com', 'password', 'sanjam', 'singh')['token']
    token2 = auth.auth_register_v1('jerrylin@gmail.com', 'password', 'jerry', 'lin')['token']      
    channels.channels_create_v1(token1, 'sanjam_channel', True)['channel_id']                     
    channel_id2 = channels.channels_create_v1(token2, 'jerry_channel', True)['channel_id']                      
    with pytest.raises(error.AccessError):                                                                
        channel.channel_details_v1(token1, channel_id2)                                    

def test_details_user_of_created_channel():
    other.clear_v1()
    user = auth.auth_register_v1('sanjamsingh@gmail.com', 'password', 'sanjam', 'singh')
    token = user['token']
    user_id = user['auth_user_id']
    handle = 'sanjamsingh'
    channel_id = channels.channels_create_v1(token, 'sanjam_channel', True)['channel_id']
    details = channel.channel_details_v1(token, channel_id)
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


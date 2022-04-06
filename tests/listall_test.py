from lib2to3.pgen2 import token
import pytest

from src import auth, channel, channels, error, data_store, other

def test_listall_invalid_token():
    other.clear_v1()
    token = None
    with pytest.raises(error.AccessError):
        channels.channels_listall_v1(token)                    
    

def test_listall_one_public_channel():
    other.clear_v1()
    token = auth.auth_register_v1('sanjamsingh@gmail.com', 'password', 'sanjam', 'singh')['token']
    channel_id = channels.channels_create_v1(token, 'sanjam_channel', True)['channel_id']
    channel_list = channels.channels_listall_v1(token)

    assert channel_list['channels'][0]['channel_id'] == channel_id     
    assert channel_list['channels'][0]['name'] == 'sanjam_channel'      

def test_listall_two_public_channel():
    other.clear_v1()
    token = auth.auth_register_v1('sanjamsingh@gmail.com', 'password', 'sanjam', 'singh')['token']
    channel_id1 = channels.channels_create_v1(token, 'sanjam_channel1', True)['channel_id']
    channel_id2 = channels.channels_create_v1(token, 'sanjam_channel2', True)['channel_id']
    list_channel_ids = [channel_id1, channel_id2]
    list_channel_names = ['sanjam_channel1', 'sanjam_channel2']
    listall_return_list = channels.channels_listall_v1(token)
    
    for ch, ids, names in zip(listall_return_list['channels'], list_channel_ids, list_channel_names):
        assert ch['channel_id'] == ids
        assert ch['name'] == names


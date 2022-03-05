import pytest

from src import auth, channel, channels, error, data_store, other

def test_listall_invalid_user_id():
    other.clear_v1()
    user_id = None
    with pytest.raises(error.AccessError):
        assert channel.channels_listall_v1(user_id)                     # tests listall function against invalid user_id
    

def test_listall_one_public_channel():
    other.clear_v1()
    user_id = auth.auth_register_v1('sanjamsingh@gmail.com', 'password', 'sanjam', 'singh')
    channel_id = channels.channels_create_v1(user_id, 'sanjam_channel', True)
    channel_list = channels.channels_listall_v1(user_id)

    assert channel_list['channels'][0]['channel_id'] == channel_id      # tests if channel id for first channel is returned
    assert channel_list['channels'][0]['name'] == 'sanjam_channel'      # tests if first channel name is returned

def test_listall_two_public_channel():
    other.clear_v1()
    user_id = auth.auth_register_v1('sanjamsingh@gmail.com', 'password', 'sanjam', 'singh')
    channel_id1 = channels.channels_create_v1(user_id, 'sanjam_channel1', True)
    channel_id2 = channels.channels_create_v1(user_id, 'sanjam_channel2', True)
    list_channel_ids = [channel_id1, channel_id2]
    list_channel_names = ['sanjam_channel1', 'sanjam_channel2']
    listall_return_list = channels.channels_listall_v1(user_id)
    
    for ch, ids, names in zip(listall_return_list['channels'], list_channel_ids, list_channel_names):
        assert ch['channel_id'] == ids
        assert ch['name'] == names


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
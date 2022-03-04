from src.channels import channels_list_v1
from src.channels import channels_create_v1
from src.other import clear_v1

#Testing for one channel 
def test1obj():
    clear_v1()
    channels_create_v1("userone", "channel1", True)
    assert channels_list_v1("userone") == [{'channel_id': 1, 'members': ['userone'], 'name': 'channel1', 'ispublic': True}]

#Testing for two channels 
def test2obj():
    clear_v1()
    channels_create_v1("userone", "channel1", True)
    channels_create_v1("userone", "channel2", True)
    assert channels_list_v1("userone") == [{'channel_id': 1, 'members': ['userone'], 'name': 'channel1', 'ispublic': True}, {'channel_id': 2, 'members': ['userone'], 'name': 'channel2', 'ispublic': True}]


#Testing to show only channels the user is part of show up
def testuserchannels():
    clear_v1()
    channels_create_v1("userone", "channel1", True)
    channels_create_v1("usertwo", "channel2", True)
    channels_create_v1("userone", "channel3", True)
    assert channels_list_v1("userone") == [{'channel_id': 1, 'members': ['userone'], 'name': 'channel1', 'ispublic': True}, {'channel_id': 3, 'members': ['userone'], 'name': 'channel3', 'ispublic': True}]
    assert channels_list_v1("usertwo") == [{'channel_id': 2, 'members': ['usertwo'], 'name': 'channel2', 'ispublic': True}]
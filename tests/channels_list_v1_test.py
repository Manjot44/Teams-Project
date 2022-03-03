import pytest
import sys
from src.channels import channels_list_v1
from src.channels import channels_create_v1

#Testing for one channel 
def test1obj():
    channels_create_v1("userone", "channel1", True)
    assert channels_list_v1("userone") =="{'channels': [{'channel_id': 1, 'members': ['userone'], 'name': 'channel1', 'ispublic': True}]}"

#Testing for two channels 
    channels_create_v1("userone", "channel2", True)
    assert channels_list_v1("userone") =="{'channels': [{'channel_id': 1, 'members': ['userone'], 'name': 'channel1', 'ispublic': True}, {'channel_id': 2, 'members': ['userone'], 'name': 'channel2', 'ispublic': True}]}"


#Testing to show only channels the user is part of show up
    channels_create_v1("usertwo", "channel3", True)
    assert channels_list_v1("userone") == "{'channels': [{'channel_id': 1, 'members': ['userone'], 'name': 'channel1', 'ispublic': True}, {'channel_id': 2, 'members': ['userone'], 'name': 'channel2', 'ispublic': True}]}"
    assert channels_list_v1("usertwo") == "{'channels': [{'channel_id': 3, 'members': ['usertwo'], 'name': 'channel3', 'ispublic': True}]}"
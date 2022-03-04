'''
import pytest
from src.channels import channels_create_v1
from src.error import InputError
from src.other import clear_v1

#Testing for correct channel_id if one channel is created
def test_normal_single():
    clear_v1()
    assert channels_create_v1(1234567, "new_channel", True) == 1

#Testing for correct channel_id if multiple channels are created
def test_normal_multiple():
    clear_v1()
    assert channels_create_v1(1234567, "new_channel1", True) == 1
    assert channels_create_v1(1234567, "new_channel2", True) == 2
    assert channels_create_v1(1234567, "new_channel3", True) == 3

#Tests border cases for the exception
def test_border():
    clear_v1()
    assert channels_create_v1(1234567, "a", True) == 1
    assert channels_create_v1(1234567, "abcdefghijklmnopqrst", True) == 2

#Tests for exception
def test_edge():
    with pytest.raises(InputError):
        channels_create_v1(1234567, "", True)
        channels_create_v1(1234567, "abcdefghijklmnopqrst0", True)
'''
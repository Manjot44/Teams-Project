import sys
import pytest
from channels import channels_create_v1
from error import InputError

def test_normal():
    assert type(channels_create_v1(1234567, "new_channel", True)["channel_id"]) == int

def test_border():
    assert type(channels_create_v1(1234567, "a", True)["channel_id"]) == int
    assert type(channels_create_v1(1234567, "abcdefghijklmnopqrstuvwxyz", True)["channel_id"]) == int

def test_edge():
    with pytest.raises(InputError):
        channels_create_v1(1234567, "", True)["channel_id"]
        channels_create_v1(1234567, "abcdefghijklmnopqrstuvwxyz0", True)["channel_id"]
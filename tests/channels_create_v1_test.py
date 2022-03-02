import pytest
import sys
from src.channels import channels_create_v1
from src.error import InputError

def test_normal():
    assert type(channels_create_v1(1234567, "new_channel", True)["channel_id"]) == int

def test_border():
    assert type(channels_create_v1(1234567, "a", True)["channel_id"]) == int
    assert type(channels_create_v1(1234567, "abcdefghijklmnopqrst", True)["channel_id"]) == int

def test_edge():
    with pytest.raises(InputError):
        channels_create_v1(1234567, "", True)["channel_id"]
        channels_create_v1(1234567, "abcdefghijklmnopqrst0", True)["channel_id"]
import requests
from src.config import url

# REGULAR SEASON TESTS
def test_standup_start_standup_period_0_sec(register_three_users):
    pass

def test_standup_start_standup_period_5_sec(register_three_users):
    pass


# PRE SEASON TESTS - INPUT ERR
def test_standup_start_channelid_invalid():
    pass

def test_standup_start_standup_period_neg_1_sec():
    pass

def test_standup_start_active_standup_running():
    pass

# PRE SEASON TESTS - ACCESS ERR
def test_standup_start_channel_id_valid_user_not_member():
    pass

def test_standup_start_token_invalid():
    pass
    
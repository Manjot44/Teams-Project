from src.auth import auth_register_v1
from src.channels import channels_create_v1
import pytest 
from src.other import clear_v1
from src.error import AccessError

def test_clear_v1():
    clear_v1()
    user = auth_register_v1("jerrylin@jerry.com", "jerrylin", "jerry", "lin")['auth_user_id']
    clear_v1()

    with pytest.raises(AccessError):
        channels_create_v1(user, "foo", True)['channel_id']

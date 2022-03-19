from src.data_store import data_store
from src import auth, channel, channels, error, other
from src.data_store import data_store
from src.channels import channels_create_v1
from src.error import InputError, AccessError

def check_valid_id(auth_user_id, data):
    has_auth_user = False
    which_auth = 0
    for idx, auth_user in enumerate(data["users"]):
        if auth_user["u_id"] == auth_user_id and auth_user_id != None:
            has_auth_user = True
            which_auth = idx
    if has_auth_user == False:
        raise AccessError(f"Error: User does not have a valid ID")

    return which_auth

def validate_channel(data, channel_id):
    valid_channel = False
    for channel in data['channels']:
        if channel_id == channel['channel_id']:
            if channel_id != None:
                valid_channel = True
    if valid_channel == False:
        raise error.InputError()   # error as channel id is not valid

def check_channel_priv(data, channel_id, which_auth):
    if data["channels"][channel_id]["is_public"] == False and data['users'][which_auth]['perm_id'] == 2: 
        raise AccessError('Error: Cannot join private channel without being invited')

def check_channel_user(data, auth_user_id, channel_id):
    users = data["channels"][channel_id]["all_members"]
    for user in users:
        if user['u_id'] == auth_user_id and auth_user_id != None:
            raise InputError(f"Error: User is already member of the channel")

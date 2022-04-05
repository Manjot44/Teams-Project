from src.data_store import data_store
from src.error import InputError, AccessError

MEMBER = 2

def check_valid_token(token, data):
    u_id = None
    valid_token = False
    for user in data["users"].items():
        if token in user[1]["valid_tokens"]:
            valid_token = True
            u_id = user[0]
    if valid_token == False:
        raise AccessError(f"Error: User does not have a valid token")
    return u_id

def check_valid_id(u_id, data):
    if u_id not in data["users"].keys() or u_id == None:
        raise InputError(f"Error: {u_id} does not have a valid ID")

def validate_channel(data, channel_id):
    if channel_id not in data["channels"].keys or channel_id == None:
        raise InputError(f"Error: {channel_id} not valid")

def check_channel_priv(data, channel_id, which_auth):
    if data["channels"][channel_id]["is_public"] == False and data['users'][which_auth]['perm_id'] == MEMBER: 
        raise AccessError('Error: Cannot join private channel without being invited')

def check_channel_user(data, u_id, channel_id):
    users = data["channels"][channel_id]["all_members"]
    if u_id in users.keys() and u_id != None:
        raise InputError(f"Error: {u_id} is already member of the channel")

def auth_user_not_in_channel(data, auth_user_id, channel_id):
    users = data["channels"][channel_id]["all_members"]
    if auth_user_id not in users.keys() or auth_user_id == None:
        raise AccessError(f"Error: {auth_user_id} not in specific channel")

def user_not_in_channel(data, u_id, channel_id):
    users = data["channels"][channel_id]["all_members"]
    if u_id not in users.keys() or u_id == None:
        raise InputError(f"Error: {u_id} not in specific channel")

def auth_channel_owner_perm(data, auth_user_id, channel_id):
    auth_user_not_in_channel(data, auth_user_id, channel_id)
    if auth_user_id not in data["channels"][channel_id]["owner_members"].keys():
        if data["users"][auth_user_id]["perm_id"] == MEMBER:
            raise AccessError(f"Error: {auth_user_id} does not have owner permissions in the channel")

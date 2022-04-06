from src.data_store import data_store
from src.error import InputError, AccessError

MEMBER = 2
OWNER = 1

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
    if channel_id not in data["channels"].keys() or channel_id == None:
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

def check_message_id(data, message_id):
    dm_message = False
    channel_message = False
    if message_id in data['channel_messages'].keys() and message_id != None:
        channel_message = True
    if message_id in data['dm_messages'].keys() and message_id != None:
        dm_message = True

    if dm_message == False and channel_message == False:
        raise InputError(f"Error: Message_id not valid")
    
    return channel_message

def check_channelmess_perms(store, auth_user_id, message_id):
    channel_id = store["channel_messages"][message_id]["channel_id"]
    if store["channel_messages"][message_id]["u_id"] != auth_user_id:
        auth_channel_owner_perm(store, auth_user_id, channel_id)
    
def check_dmmess_perms(store, auth_user_id, message_id):
    dm_id = store["dm_messages"][message_id]["dm_id"]
    if store["dm_messages"][message_id]["u_id"] != auth_user_id:
        if store["dms"][dm_id]["creator_id"] != auth_user_id and store["users"][auth_user_id]["perm_id"] == MEMBER:
            raise AccessError(f"Error: Forbidden from editing message")

def check_global_owner_count(data, u_id):
    global_count = 0
    for user in data['users'].values():
        if user['perm_id'] == OWNER:
            global_count += 1
    if global_count == 1 and data["users"][u_id]["perm_id"] == OWNER:
        raise InputError(f"Error: Need to at least have one global owner")

def check_global_owner(data, u_id):
    if data['users'][u_id]['perm_id'] == MEMBER:
        raise AccessError(f"Error: {u_id} is not a global owner")
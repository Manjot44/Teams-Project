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
    if u_id not in data["users"].keys() or u_id == -1:
        raise InputError(f"Error: {u_id} does not have a valid ID")

def validate_channel(data, channel_id):
    if channel_id not in data["channels"].keys() or channel_id == -1:
        raise InputError(f"Error: {channel_id} not valid")

def check_channel_priv(data, channel_id, u_id):
    if data["channels"][channel_id]["is_public"] == False and data['users'][u_id]['perm_id'] == MEMBER: 
        raise AccessError('Error: Cannot join private channel without being invited')

def check_channel_user(data, u_id, channel_id):
    users = data["channels"][channel_id]["member_ids"]
    if u_id in users:
        raise InputError(f"Error: {u_id} is already member of the channel")

def auth_user_not_in_channel(data, auth_user_id, channel_id):
    users = data["channels"][channel_id]["member_ids"]
    if auth_user_id not in users:
        raise AccessError(f"Error: {auth_user_id} not in specific channel")

def user_not_in_channel(data, u_id, channel_id):
    users = data["channels"][channel_id]["member_ids"]
    if u_id not in users:
        raise InputError(f"Error: {u_id} not in specific channel")

def auth_channel_owner_perm(data, auth_user_id, channel_id):
    auth_user_not_in_channel(data, auth_user_id, channel_id)
    if auth_user_id not in data["channels"][channel_id]["owner_ids"]:
        if data["users"][auth_user_id]["perm_id"] == MEMBER:
            raise AccessError(f"Error: {auth_user_id} does not have owner permissions in the channel")

def check_message_id(data, message_id):
    if message_id not in data['messages'].keys() or message_id == -1:
        raise InputError(f"Error: Message_id not valid")
    
    channeldm_id = 0
    for id, channel in data['channels'].items():
        if message_id in channel['message_ids']:
            channeldm_id = id
    for id, dm in data['dms'].items():
        if message_id in dm['message_ids']:
            channeldm_id = id
    
    return channeldm_id

def check_channelmess_perms(store, auth_user_id, channel_id, message_id):
    if store["messages"][message_id]["u_id"] != auth_user_id:
        auth_channel_owner_perm(store, auth_user_id, channel_id)
    
def check_dmmess_perms(store, auth_user_id, dm_id, message_id):
    if store["messages"][message_id]["u_id"] != auth_user_id:
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

def validate_dm(data, dm_id):
    if dm_id not in data["dms"].keys() or dm_id == -1:
        raise InputError(f"Error: DM {dm_id} not valid")

def user_not_in_dm(data, u_id, dm_id):
    users = data["dms"][dm_id]["member_ids"]
    if u_id not in users:
        raise InputError(f"Error: {u_id} not in specific channel")
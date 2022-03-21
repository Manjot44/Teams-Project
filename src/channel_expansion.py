from src.data_store import data_store
import src.error_help
from src.error import InputError, AccessError

def channel_leave_v1(token, channel_id):
    '''Given a channel with ID channel_id that the authorised user is a member of, remove them as a member of the channel

    Arguments:
        token (str) - jwt passed in,
        channel_id (str) - channel identification number

    Exceptions:
        InputError  - Occurs when:
            channel_id does not refer to a valid channel
        AccessError - Occurs when:
            token passed in is not valid,
            channel_id is valid and the authorised user is not a member of the channel 

    Return Value:
        (dict): returns an empty dictionary
    '''
    store = data_store.get()
    auth_user_id = src.error_help.check_valid_token(token, store)
    src.error_help.validate_channel(store, channel_id)
    src.error_help.user_not_in_channel(store, auth_user_id, channel_id)    
    
    for idx, member in enumerate(store["channels"][channel_id]["all_members"]):
        if member["u_id"] == auth_user_id:
            store["channels"][channel_id]["all_members"].pop(idx)
            break
    
    for idx, member in enumerate(store["channels"][channel_id]["owner_members"]):
        if member["u_id"] == auth_user_id:
            store["channels"][channel_id]["owner_members"].pop(idx)
            break
    
    return {
    }

def channel_addowner_v1(token, channel_id, u_id):
    '''Given a channel with ID channel_id that the authorised user is a member of, remove them as a member of the channel

    Arguments:
        token (str) - jwt passed in,
        channel_id (str) - channel identification number,
        u_id (int) - user authentication id number

    Exceptions:
        InputError  - Occurs when:
            channel_id does not refer to a valid channel,
            u_id does not refer to a valid user,
            u_id refers to a user who is not a member of the channel,
            u_id refers to a user who is already an owner of the channel
        AccessError - Occurs when:
            token passed in is not valid,
            channel_id is valid and the authorised user does not have owner permissions in the channel

    Return Value:
        (dict): returns an empty dictionary
    '''
    store = data_store.get()   
    
    auth_user_id = src.error_help.check_valid_token(token, store)
    src.error_help.validate_channel(store, channel_id)
    src.error_help.check_valid_id(u_id, store)
    src.error_help.user_not_in_channel(store, u_id, channel_id)

    for owner in store["channels"][channel_id]["owner_members"]:
        if owner["u_id"] == u_id:
            raise InputError(f"Error: {u_id} is already an owner of the channel")
    
    is_owner = False
    for owner in store["channels"][channel_id]["owner_members"]:
        if owner["u_id"] == auth_user_id:
            is_owner = True
    if is_owner == False:
        if store["users"][auth_user_id]["perm_id"] == 2:
            raise AccessError(f"Error: channel_id is valid and the authorised user does not have owner permissions in the channel")

    add_user_info = {
        'u_id': store['users'][u_id]['u_id'],
        'email': store['users'][u_id]['email'],
        'name_first': store['users'][u_id]['name_first'],
        'name_last': store['users'][u_id]['name_last'],
        'handle_str': store['users'][u_id]['handle_str'],
    }
    store["channels"][channel_id]["owner_members"].append(add_user_info)

    data_store.set(store)

    return {
    }

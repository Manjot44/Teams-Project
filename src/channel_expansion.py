from src.data_store import data_store
import src.error_help
from src.error import InputError, AccessError
import src.persistence

MEMBER = 2

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
    store = src.persistence.get_pickle()
    
    auth_user_id = src.error_help.check_valid_token(token, store)
    src.error_help.validate_channel(store, channel_id)
    src.error_help.auth_user_not_in_channel(store, auth_user_id, channel_id)
    
    store["channels"][channel_id]["all_members"].pop(auth_user_id)
    if auth_user_id in store["channels"][channel_id]["owner_members"].keys():
        store["channels"][channel_id]["owner_members"].pop(auth_user_id)
    
    src.persistence.set_pickle(store)
    return {
    }

def channel_addowner_v1(token, channel_id, u_id):
    '''Make user with user id u_id an owner of the channel

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
    store = src.persistence.get_pickle()
    
    auth_user_id = src.error_help.check_valid_token(token, store)
    src.error_help.validate_channel(store, channel_id)
    src.error_help.check_valid_id(u_id, store)
    src.error_help.user_not_in_channel(store, u_id, channel_id)
    if u_id in store["channels"][channel_id]["owner_members"].keys():
        raise InputError(f"Error: {u_id} is already an owner of the channel")
    src.error_help.auth_channel_owner_perm(store, auth_user_id, channel_id)

    add_user_info = {k: store['users'][auth_user_id][k] for k in ('u_id', 'email', 'name_first', 'name_last', 'handle_str')}
    store["channels"][channel_id]["owner_members"][u_id] = add_user_info

    src.persistence.set_pickle(store)

    return {
    }

def channel_removeowner_v1(token, channel_id, u_id):
    '''Remove user with user id u_id as an owner of the channel

    Arguments:
        token (str) - jwt passed in,
        channel_id (str) - channel identification number,
        u_id (int) - user authentication id number

    Exceptions:
        InputError  - Occurs when:
            channel_id does not refer to a valid channel,
            u_id does not refer to a valid user,
            u_id refers to a user who is not an owner of the channel,
            u_id refers to a user who is currently the only owner of the channel
        AccessError - Occurs when:
            token passed in is not valid,
            channel_id is valid and the authorised user does not have owner permissions in the channel

    Return Value:
        (dict): returns an empty dictionary
    '''
    store = src.persistence.get_pickle()

    auth_user_id = src.error_help.check_valid_token(token, store)
    src.error_help.validate_channel(store, channel_id)
    src.error_help.check_valid_id(u_id, store)
    if u_id not in store["channels"][channel_id]["owner_members"].keys():
        raise InputError(f"Error: {u_id} refers to a user who is not an owner of the channel")
    if len(store["channels"][channel_id]["owner_members"]) == 1:
        raise InputError(f"Error: {u_id} refers to a user who is currently the only owner of the channel")
    src.error_help.auth_channel_owner_perm(store, auth_user_id, channel_id)
    
    store["channels"][channel_id]["owner_members"].pop(u_id)

    src.persistence.set_pickle(store)

    return {
    }    

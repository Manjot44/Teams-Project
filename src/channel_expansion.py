from src.data_store import data_store
import src.error_help

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
    
    data_store.set(store)
    return {
    }

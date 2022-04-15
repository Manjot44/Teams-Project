from src.error import InputError
from src.error_help import check_valid_token
import src.persistence

def channels_list_v1(token):
    '''Provide a list of all channels (and their associated details) that the authorised user is part of.

    Arguments:
        auth_user_id (int) - user authentication id number

    Exceptions:
        AccessError - Occurs when:
            auth_user_id passed in is not valid

    Return Value:
        (dict): returns a dictionary with the list of channels the user is a part of, displayed as channel_id and name 
    '''

    store = src.persistence.get_pickle()

    auth_user_id = check_valid_token(token, store)

    channels_list = []

    for channel in store["channels"].values():
        if auth_user_id in channel["member_ids"]:
            channels_list.append({
                    'channel_id': channel["channel_id"],
                    'name': channel["name"]
                })

    return {
        "channels": channels_list
    }


def channels_listall_v1(token):
    '''Provide a list of all channels, including private channels, (and their associated details)

    Arguments:
        auth_user_id (int) - user authentication id number

    Exceptions:
        AccessError - Occurs when:
            auth_user_id passed in is not valid

    Return Value:
        (dict): returns a dictionary with key 'channels' which is a list of dictionaries with 'channel_id' and 'name'
    '''

    saved_data = src.persistence.get_pickle()
    check_valid_token(token, saved_data)

    listall_return = {
        'channels': []
    }
    
    if -1 not in saved_data['channels'].keys():
        for channel in saved_data['channels'].values():
            appended_channel = {
                'channel_id': channel['channel_id'],
                'name': channel['name'],
            }
            listall_return['channels'].append(appended_channel)

    return listall_return


def channels_create_v1(token, name, is_public):
    '''Creates a new channel with the given name that is either a public or private channel. 
    The user who created it automatically joins the channel.

    Arguments:
        token (str) - user authentication token

    Exceptions:
        InputError - Occurs when:
            length of name is less than 1 or more than 20 characters
        AccessError - Occurs when:
            Token passed in is not valid

    Return Value: 
        (dict): returns a dictionary with the newly created channel_id 

    '''

    store = src.persistence.get_pickle()

    namelen = len(name)
    if namelen < 1 or namelen > 20:
        raise InputError(f"Name must be between 1 and 20 characters long")

    auth_user_id = check_valid_token(token, store)

    store["id"] += 1
    channel_id = store["id"]

    if -1 in store["channels"].keys():
        store["channels"] = {}

    store["channels"][channel_id] = {
        "channel_id": channel_id,
        "name": name,
        "owner_ids": [auth_user_id],
        "member_ids": [auth_user_id],
        "is_public": is_public,
        "message_ids": [],
        'standup': {
            'is_active': False,
            'time_finish': None,
            'queue': [],
        },
    }

    src.persistence.set_pickle(store)

    return {
        'channel_id': channel_id,
    }

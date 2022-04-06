from src.error import InputError, AccessError
from src.data_store import data_store
from src.error_help import check_valid_id, validate_channel, check_channel_priv, check_channel_user, user_not_in_channel, check_valid_token


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

    store = data_store.get()

    auth_user_id = check_valid_token(token, store)

    channels_list = []

    for channel in store["channels"].items():
        if auth_user_id in channel[1]["all_members"]:
            channels_list.append({
                    'channel_id': channel[0],
                    'name': channel[1]["name"]
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
        Returns {
            'channel_id': channel_id (int),
            'name': channel_name (str),
            'owner_members': [
                {
                    'u_id': id (int),
                    'email': email (str),
                    'name_first': name_first (str),
                    'name_last': name_last (str),
                    'handle_str': handle (str),
                }
            ],
            'all_members': [
                {
                    'u_id': id (int),
                    'email': email (str),
                    'name_first': name_first (str),
                    'name_last': name_last (str),
                    'handle_str': handle (str),
                }
            ],
            'is_public': public (bool),
            'messages': [
                {
                    'message_id': message_id (int),
                    'u_id': u_id (int),
                    'message': message (str),
                    'time_sent': time (int),
                },
            ]
        }
    '''

    saved_data = data_store.get()
    check_valid_token(token, saved_data)

    listall_return = {
        'channels': []
    }
    
    if None not in saved_data['channels'].keys():
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

    store = data_store.get()

    namelen = len(name)
    if namelen < 1 or namelen > 20:
        raise InputError(f"Name must be between 1 and 20 characters long")

    auth_user_id = check_valid_token(token, store)

    store["channel_id"] += 1
    channel_id = store["channel_id"]

    add_user = {k: store['users'][auth_user_id][k] for k in ('u_id', 'email', 'name_first', 'name_last', 'handle_str', 'profile_img_url')}

    if None in store["channels"].keys():
        store["channels"] = {
            }

    store["channels"][channel_id] = {
        "channel_id": channel_id,
        "name": name,
        "owner_members": {
            auth_user_id: add_user
        },
        "all_members": {
            auth_user_id: add_user
        },
        "is_public": is_public
    }

    data_store.set(store)

    return {
        'channel_id': channel_id,
    }

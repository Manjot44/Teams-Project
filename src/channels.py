from src.error import InputError, AccessError
from src.data_store import data_store
from src.error_help import check_valid_id, validate_channel, check_channel_priv, check_channel_user, user_not_in_channel, check_valid_token


def channels_list_v1(auth_user_id):
    '''Provide a list of all channels (and their associated details) that the authorised user is part of.

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

    # Getting Data from data storage file
    store = data_store.get()

    # Assessing for Access Error
    check_valid_id(auth_user_id, store)

    # Creating empty list for the channels the user is part of
    channels_list = []

    # Looping through all channels and adding the channels that the user is part of to "channels_list"
    for channel in store["channels"]:
        for member in channel["all_members"]:
            if auth_user_id == member["u_id"]:
                channels_list.append(channel)

    fixstore = {
        "channels": channels_list
    }
    return fixstore


def channels_listall_v1(auth_user_id):
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

    # dictionary that is to be returned by function
    listall = {
        'channels': []
    }

    saved_data = data_store.get()

    # validate auth user id
    check_valid_id(auth_user_id, saved_data)

    # copying channels to 'listall' dict from saved channel data
    listall['channels'] = saved_data['channels']

    return listall


def channels_create_v1(auth_user_id, name, is_public):
    '''Creates a new channel with the given name that is either a public or private channel. 
    The user who created it automatically joins the channel.

    Arguments:
        auth_user_id (int) - user authentication id number

    Exceptions:
        InputError - Occurs when:
            length of name is less than 1 or more than 20 characters
        AccessError - Occurs when:
            auth_user_id passed in is not valid

    Return Value:
        Returns {
            'channel_id': channel_id,
        }
    '''

    # Getting Data from data storage file
    store = data_store.get()

    # Assessing for exception
    namelen = len(name)
    if namelen < 1 or namelen > 20:
        raise InputError(f"Name must be between 1 and 20 characters long")

    which_user = check_valid_id(auth_user_id, store)

    # Creates and adds the new channel to the channels list
    if store["channels"][0]["channel_id"] == None:
        store["channels"] = []
    channel_id = len(store["channels"])
    nc = {}
    nc["channel_id"] = channel_id
    store["channels"].append(nc)

    # Assigning variable to newly created channel
    current_channel = store["channels"][channel_id]

    # Assigning user inputs
    current_channel["channel_id"] = channel_id
    current_channel["name"] = name
    current_channel["is_public"] = is_public
    current_channel["messages"] = []

    add_user = {
        'u_id': store['users'][which_user]['u_id'],
        'email': store['users'][which_user]['email'],
        'name_first': store['users'][which_user]['name_first'],
        'name_last': store['users'][which_user]['name_last'],
        'handle_str': store['users'][which_user]['handle_str'],
    }

    current_channel["all_members"] = [add_user]
    current_channel["owner_members"] = [add_user]

    # Saving to datastore
    data_store.set(store)

    return {
        'channel_id': channel_id,
    }

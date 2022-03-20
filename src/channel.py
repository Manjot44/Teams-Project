from src.data_store import data_store
from src import auth, channel, channels, error, other
from src.data_store import data_store
from src.channels import channels_create_v1
from src.error import InputError, AccessError
from src.error_help import check_valid_id, validate_channel, check_channel_priv, check_channel_user, user_not_in_channel

def channel_invite_v1(auth_user_id, channel_id, u_id):
    '''Invites a user with ID u_id to join a channel with ID channel_id. 
    Once invited, the user is added to the channel immediately. 
    In both public and private channels, all members are able to invite users.

    Arguments:
        auth_user_id (int) - user authentication id number (of person inviting),
        channel_id (int) - channel identification number,
        u_id (int) - user authentication id number (of person being invited)

    Exceptions:
        InputError  - Occurs when:
            channel_id does not refer to a valid channel,
            u_id does not refer to a valid user,
            u_id refers to a user who is already a member of the channel
        AccessError - Occurs when:
            auth_user_id passed in is not valid,
            channel_id is valid and the authorised user is not a member of the channel

    Return Value:
        Returns {}
    '''
    
    store = data_store.get()

    check_valid_id(auth_user_id, store)
    has_u_id = False
    which_auth = 0
    for idx, user in enumerate(store["users"]):
        if user["u_id"] == u_id:
            if auth_user_id != None:    
                has_u_id = True
                which_auth = idx
    if has_u_id == False:
        raise InputError(f"Error: User does not have a valid ID")

    validate_channel(store, channel_id)

    # Checks if auth_user is in the channel of channel_id
    user_not_in_channel(store, auth_user_id, channel_id)
    check_channel_user(store, u_id, channel_id)

    # Once the above functions run and confirm that the auth_user is in channel and that u_id valid, u_id will be added to channel 
    add_user_info = {
        'u_id': store['users'][which_auth]['u_id'],
        'email': store['users'][which_auth]['email'],
        'name_first': store['users'][which_auth]['name_first'],
        'name_last': store['users'][which_auth]['name_last'],
        'handle_str': store['users'][which_auth]['handle_str'],
    }
    users = store["channels"][channel_id]["all_members"]
    users.append(add_user_info)
    data_store.set(store)
    return {
    }

def channel_details_v1(auth_user_id, channel_id):
    '''Given a channel with ID channel_id that the authorised user is a member of, provide basic details about the channel.

    Arguments:
        auth_user_id (int) - user authentication id number,
        channel_id (int) - channel identification number

    Exceptions:
        InputError  - Occurs when:
            channel_id does not refer to a valid channel
        AccessError - Occurs when:
            auth_user_id passed in is not valid,
            channel_id is valid and the authorised user is not a member of the channel 

    Return Value:
        Returns {
            'name': channel_name (str),
            'is_public': public (bool),
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
        }
    '''

    # dictionary that is to be returned with function
    details = {
        'name': None,
        'is_public': None,
        'owner_members': [],
        'all_members': [],
    }

    saved_data = data_store.get()
    check_valid_id(auth_user_id, saved_data)
    validate_channel(saved_data, channel_id)

    # validate user is member of channel
    user_not_in_channel(saved_data, auth_user_id, channel_id)

    # configuring 'name' key
    details['name'] = saved_data['channels'][channel_id]['name']
    
    # configuring 'is_public' key
    public = saved_data['channels'][channel_id]['is_public']
    details['is_public'] = public

    # configuring 'owner_members' key
    details['owner_members'] = saved_data['channels'][channel_id]['owner_members']

    # configuring 'all_members' key
    details['all_members'] = saved_data['channels'][channel_id]['all_members']

    return details


def channel_messages_v1(auth_user_id, channel_id, start):
    '''Given a channel with ID channel_id that the authorised user is a member of, 
    return up to 50 messages between index "start" and "start + 50". 
    Message with index 0 is the most recent message in the channel. 
    This function returns a new index "end" which is the value of "start + 50", or, 
    if this function has returned the least recent messages in the channel, returns -1 in "end" to 
    indicate there are no more messages to load after this return

    Arguments:
        auth_user_id (int) - user authentication id number,
        channel_id (int) - channel identification number,
        start (int) - which message to start from (0 is the most recent)

    Exceptions:
        InputError  - Occurs when:
            channel_id does not refer to a valid channel,
            start is greater than the total number of messages in the channel
        AccessError - Occurs when:
            auth_user_id passed in is not valid,
            channel_id is valid and the authorised user is not a member of the channel
    
    Return Value:
        Returns {
            'messages': [
                {
                    'message_id': message_id (int),
                    'u_id': u_id (int),
                    'message': message (str),
                    'time_sent': time (int),
                }
            ],
            'start': start (int),
            'end: end (int),
        }
    '''

    store = data_store.get()
    check_valid_id(auth_user_id, store)
    validate_channel(store, channel_id)
    user_not_in_channel(store, auth_user_id, channel_id)

    messagesreturn = {
        'messages': [],
        'start': start, 
        'end': start + 50
    }
    
    messages = store['channels'][channel_id]['messages']

    if start > len(messages):
        raise error.InputError(f"start must be smaller than total amount of messages")

    if start + 50 > len(messages):
        messagesreturn['end'] = -1
        messagesreturn['messages'] = messages
    else:
        messagesreturn['messages'] = messages[:50]

    return messagesreturn        

def channel_join_v1(auth_user_id, channel_id):
    '''Given a channel_id of a channel that the authorised user can join, adds them to that channel.

    Arguments:
        auth_user_id (int) - user authentication id number,
        channel_id (int) - channel identification number

    Exceptions:
        InputError  - Occurs when:
            channel_id does not refer to a valid channel,
            the authorised user is already a member of the channel
        AccessError - Occurs when:
            auth_user_id passed in is not valid,
            channel_id refers to a channel that is private and 
            the authorised user is not already a channel member and is not a global owner
    
    Return Value:
        Returns {}
    '''
    
    store = data_store.get()

    # Checks if the auth_user_id is valid
    which_auth = check_valid_id(auth_user_id, store)
    validate_channel(store, channel_id)
    check_channel_priv(store, channel_id, which_auth)
    check_channel_user(store, auth_user_id, channel_id)
    
    # Once confirmed that user is not in channel, user will be added
    add_user_info = {
        'u_id': store['users'][which_auth]['u_id'],
        'email': store['users'][which_auth]['email'],
        'name_first': store['users'][which_auth]['name_first'],
        'name_last': store['users'][which_auth]['name_last'],
        'handle_str': store['users'][which_auth]['handle_str'],
    }
    users = store["channels"][channel_id]["all_members"]
    users.append(add_user_info)
    data_store.set(store)
    return {
    }

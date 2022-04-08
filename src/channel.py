from src.error import InputError
from src.error_help import check_valid_token, check_valid_id, validate_channel, check_channel_priv, check_channel_user, auth_user_not_in_channel
import src.persistence

def channel_invite_v1(token, channel_id, u_id):
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
        (dict): returns an empty dictionary
    '''
    
    store = src.persistence.get_pickle()

    auth_user_id = check_valid_token(token, store)
    check_valid_id(u_id, store)
    validate_channel(store, channel_id)
    auth_user_not_in_channel(store, auth_user_id, channel_id)
    check_channel_user(store, u_id, channel_id)

    store["channels"][channel_id]["member_ids"].append(u_id)
    
    src.persistence.set_pickle(store)
    return {
    }

def channel_details_v1(token, channel_id):
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
        (dict): returns dictionary with keys 'name', 'is_public', 'all_members', and 'owner_members'
    '''
    
    saved_data = src.persistence.get_pickle()
    u_id = check_valid_token(token, saved_data)
    validate_channel(saved_data, channel_id)
    auth_user_not_in_channel(saved_data, u_id, channel_id)

    channel = saved_data['channels'][channel_id]
    details = {
        'name': channel['name'],
        'is_public': channel['is_public'],
        'owner_members': [],
        'all_members': [],
    }

    for u_id in channel['member_ids']:
        add_new = {k:saved_data['users'][u_id][k] for k in ('u_id', 'email', 'name_first', 'name_last', 'handle_str', 'profile_img_url')}
        details['all_members'].append(add_new)
        if u_id in channel['owner_ids']:
            details['owner_members'].append(add_new)

    return details


def channel_messages_v1(token, channel_id, start):
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
        (dict): returns a dictionary with keys 'messages', 'start', and 'end'
    '''

    store = src.persistence.get_pickle()
    auth_user_id = check_valid_token(token, store)
    validate_channel(store, channel_id)
    auth_user_not_in_channel(store, auth_user_id, channel_id)
    if start > len(store['channels'][channel_id]['message_ids']):
        raise InputError(f"start must be smaller than total amount of messages")

    messagesreturn = {
        'messages': [],
        'start': start, 
        'end': start + 50
    }
    
    for message_id in store['channels'][channel_id]['message_ids']:
        messagesreturn['messages'].append(store['messages'][message_id])
    messagesreturn['messages'].reverse()
    
    if start + 50 > len(messagesreturn['messages']):
        messagesreturn['end'] = -1
        messagesreturn['messages'] = messagesreturn['messages'][start:]   
    else:
        messagesreturn['messages'] = messagesreturn['messages'][start:start + 50]
        messagesreturn['end'] = start + 50

    return messagesreturn  

def channel_join_v1(token, channel_id):
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
        (dict): returns an empty dictionary
    '''
    
    store = src.persistence.get_pickle()
    auth_user_id = check_valid_token(token, store)
    validate_channel(store, channel_id)
    check_channel_priv(store, channel_id, auth_user_id)
    check_channel_user(store, auth_user_id, channel_id)
    
    store["channels"][channel_id]["member_ids"].append(auth_user_id)
    src.persistence.set_pickle(store)

    return {
    }

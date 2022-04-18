import src.persistence
import src.channels
import src.dm
import src.error_help
from src.error import InputError


def which_messages(token, store):
    '''Finds which messages are relevant to the user with inputted token

    Arguments:
        token (str) - jwt passed in,
        store (dict) - all stored data

    Exceptions:
        N/A

    Return Value:
        (list): returns the list of relevant message ids
    '''
    channel_ids = []
    which_channels = src.channels.channels_list_v1(token)['channels']
    for channel in which_channels:
        channel_ids.append(channel['channel_id'])
    
    dm_ids = []
    which_dms = src.dm.dm_list_v1(token)['dms']
    for dm in which_dms:
        dm_ids.append(dm['dm_id'])
    
    which_messages = []
    for id in channel_ids:
        which_messages += store['channels'][id]['message_ids']
    for id in dm_ids:
        which_messages += store['dms'][id]['message_ids']
    
    return which_messages


def set_react(new_message, auth_user_id):
    '''Sets the 'is_this_user_reacted' field for the auth_user

    Arguments:
        new_message (dict) - message for which reactions neeed to be set,
        auth_user_id (int) - user id of the auth_user

    Exceptions:
        N/A

    Return Value:
        (dict): returns the message with the set reactions
    '''
    for reaction in new_message['reacts'].values():
        if auth_user_id in reaction['u_ids']:
            reaction['is_this_user_reacted'] = True
        else:
            reaction['is_this_user_reacted'] = False
    new_message['reacts'] = list(new_message['reacts'].values())
    
    return new_message



def search_v1(token, query_str):
    '''Given a query string, return a collection of messages in all of the channels/DMs 
    that the user has joined that contain the query (case-insensitive).

    Arguments:
        token (str) - jwt passed in,
        query_str (str) - keyword/s to search for

    Exceptions:
        InputError - Occurs when:
            length of query_str is less than 1 or over 1000 characters
        AccessError - Occurs when:
            token passed in is not valid

    Return Value:
        (dict): returns a dictionary with the 'messages' key, which is a list of messages
    '''
    store = src.persistence.get_pickle()

    auth_user_id = src.error_help.check_valid_token(token, store)

    if query_str == None or len(query_str) < 1 or len(query_str) > 1000:
        raise InputError(f"Query string must be in between 1 and 1000 characters inclusive")
    
    message_ids = which_messages(token, store)

    print(message_ids)

    query_str = query_str.lower()
    searched_messages = []
    for id in message_ids:
        lower_message = store['messages'][id]['message'].lower()
        if query_str in lower_message:
            new_message = {k:store['messages'][id][k] for k in ('message_id', 'u_id', 'message', 'time_sent', 'reacts', 'is_pinned')}
            new_message = set_react(new_message, auth_user_id)
            searched_messages.append(new_message)

    return {
        'messages': searched_messages
    }

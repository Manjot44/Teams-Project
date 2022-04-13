import src.persistence
import src.channels
import src.dm
import src.error_help
from src.error import InputError


def which_messages(token, store):
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



def search_v1(token, query_str):
    store = src.persistence.get_pickle()

    src.error_help.check_valid_token(token, store)

    if query_str == None or len(query_str) < 1 or len(query_str) > 1000:
        raise InputError(f"Query string must be in between 1 and 1000 characters inclusive")
    
    message_ids = which_messages(token, store)

    query_str.lower()
    searched_messages = []
    for id in message_ids:
        store['messages'][id]['message'].lower()
        if query_str in store['messages'][id]['message']:
            new_message = {k:store['messages'][id][k] for k in ('message_id', 'u_id', 'message', 'time_sent', 'reacts', 'is_pinned')}
            searched_messages.append(new_message)
        
    return {
        'messages': searched_messages
    }

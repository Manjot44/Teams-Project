from src.error_help import check_valid_token, validate_channel, auth_user_not_in_channel
from src.error import InputError, AccessError
import src.persistence
from datetime import datetime
import threading
import requests
from src.config import url

def standup_send_queue(token, channel_id, time_finish):
    '''When called sends the messages that were queued in standup
    period as one message from authorised user.

    Arguments:
        token (str) - user authentication
        channel_id (int) - channel identification number
    '''
    store = src.persistence.get_pickle()
    queued_messages = store['channels'][channel_id]['standup']['queue']
    formatted_queue = ''
    for idx, message in enumerate(queued_messages):
        if idx != 0:
            formatted_queue += '\n'
        formatted_queue += message

    m_id = requests.post(f"{url}message/send/v1", json={'token': token, 'channel_id': channel_id, 'message': formatted_queue})
    store = src.persistence.get_pickle()
    store['messages'][m_id.json()['message_id']]['time_sent'] = time_finish
    store['channels'][channel_id]['standup']['is_active'] = False
    store['channels'][channel_id]['standup']['time_finish'] = None
    store['channels'][channel_id]['standup']['queue'] = []
    src.persistence.set_pickle(store)
    return


def standup_start_v1(token, channel_id, length):
    '''For given channel, starts the standup period where any calls
    to "standup/send" gets buffered during X second window then
    added to message queue as message from the user who called it.

    Arguments:
        token (str) - user authentication
        channel_id (int) - channel identification number
        length (int) - number of sec

    Exceptions:
        InputError - Occurs when:
            - channel_id does not refer to a valid channel
            - length is a negative integer
            - active standup is currently running in the channel
        AccessError - Occurs when:
            - token passed in is not valid
            - channel_id is valid and the authorised user is not a 
            member of the channel

    Return Value:
        (dict): returns a dictionary with 'time_finish' item
    '''
    store = src.persistence.get_pickle()
    u_id = check_valid_token(token, store)
    validate_channel(store, channel_id)
    auth_user_not_in_channel(store, u_id, channel_id)
    if length < 0 or None:
        raise InputError("Error: Length is a negative number.")
    if store['channels'][channel_id]['standup']['is_active'] == True:
        raise InputError("Error: Active standup currently running on this channel.")
    
    time_finish = round(datetime.now().timestamp()) + length
    store['channels'][channel_id]['standup']['is_active'] = True
    store['channels'][channel_id]['standup']['time_finish'] = time_finish
    send_queue = threading.Timer(length, standup_send_queue, args=(token, channel_id, time_finish,))
    send_queue.start()

    src.persistence.set_pickle(store)
    return {'time_finish': time_finish}
    

def standup_active_v1(token, channel_id):
    '''For given channel, return whether a standup is active in it,
    and what time the standup finishes.

    Arguments:
        token (str) - user authentication
        channel_id (int) - channel identification number

    Exceptions:
        InputError - Occurs when:
            - channel_id does not refer to a valid channel
        AccessError - Occurs when:
            - token passed in is not valid
            - channel_id is valid and the authorised user is not a 
            member of the channel

    Return Value:
        (dict): returns a dictionary with 'is_active' and 
        'time_finish' items
    '''
    store = src.persistence.get_pickle()
    u_id = check_valid_token(token, store)
    validate_channel(store, channel_id)
    auth_user_not_in_channel(store, u_id, channel_id)
    
    return {
        'is_active': store['channels'][channel_id]['standup']['is_active'],
        'time_finish': store['channels'][channel_id]['standup']['time_finish'],
    }


def standup_send_v1(token, channel_id, message):
    '''For given channel, sending a message to get buffered in the
    standup queue, assuming a standup is currently active.

    Arguments:
        token (str) - user authentication
        channel_id (int) - channel identification number
        message (str) - message to be sent to queue

    Exceptions:
        InputError - Occurs when:
            - channel_id does not refer to a valid channel
            - length of message is over 1000 characters
            - an active standup is not currently running in the channel
        AccessError - Occurs when:
            - token passed in is not valid
            - channel_id is valid and the authorised user is not a 
            member of the channel

    Return Value:
        (dict): returns empty dictionary 
    '''
    store = src.persistence.get_pickle()
    u_id = check_valid_token(token, store)
    validate_channel(store, channel_id)
    auth_user_not_in_channel(store, u_id, channel_id)
    if store['channels'][channel_id]['standup']['is_active'] == False:
        raise InputError("Error: Standup is not currently active in this channel.")
    if len(message) > 1000:
        raise InputError("Error: Message is over 1000 characters (standup).")

    user_handle = store['users'][u_id]['handle_str']
    store['channels'][channel_id]['standup']['queue'].append(f"{user_handle}: {message}")
    src.persistence.set_pickle(store)

    return {}
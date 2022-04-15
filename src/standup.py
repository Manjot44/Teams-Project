from src.error_help import check_valid_token, validate_channel, auth_user_not_in_channel
from src.error import InputError, AccessError
import src.persistence
from datetime import datetime
import threading
import requests
from src.config import url

def standup_send_queue(token, channel_id):
    store = src.persistence.get_pickle()
    # print(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>     1:    {store['channels'][channel_id]['standup']}      <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    queued_messages = store['channels'][channel_id]['standup']['queue']
    formatted_queue = ''
    for idx, message in enumerate(queued_messages):
        if idx != 0:
            formatted_queue += '\n'
        formatted_queue += message

    requests.post(f"{url}message/send/v1", json={'token': token, 'channel_id': channel_id, 'message': formatted_queue})
    store['channels'][channel_id]['standup']['is_active'] = False
    store['channels'][channel_id]['standup']['time_finish'] = None
    store['channels'][channel_id]['standup']['queue'] = []
    # src.persistence.set_pickle(store)
    return

def standup_deactivate(channel_id):
    store = src.persistence.get_pickle()
    store['channels'][channel_id]['standup']['is_active'] = False
    store['channels'][channel_id]['standup']['time_finish'] = None
    store['channels'][channel_id]['standup']['queue'] = []
    src.persistence.set_pickle(store)

def standup_start_v1(token, channel_id, length):
    ''' docstring '''
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
    send_queue = threading.Timer(length, standup_send_queue, args=(token, channel_id,))
    send_queue.start()
    deact = threading.Timer(length, standup_deactivate, args=(channel_id,))
    deact.start()

    src.persistence.set_pickle(store)
    return {'time_finish': time_finish}
    

def standup_active_v1(token, channel_id):
    '''doct str'''
    store = src.persistence.get_pickle()
    u_id = check_valid_token(token, store)
    validate_channel(store, channel_id)
    auth_user_not_in_channel(store, u_id, channel_id)
    
    return {
        'is_active': store['channels'][channel_id]['standup']['is_active'],
        'time_finish': store['channels'][channel_id]['standup']['time_finish'],
    }


def standup_send_v1(token, channel_id, message):
    '''doct str'''
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
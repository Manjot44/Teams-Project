from src.error_help import check_valid_token, validate_channel, auth_user_not_in_channel
from src.error import InputError, AccessError
import src.persistence
from datetime import datetime
import threading
import requests
from src.config import url

def standup_deactivate(token, channel_id, store):
    queued_messages = str(store['channels'][channel_id]['standup']['queue'])
    formatted_queue = ''
    for message in queued_messages:
        formatted_queue += message

    requests.post(f"{url}message/send/v1", json={'token': token, 'channel_id': channel_id, 'message': formatted_queue})
    store['channels'][channel_id]['standup']['is_active'] = False
    store['channels'][channel_id]['standup']['time_finish'] = None
    store['channels'][channel_id]['standup']['queue'] = []
    # src.persistence.set_pickle(store)
    return

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
    deactivate = threading.Timer(length, standup_deactivate, args=(token, channel_id, store,))
    deactivate.start()

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

    user_handle = store['users'][u_id]['handle_str']
    store['channels'][channel_id]['standup']['queue'].append(f"{user_handle}: {message}")
    src.persistence.set_pickle(store)

    return {}
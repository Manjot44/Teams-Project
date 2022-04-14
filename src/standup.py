from src.error_help import check_valid_token, validate_channel, auth_user_not_in_channel
from src.error import InputError, AccessError
import src.persistence
from datetime import datetime
import threading
import requests
from src.config import url

def standup_deactivate(token, channel_id):
    store = src.persistence.get_pickle()
    queued_messages = str(store['channels'][channel_id]['standup']['queue'])        # LINE NEEDS TO BE IMPLEMENTED CORRECTLY;
                                                                                    # QM HAS TO BE ARRANGED INTO STYLE OF STDUP MSG
    requests.post(f"{url}message/send/v1", json={'token': token, 'channel_id': channel_id, 'message': queued_messages})
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
    deactivate = threading.Timer(length, standup_deactivate(token, channel_id))
    deactivate.start()

    src.persistence.set_pickle(store)
    return {'time_finish': time_finish}
    

def standup_active_v1(token, channel_id):
    ''''doct str''''
    store = src.persistence.get_pickle()
    u_id = check_valid_token(token, store)
    validate_channel(store, channel_id)
    auth_user_not_in_channel(store, u_id, channel_id)
    return {
        'is_active': store['channels'][channel_id]['standup']['is_active'],
        'time_finish': store['channels'][channel_id]['standup']['time_finish'],
    }


def standup_send_v1(token, channel_id, message):
    pass

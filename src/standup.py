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
    store = src.persistence.get_pickle()
    # CHECK TOKEN VALID
    u_id = check_valid_token(token, store)
    # CHECK CHANNEL_ID VALID
    validate_channel(store, channel_id)
    # CHECK IF USER IS AUTHORISED MEMBER
    auth_user_not_in_channel(store, u_id, channel_id)
    # CHECK LENGTH VALID
    if length < 0 or None:
        raise InputError("Error: Length is a negative number.")
    # CHECK STANDUP ACTIVE
    if store['channels'][channel_id]['standup']['is_active'] == True:
        raise InputError("Error: Active standup currently running on this channel.")
    
    time_finish = round(datetime.now().timestamp()) + length
    store['channels'][channel_id]['standup']['is_active'] = True
    deactivate = threading.Timer(length, standup_deactivate(token, channel_id))
    deactivate.start()

    src.persistence.set_pickle(store)
    return {'time_finish': time_finish}
    


def standup_active_v1(token, channel_id):
    pass

def standup_send_v1(token, channel_id, message):
    pass

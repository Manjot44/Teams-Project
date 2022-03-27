from src.data_store import data_store
import src.error_help
from src.error import InputError, AccessError
import datetime

def message_send_v1(token, channel_id, message):
    
    store = data_store.get()
    
    auth_user_id = src.error_help.check_valid_token(token, store)
    src.error_help.validate_channel(store, channel_id)
    if message == None or len(message) < 1 or len(message) > 1000:
        raise InputError(f"Error: length of message is less than 1 or over 1000 characters")
    src.error_help.user_not_in_channel(store, auth_user_id, channel_id)

    if store["messages"][0]["message_id"] == None:
        store["messages"] = []
    id = len(store["messages"])
    
    current_time = datetime.datetime.now(datetime.timezone.utc)
    utc_time = current_time.replace(tzinfo=datetime.timezone.utc)
    unix_timestamp = utc_time.timestamp()

    new_message = {
        "message_id": id,
        "u_id": auth_user_id,
        "message": message,
        "time_sent": int(unix_timestamp),
        "channel_id": channel_id,
    }


    store["messages"].append(new_message)
    data_store.set(store)

    return {
        "message_id": id
    }

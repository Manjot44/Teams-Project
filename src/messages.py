from src.data_store import data_store
import src.error_help
from src.error import InputError, AccessError
import datetime
import src.persistence

MEMBER = 2
OWNER = 1

def message_send_v1(token, channel_id, message):
    ''' Send a message from the authorised user to the channel specified by channel_id. 
        Note: Each message should have its own unique ID, 
        i.e. no messages should share an ID with another message, 
        even if that other message is in a different channel.

        Arguments:
            token (str) - user authentication
            channel_id (int) - channel identification number
            message (str) - message being sent

        Exceptions:
            InputError - Occurs when:
                channel_id does not refer to a valid channel
                length of message is less than 1 or over 1000 characters

            AccessError - Occurs when:
                channel_id is valid and the authorised user is not a member of the channel
        
        Return Value:
            Returns {
                'message_id': message_id,
            }
    '''
    store = src.persistence.get_pickle()
    
    auth_user_id = src.error_help.check_valid_token(token, store)
    src.error_help.validate_channel(store, channel_id)
    if message == None or len(message) < 1 or len(message) > 1000:
        raise InputError(f"Error: length of message is less than 1 or over 1000 characters")
    src.error_help.auth_user_not_in_channel(store, auth_user_id, channel_id)

    store["message_id"] += 1
    id = store["message_id"]

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

    if None in store["channel_messages"].keys():
        store["channel_messages"] = {}
    store["channel_messages"][id] = new_message
    
    src.persistence.set_pickle(store)

    return {
        "message_id": id
    }

def message_edit_v1(token, message_id, message):
    ''' Given a message_id for a message, this message is removed from the channel/DM

        Arguments:
            token (str) - user authentication
            message_id (int) - identification number for message being edited
            message (str) - message being edited

        Exceptions:
            InputError - Occurs when:
                 - length of message is over 1000 characters
                 - message_id does not refer to a valid message within a channel/DM that the authorised user has joined

            AccesError - Occurs when message_id refers to a valid message in a joined channel/DM and none of the following are true:
                 - the message was sent by the authorised user making this request
                 - the authorised user has owner permissions in the channel/DM

        Return Value:
            Returns { 

            }
    '''
    store = src.persistence.get_pickle()

    auth_user_id = src.error_help.check_valid_token(token, store)
    is_channel_message = src.error_help.check_message_id(store, message_id)
    if len(message) > 1000: raise InputError(f"Error: Message over 1000 characters long")

    if is_channel_message == True:
        src.error_help.check_channelmess_perms(store, auth_user_id, message_id)
        if len(message) == 0:
            store["channel_messages"].pop(message_id)
        else:
            store["channel_messages"][message_id]["message"] = message
    else:
        src.error_help.check_dmmess_perms(store, auth_user_id, message_id)
        if len(message) == 0:
            store["dm_messages"].pop(message_id)
        else:
            store["dm_messages"][message_id]["message"] = message

    src.persistence.set_pickle(store)
    return {
    }

def message_remove_v1(token, message_id):
    ''' Given a message_id for a message, this message is removed from the channel/DM

        Arguments:
            token (str) - user authentication
            message_id (int) - identification number for message being deleted

        Exceptions:
            InputError - Occurs when:
                - message_id does not refer to a valid message within a channel/DM that the authorised user has joined
                
            AccessError - Occurs when:
                - the message was sent by the authorised user making this request
                - the authorised user has owner permissions in the channel/DM

        Return Value:
            Returns {

            }
    '''

    store = src.persistence.get_pickle()

    auth_user_id = src.error_help.check_valid_token(token, store)
    is_channel_message = src.error_help.check_message_id(store, message_id)

    if is_channel_message == True:
        src.error_help.check_channelmess_perms(store, auth_user_id, message_id)
        store["channel_messages"].pop(message_id)
    else:
        src.error_help.check_dmmess_perms(store, auth_user_id, message_id)
        store["dm_messages"].pop(message_id)

    src.persistence.set_pickle(store)
    return {
    }

def message_senddm_v1(token, dm_id, message):
    ''' Send a message from the authorised user to the DM specified by dm_id. 

        Arguments:
            token (str) - user authentication
            dm_id (int) - DM identification number
            message (str) - message being sent

        Exceptions:
            InputError - Occurs when:
                dm_id does not refer to a valid channel
                length of message is less than 1 or over 1000 characters

            AccessError - Occurs when:
                dm_id is valid and the authorised user is not a member of the DM
        
        Return Value:
            Returns {
                'message_id': message_id,
            }
    '''

    store = src.persistence.get_pickle()
    auth_user_id = src.error_help.check_valid_token(token, store)
    
    if None in store['dms'].keys() or dm_id not in store['dms'].keys():
        raise InputError(f"dm_id = {dm_id} is not valid")

    if message == None or len(message) < 1 or len(message) > 1000:
        raise InputError(f"Error: length of message is less than 1 or over 1000 characters")

    if auth_user_id not in store['dms'][dm_id]['all_members'].keys():
        raise AccessError(f"User is not member of DM")

    store['message_id'] += 1
    id = store['message_id']

    if None in store['dm_messages'].keys():
        store['dms'][dm_id]['messages'] = {}
    
    current_time = datetime.datetime.now(datetime.timezone.utc)
    utc_time = current_time.replace(tzinfo=datetime.timezone.utc)
    unix_timestamp = utc_time.timestamp()

    new_message = {
        "message_id": id,
        "dm_id": dm_id,
        "u_id": auth_user_id,
        "message": message,
        "time_sent": int(unix_timestamp),
    }

    store['dm_messages'][id] = new_message
    src.persistence.set_pickle(store)

    return {
        "message_id": id
    }

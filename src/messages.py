import src.error_help
from src.error import InputError, AccessError
import datetime
import src.persistence
import src.notifications
import threading

MEMBER = 2
OWNER = 1
SHARED_MSG_OFFSET = 9

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
            (dict): returns a dictionary with 'message_id'
    '''
    store = src.persistence.get_pickle()
    
    auth_user_id = src.error_help.check_valid_token(token, store)
    src.error_help.validate_channel(store, channel_id)
    if message == None or len(message) < 1 or len(message) > 1000:
        raise InputError(f"Error: length of message is less than 1 or over 1000 characters")
    src.error_help.auth_user_not_in_channel(store, auth_user_id, channel_id)

    store["id"] += 1
    id = store["id"]

    current_time = datetime.datetime.now(datetime.timezone.utc)
    utc_time = current_time.replace(tzinfo=datetime.timezone.utc)
    unix_timestamp = utc_time.timestamp()

    new_message = {
        "message_id": id,
        "u_id": auth_user_id,
        "shared_message_length": 0,
        "message": message,
        "time_sent": int(unix_timestamp),
        "reacts": {1:
            {
                "react_id": 1,
                "u_ids": [],
                "is_this_user_reacted": None,
            }
        },
        "is_pinned": False,
    }

    if -1 in store["messages"].keys():
        store["messages"] = {}
    store["messages"][id] = new_message
    
    store["channels"][channel_id]["message_ids"].append(id)

    src.persistence.set_pickle(store)

    src.notifications.create_tag_notification(auth_user_id, channel_id, message)

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
            (dict): returns an empty dictionary
    '''
    store = src.persistence.get_pickle()

    auth_user_id = src.error_help.check_valid_token(token, store)
    channeldm_id = src.error_help.check_message_id(store, message_id)
    if len(message) > 1000: raise InputError(f"Error: Message over 1000 characters long")
    offset = store['messages'][message_id]['shared_message_length']

    if channeldm_id in store['channels'].keys():
        src.error_help.check_channelmess_perms(store, auth_user_id, channeldm_id, message_id)
        if len(message) == 0:
            store["messages"].pop(message_id)
            store['channels'][channeldm_id]['message_ids'].remove(message_id)
    else:
        src.error_help.check_dmmess_perms(store, auth_user_id, channeldm_id, message_id)
        if len(message) == 0:
            store["messages"].pop(message_id)
            store['dms'][channeldm_id]['message_ids'].remove(message_id)
    
    if len(message) != 0:
        shared_string = store["messages"][message_id]["message"][:offset]
        store["messages"][message_id]["message"] = shared_string + message

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
            (dict): returns an empty dictionary
    '''

    store = src.persistence.get_pickle()

    auth_user_id = src.error_help.check_valid_token(token, store)
    channeldm_id = src.error_help.check_message_id(store, message_id)

    if channeldm_id in store['channels'].keys():
        src.error_help.check_channelmess_perms(store, auth_user_id, channeldm_id, message_id)
        store['channels'][channeldm_id]['message_ids'].remove(message_id)
    else:
        src.error_help.check_dmmess_perms(store, auth_user_id, channeldm_id, message_id)
        store['dms'][channeldm_id]['message_ids'].remove(message_id)
    
    store["messages"].pop(message_id)

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
            (dict): returns a dictionary with 'message_id'
    '''

    store = src.persistence.get_pickle()
    auth_user_id = src.error_help.check_valid_token(token, store)
    
    if dm_id == -1 or dm_id not in store['dms'].keys():
        raise InputError(f"dm_id = {dm_id} is not valid")

    if message == None or len(message) < 1 or len(message) > 1000:
        raise InputError(f"Error: length of message is less than 1 or over 1000 characters")

    if auth_user_id not in store['dms'][dm_id]['member_ids']:
        raise AccessError(f"User is not member of DM")

    store['id'] += 1
    id = store['id']

    if -1 in store['messages'].keys():
        store['dms'][dm_id]['messages'] = {}
    
    current_time = datetime.datetime.now(datetime.timezone.utc)
    utc_time = current_time.replace(tzinfo=datetime.timezone.utc)
    unix_timestamp = utc_time.timestamp()

    new_message = {
        "message_id": id,
        "u_id": auth_user_id,
        "shared_message_length": 0,
        "message": message,
        "time_sent": int(unix_timestamp),
        "reacts": {1:
            {
                "react_id": 1,
                "u_ids": [],
                "is_this_user_reacted": None,
            }
        },
        "is_pinned": False,
    }
    store['messages'][id] = new_message

    store['dms'][dm_id]['message_ids'].append(id)
    
    src.persistence.set_pickle(store)

    src.notifications.create_tag_notification(auth_user_id, dm_id, message)

    return {
        "message_id": id
    }

def message_share_v1(token, og_message_id, message, channel_id, dm_id):
    ''' og_message_id is the ID of the original message. 
        channel_id is the channel that the message is being shared to, 
        and is -1 if it is being sent to a DM. dm_id is the DM that the message is being shared to, 
        and is -1 if it is being sent to a channel. 
        message is the optional message in addition to the shared message, 
        and will be an empty string '' if no message is given.
        
        Arguments:
            token (str) - user authentication number
            og_message_id (int) - identification number for message being shared
            message (str) - extra message that is being sent along with shared message
            channel_id (int) - identification number for channel being sent to
            dm_id (int) - identification number for dm being sent to

        Exceptions:
            InputError - Occurs when:
                - both channel_id and dm_id are invalid
                - neither channel_id nor dm_id are -1
                - og_message_id does not refer to a valid message within a channel/DM that the authorised user has joined
                - length of message is more than 1000 characters

            AccessError - Occurs when:
                - the pair of channel_id and dm_id are valid 
                  (i.e. one is -1, the other is valid) and the authorised user has not joined the channel or DM they are trying to share the message to

        Return Value:
        (dict): returns a dictionary with the shared_message_id
    '''
    store = src.persistence.get_pickle()

    # Authorise user token and message 
    auth_user_id = src.error_help.check_valid_token(token, store)
    channeldm_id = src.error_help.check_message_id(store, og_message_id)

    # Checks and validate channel_id and dm_id input
    if dm_id != -1 and channel_id != -1:
        raise InputError("Neither chanel_id or dm_id is -1")
    elif dm_id == -1 and channel_id == -1:
        raise InputError("Both channel_id and dm_id cannot be -1")
    
    # Check message length
    if len(message) > 1000:
        raise InputError("Length of message over 1000 characters")

    # starts checking the channel/dm message
    if dm_id == -1:
        src.error_help.validate_channel(store, channel_id)
        src.error_help.check_channelmess_perms(store, auth_user_id, channeldm_id, og_message_id)
        
        store["id"] += 1
        id = store["id"]

        current_time = datetime.datetime.now(datetime.timezone.utc)
        utc_time = current_time.replace(tzinfo=datetime.timezone.utc)
        unix_timestamp = utc_time.timestamp()

        new_message = {
            "message_id": id,
            "u_id": auth_user_id,
            "shared_message_length": len(store['messages'][og_message_id]['message']) + SHARED_MSG_OFFSET,
            "message": '"""' + "\n" + store['messages'][og_message_id]['message'] + "\n" + '"""' + "\n" + message,
            "time_sent": int(unix_timestamp),
            "reacts": {1:
                {
                    "react_id": 1,
                    "u_ids": [],
                    "is_this_user_reacted": None,
                }
            },
            "is_pinned": False,
        }

        # if -1 in store["messages"].keys():
        #     store["messages"] = {}
        store["messages"][id] = new_message
        
        store["channels"][channel_id]["message_ids"].append(id)

    elif channel_id == -1:
        src.error_help.validate_dm(store, dm_id)
        src.error_help.check_dmmess_perms(store, auth_user_id, channeldm_id, og_message_id)

        store['id'] += 1
        id = store['id']

        # if -1 in store['messages'].keys():
        #     store['dms'][dm_id]['messages'] = {}
        
        current_time = datetime.datetime.now(datetime.timezone.utc)
        utc_time = current_time.replace(tzinfo=datetime.timezone.utc)
        unix_timestamp = utc_time.timestamp()

        new_message = {
            "message_id": id,
            "u_id": auth_user_id,
            "shared_message_length": len(store['messages'][og_message_id]['message']) + SHARED_MSG_OFFSET,
            "message": '"""' + "\n" + store['messages'][og_message_id]['message'] + "\n" + '"""' + "\n" + message,
            "time_sent": int(unix_timestamp),
            "reacts": {1:
                {
                    "react_id": 1,
                    "u_ids": [],
                    "is_this_user_reacted": None,
                }
            },
            "is_pinned": False,
        }
        store['messages'][id] = new_message

        store['dms'][dm_id]['message_ids'].append(id)
        
    src.persistence.set_pickle(store)
    return {
        "shared_message_id": id
    }

def add_message(auth_user_id, unix_timestamp, channel_id, message, id):    
    store = src.persistence.get_pickle()

    new_message = {
        "message_id": id,
        "u_id": auth_user_id,
        "shared_message_length": 0,
        "message": message,
        "time_sent": int(unix_timestamp),
        "reacts": {1:
            {
                "react_id": 1,
                "u_ids": [],
                "is_this_user_reacted": None,
            }
        },
        "is_pinned": False,
    }

    store["messages"][id] = new_message
    
    store["channels"][channel_id]["message_ids"].append(id)
    src.persistence.set_pickle(store)

def message_sendlater_v1(token, channel_id, message, time_sent):
    ''' Send a message from the authorised user to the channel 
        specified by channel_id automatically at a specified 
        time in the future.

        Arguments:
            token (str) - user authentication number
            channel_id (int) - identification number for channel being sent to
            message (str) - message that is being sent
            time_sent (int: unix timestamp) - time in unix timestamp at which the message will be sent 

        Exceptions:
            InputError - Occurs when:
                - channel_id does not refer to a valid channel
                - length of message is less than 1 or over 1000 characters
                - time_sent is a time in the past

            AccessError - Occurs when:
                - channel_id is valid and the authorised user is not a member of the channel they are trying to post to

        Return Value:
        (dict): returns a dictionary with the message_id
    '''
    store = src.persistence.get_pickle()

    current_time = datetime.datetime.now(datetime.timezone.utc)
    utc_time = current_time.replace(tzinfo=datetime.timezone.utc)
    unix_timestamp = utc_time.timestamp()

    auth_user_id = src.error_help.check_valid_token(token, store)
    src.error_help.validate_channel(store, channel_id)
    src.error_help.auth_user_not_in_channel(store, auth_user_id, channel_id)

    if len(message) > 1000:
        raise InputError("Length of message over 1000 characters")
    if unix_timestamp > time_sent:
        raise InputError("Timestamp cannot be in the past")

    timepass = time_sent - unix_timestamp

    # Grab a new id
    store["id"] += 1
    id = store["id"]

    if -1 in store["messages"].keys():
        store["messages"] = {}

    src.persistence.set_pickle(store)

    t = threading.Timer(timepass, add_message, args = [auth_user_id, time_sent, channel_id, message, id], kwargs = None)
    t.start()

    return {
        "message_id": id
    }
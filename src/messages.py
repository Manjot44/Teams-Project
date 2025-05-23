import src.error_help
from src.error import InputError, AccessError
import datetime
import src.persistence
import src.notifications
import threading

MEMBER = 2
OWNER = 1
SHARED_MSG_OFFSET = 9
CHANNEL_MSG = 3
DM_MSG = 4

def add_message(auth_user_id, unix_timestamp, channeldm_id, message, id, shared_message_length, identifier):    
    store = src.persistence.get_pickle()

    new_message = {
        "message_id": id,
        "u_id": auth_user_id,
        "shared_message_length": shared_message_length,
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

    if identifier == CHANNEL_MSG:
        store["channels"][channeldm_id]["message_ids"].append(id)
    elif identifier == DM_MSG:
        store['dms'][channeldm_id]['message_ids'].append(id)

    src.persistence.set_pickle(store)
    src.notifications.create_tag_notification(auth_user_id, channeldm_id, message)

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
    src.error_help.check_empty_message(message)  
    src.error_help.auth_user_not_in_channel(store, auth_user_id, channel_id)

    store["id"] += 1
    id = store["id"]

    if -1 in store["messages"].keys():
        store["messages"] = {}

    current_time = datetime.datetime.now(datetime.timezone.utc)
    utc_time = current_time.replace(tzinfo=datetime.timezone.utc)
    unix_timestamp = utc_time.timestamp()

    src.persistence.set_pickle(store)
    add_message(auth_user_id, unix_timestamp, channel_id, message, id, 0, CHANNEL_MSG)
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
    src.error_help.check_message_length(message)
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
    src.error_help.validate_dm(store, dm_id)
    src.error_help.check_empty_message(message)
    src.error_help.auth_user_not_in_dm(store, auth_user_id, dm_id)

    store['id'] += 1
    id = store['id']

    if -1 in store['messages'].keys():
        store['dms'][dm_id]['messages'] = {}
    
    current_time = datetime.datetime.now(datetime.timezone.utc)
    utc_time = current_time.replace(tzinfo=datetime.timezone.utc)
    unix_timestamp = utc_time.timestamp()

    src.persistence.set_pickle(store)
    add_message(auth_user_id, unix_timestamp, dm_id, message, id, 0, DM_MSG)
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

    auth_user_id = src.error_help.check_valid_token(token, store)
    src.error_help.check_message_id(store, og_message_id)

    if dm_id != -1 and channel_id != -1:
        raise InputError("Neither chanel_id or dm_id is -1")
    elif dm_id == -1 and channel_id == -1:
        raise InputError("Both channel_id and dm_id cannot be -1")
    
    current_time = datetime.datetime.now(datetime.timezone.utc)
    utc_time = current_time.replace(tzinfo=datetime.timezone.utc)
    unix_timestamp = utc_time.timestamp()

    src.error_help.check_message_length(message)
    shared_message_length = len(store['messages'][og_message_id]['message']) + SHARED_MSG_OFFSET
    message = '"""' + "\n" + store['messages'][og_message_id]['message'] + "\n" + '"""' + "\n" + message

    if dm_id == -1:
        src.error_help.validate_channel(store, channel_id)
        src.error_help.auth_user_not_in_channel(store, auth_user_id, channel_id)

        store["id"] += 1
        id = store["id"]

        src.persistence.set_pickle(store)
        add_message(auth_user_id, unix_timestamp, channel_id, message, id, shared_message_length, CHANNEL_MSG)

    elif channel_id == -1:
        src.error_help.validate_dm(store, dm_id)
        src.error_help.auth_user_not_in_dm(store, auth_user_id, dm_id)

        store['id'] += 1
        id = store['id']
        
        src.persistence.set_pickle(store)
        add_message(auth_user_id, unix_timestamp, dm_id, message, id, shared_message_length, DM_MSG)

    return {
        "shared_message_id": id
    }

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

    src.error_help.check_message_length(message)
    src.error_help.check_valid_time(unix_timestamp, time_sent)

    store["id"] += 1
    id = store["id"]

    if -1 in store["messages"].keys():
        store["messages"] = {}

    src.persistence.set_pickle(store)

    t = threading.Timer(time_sent - unix_timestamp, add_message, args = [auth_user_id, time_sent, channel_id, message, id, 0, CHANNEL_MSG], kwargs = None)
    t.start()

    return {
        "message_id": id
    }

def message_sendlaterdm_v1(token, dm_id, message, time_sent):
    ''' Send a message from the authorised user to the DM specified 
        by dm_id automatically at a specified time in the future
    
        Arguments:
            token (str) - user authentication number
            dm_id (int) - identification number for DM being sent to
            message (str) - message that is being sent
            time_sent (int: unix timestamp) - time in unix timestamp at which the message will be sent 

        Exceptions:
            InputError - Occurs when:
                - dm_id does not refer to a valid DM
                - length of message is less than 1 or over 1000 characters
                - time_sent is a time in the past

            AccessError - Occurs when:
                - dm_id is valid and the authorised user is not a member of the DM they are trying to post to

        Return Value:
        (dict): returns a dictionary with the message_id
    '''
    store = src.persistence.get_pickle()

    current_time = datetime.datetime.now(datetime.timezone.utc)
    utc_time = current_time.replace(tzinfo=datetime.timezone.utc)
    unix_timestamp = utc_time.timestamp()

    auth_user_id = src.error_help.check_valid_token(token, store)
    src.error_help.validate_dm(store, dm_id)
    src.error_help.auth_user_not_in_dm(store, auth_user_id, dm_id)

    src.error_help.check_message_length(message)
    src.error_help.check_valid_time(unix_timestamp, time_sent)

    store["id"] += 1
    id = store["id"]

    if -1 in store["messages"].keys():
        store["messages"] = {}

    src.persistence.set_pickle(store)

    t = threading.Timer(time_sent - unix_timestamp, add_message, args = [auth_user_id, time_sent, dm_id, message, id, 0, DM_MSG], kwargs = None)
    t.start()

    return {
        "message_id": id
    }

def message_react_v1(token, message_id, react_id):
    '''Given a message within a channel or DM the authorised user is part of, add a "react" to that particular message.
    
        Arguments:
            token (str) - user authentication string
            message_id (int) - message that is being reacted to
            react_id (int) - type of reaction

        Exceptions:
            InputError - Occurs when:
                - message_id is not a valid message within a channel or DM that the authorised user has joined
                - react_id is not a valid react ID
                - the message already contains a react with ID react_id from the authorised user

        Return Value:
        (dict): returns an empty dictionary      
    '''
    store = src.persistence.get_pickle()

    auth_user_id = src.error_help.check_valid_token(token, store)
    channeldm_id = src.error_help.check_message_id(store, message_id)
    src.error_help.user_not_in_channeldm(store, auth_user_id, channeldm_id)

    if react_id != 1:
        raise InputError(f"Invalid react_id")
    if auth_user_id in store["messages"][message_id]["reacts"][react_id]["u_ids"]:
        raise InputError(f"You have already reacted to this message")
    
    if react_id not in store["messages"][message_id]["reacts"]:
        store["messages"][message_id]["reacts"][react_id] = {
            'react_id': react_id,
            'u_ids': [auth_user_id],
            'is_this_user_reacted': None,
        }
    else:
        store["messages"][message_id]["reacts"][react_id]["u_ids"].append(auth_user_id)

    src.persistence.set_pickle(store)
    src.notifications.create_react_notification(auth_user_id, message_id)
    return {}

def message_unreact_v1(token, message_id, react_id):
    '''Given a message within a channel or DM the authorised user is part of, unreact to that particular message.
    
        Arguments:
            token (str) - user authentication string
            message_id (int) - message that is being unreacted to
            react_id (int) - type of reaction

        Exceptions:
            InputError - Occurs when:
                - message_id is not a valid message within a channel or DM that the authorised user has joined
                - react_id is not a valid react ID
                - the message does not contain a react with ID react_id from the authorised user
        Return Value:
        (dict): returns an empty dictionary      
    '''
    store = src.persistence.get_pickle()

    auth_user_id = src.error_help.check_valid_token(token, store)
    channeldm_id = src.error_help.check_message_id(store, message_id)
    src.error_help.user_not_in_channeldm(store, auth_user_id, channeldm_id)
    
    if react_id not in store["messages"][message_id]["reacts"] or react_id == -1:
        raise InputError(f"Invalid react_id")
    if auth_user_id not in store["messages"][message_id]["reacts"][react_id]["u_ids"]:
        raise InputError(f"You have not reacted to this message")

    store["messages"][message_id]["reacts"][react_id]["u_ids"].remove(auth_user_id)
    src.persistence.set_pickle(store)

    return {}

def message_pin_v1(token, message_id):
    '''Given a message within a channel or DM, mark it as "pinned".

        Arguments:
            token (str) - user authentication string
            message_id (int) - message that is being pinned 

        Exceptions:
            InputError - Occurs when:
                - message_id is not a valid message within a channel or DM that the authorised user has joined
                - the message is already pinned

            AccessError - Occurs when:
                - message_id refers to a valid message in a joined channel/DM and the authorised user does not have owner permissions in the channel/DM

        Return Value:
        (dict): returns an empty dictionary      
    '''
    store = src.persistence.get_pickle()

    auth_user_id = src.error_help.check_valid_token(token, store)
    channeldm_id = src.error_help.check_message_id(store, message_id)
    src.error_help.user_not_in_channeldm(store, auth_user_id, channeldm_id)
    
    if store["messages"][message_id]["is_pinned"] == True:
        raise InputError(f"This message is already pinned")
    for channel in store['channels'].values():
        if message_id in channel['message_ids']:
            if auth_user_id in channel["owner_ids"]:
                store["messages"][message_id]["is_pinned"] = True
                src.persistence.set_pickle(store)
                return {}
    for dm in store['dms'].values():
        if message_id in dm['message_ids']:
            if auth_user_id == dm["creator_id"]:
                store["messages"][message_id]["is_pinned"] = True
                src.persistence.set_pickle(store)
                return {}

    raise AccessError(f"You are not an owner of the dm/channel")

def message_unpin_v1(token, message_id):
    '''Given a message within a channel or DM, remove its mark as pinned.

        Arguments:
            token (str) - user authentication string
            message_id (int) - message that is being pinned 

        Exceptions:
            InputError - Occurs when:
                - message_id is not a valid message within a channel or DM that the authorised user has joined
                - the message is not already pinned

            AccessError - Occurs when:
                - message_id refers to a valid message in a joined channel/DM and the authorised user does not have owner permissions in the channel/DM

        Return Value:
        (dict): returns an empty dictionary      
    '''
    store = src.persistence.get_pickle()

    auth_user_id = src.error_help.check_valid_token(token, store)
    channeldm_id = src.error_help.check_message_id(store, message_id)
    src.error_help.user_not_in_channeldm(store, auth_user_id, channeldm_id)
    
    if store["messages"][message_id]["is_pinned"] == False:
        raise InputError(f"This message is not pinned")
    for channel in store['channels'].values():
        if message_id in channel['message_ids']:
            if auth_user_id in channel["owner_ids"]:
                store["messages"][message_id]["is_pinned"] = False
                src.persistence.set_pickle(store)
                return {}
    for dm in store['dms'].values():
        if message_id in dm['message_ids']:
            if auth_user_id == dm["creator_id"]:
                store["messages"][message_id]["is_pinned"] = False
                src.persistence.set_pickle(store)
                return {}

    raise AccessError(f"You are not an owner of the dm/channel")

        
        
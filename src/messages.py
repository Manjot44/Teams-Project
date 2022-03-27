from src.data_store import data_store
import src.error_help
from src.error import InputError, AccessError
import datetime

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
    store = data_store.get()
    
    auth_user_id = src.error_help.check_valid_token(token, store)
    src.error_help.validate_channel(store, channel_id)
    if message == None or len(message) < 1 or len(message) > 1000:
        raise InputError(f"Error: length of message is less than 1 or over 1000 characters")
    src.error_help.user_not_in_channel(store, auth_user_id, channel_id)

    channel_mess_id = store["messages"][-1]["message_id"]
    if channel_mess_id == None:
        store["messages"] = []
        channel_mess_id = -1
    
    dm_message_id = -1
    for dms in store["dms"]:
        if (dms["messages"][-1]["message_id"] != None) and (dms["messages"][-1]["message_id"] > dm_message_id):
            dm_message_id = dms['messages'][-1]["message_id"]
    
    if dm_message_id > channel_mess_id:
        id = dm_message_id + 1
    else:
        id = channel_mess_id + 1

    
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
    store = data_store.get()

    # Validify token/user_id
    auth_user_id = src.error_help.check_valid_token(token, store)

    # Validify message_id
    valid_messageid = False
    for messages in store["messages"]:
        if messages["message_id"] == message_id:
            valid_messageid = True
    if valid_messageid == False:
        raise InputError(f"Error: Message_id not valid")

    # Check if authorised user is allowed to edit message once their token has been validified
    if store["messages"][message_id]["u_id"] != auth_user_id and store["users"][auth_user_id]["perm_id"] == 2:
        raise AccessError(f"Error: Forbidden from editing message")

    # Ensure that the length of the edited message is > 0 and <= 1000 characters before its edited. If 0 characters long, message_id will be deleted
    if len(message) == 0:
        del store["messages"][message_id]
    elif len(message) > 1000:
        raise InputError(f"Error: Message over 1000 characters long")
    else:
        store["messages"][message_id]["message"] = message

    data_store.set(store)
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

    store = data_store.get()

    # Validify token/user_id
    auth_user_id = src.error_help.check_valid_token(token, store)

    # Validify message_id
    valid_messageid = False
    for messages in store["messages"]:
        if messages["message_id"] == message_id:
            valid_messageid = True
    if valid_messageid == False:
        raise InputError(f"Error: Message_id not valid")

    # Check if authorised user is allowed to delete message once their token has been validified
    if store["messages"][message_id]["u_id"] != auth_user_id and store["users"][auth_user_id]["perm_id"] == 2:
        raise AccessError(f"Error: Forbidden from editing message")

    del store["messages"][message_id]

    data_store.set(store)
    return {
    }

def message_senddm_v1(token, dm_id, message):
    ''' DOCSTRING '''
    # Checks if token is valid
    store = data_store.get()
    auth_user_id = src.error_help.check_valid_token(token, store)
    # Checks if dm_id is valid
    if store['dms'][0]['dm_id'] == None:
        raise InputError(f"dm_id is not valid because there are no DMs")
    valid_dm = False
    dm_index = 0
    for dm in store['dms']:
        if dm['dm_id'] == dm_id:
            valid_dm = True
            break
        dm_index += 1
    if valid_dm == False:
        raise InputError(f"dm_id = {dm_id} is not valid")
    # Checks if message is valid
    if message == None or len(message) < 1 or len(message) > 1000:
        raise InputError(f"Error: length of message is less than 1 or over 1000 characters")
    # Checks if user is in dm
    valid_member = False
    member_index = 0
    for members in store['dms'][dm_index]['all_members']:
        if members['u_id'] == auth_user_id:
            valid_member = True
            break
        member_index += 1
    if valid_member == False:
        raise AccessError(f"User is not member of DM")

    if store["dms"][dm_index]["messages"][0]["message_id"] == None:
        store["dms"][dm_index]["messages"] = []

    # Assigning unique message_id
    channel_mess_id = store["messages"][-1]["message_id"]
    if channel_mess_id == None:
        channel_mess_id = -1
    
    dm_message_id = -1
    for dms in store["dms"]:
        if (dms["messages"] != []) and (dms["messages"][-1]["message_id"] > dm_message_id):
            dm_message_id = dms['messages'][-1]["message_id"]
    
    if dm_message_id > channel_mess_id:
        id = dm_message_id + 1
    else:
        id = channel_mess_id + 1

    
    current_time = datetime.datetime.now(datetime.timezone.utc)
    utc_time = current_time.replace(tzinfo=datetime.timezone.utc)
    unix_timestamp = utc_time.timestamp()

    new_message = {
        "message_id": id,
        "u_id": auth_user_id,
        "message": message,
        "time_sent": int(unix_timestamp),
    }


    store['dms'][dm_index]['messages'].append(new_message)
    data_store.set(store)

    return {
        "message_id": id
    }

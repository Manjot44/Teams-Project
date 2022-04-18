import src.persistence
import src.error_help

def initialise_notif(channeldm_id, store):
    '''Initialises the notification dictionary with channel id and dm id

    Arguments:
        channeldm_id (int) - the id of the channel/dm,
        store (dict) - all stored data

    Exceptions:
        N/A

    Return Value:
        (tuple): returns the notifications dicitonary and the channel/dm name
    '''
    new_notif = {
        'channel_id': None,
        'dm_id': None,
        'notification_message': None,
    }
    name = None
    if channeldm_id in store['channels'].keys():
        new_notif['channel_id'] = channeldm_id
        new_notif['dm_id'] = -1
        name = store['channels'][channeldm_id]['name']
    else:
        new_notif['dm_id'] = channeldm_id
        new_notif['channel_id'] = -1
        name = store['dms'][channeldm_id]['name']
    
    return [new_notif, name]


def check_in_channeldm(store, new_notif, valid_id):
    '''Checks if a valid user is a part of the relevant channel/dm of the notification

    Arguments:
        store (dict) - all stored data,
        new_notif (dict) - dictionary with notification details (channel and dm id at this stage),
        valid_id (int) - the id of a registered user

    Exceptions:
        N/A

    Return Value:
        (int): returns the user id of the user with the valid handle or -1 if invalid
    '''
    if new_notif['channel_id'] == -1:
        dm_id = new_notif['dm_id']
        if valid_id not in store['dms'][dm_id]['member_ids']:
            valid_id = -1
    else:
        channel_id = new_notif['channel_id']
        if valid_id not in store['channels'][channel_id]['member_ids']:
            valid_id = -1

    return valid_id


def find_valid_handle(message, new_notif, store):
    '''Finds a handle in a specified message and checks the validity of the handle
    Also checks if the user with the handle found is in the relevant channel/dm

    Arguments:
        message (str) - message that has been sent,
        new_notif (dict) - dictionary with notification details (channel and dm id at this stage),
        store (dict) - all stored data

    Exceptions:
        N/A

    Return Value:
        (int): returns the user id of the user with the valid handle or -1 if invalid
    '''
    handle = ""
    for char in message:
        if char.isalnum():
            handle += char
        else:
            break
    
    valid_id = -1
    for user in store['users'].values():
        if user['handle_str'] == handle:
            valid_id = user['u_id']

    valid_id = check_in_channeldm(store, new_notif, valid_id)

    return valid_id   


def create_add_notification(auth_user_id, channeldm_id, u_id):
    '''Creates a notification when someone has been invited/added to a channel/dm

    Arguments:
        auth_user_id (int) - user id of the person adding,
        channeldm_id (int) - the id of the channel/dm the person user is getting added to,
        u_id (int) - user id of person being added

    Exceptions:
        N/A

    Return Value:
        (void): no return
    '''
    store = src.persistence.get_pickle()
    new_notif, name = initialise_notif(channeldm_id, store)
    
    new_notif['notification_message'] = f"{store['users'][auth_user_id]['handle_str']} added you to {name}"
    
    if store['users'][u_id]['notifications'][0]['channel_id'] == None:
        store['users'][u_id]['notifications'] = []
    store['users'][u_id]['notifications'].append(new_notif)

    src.persistence.set_pickle(store)

    return


def create_tag_notification(auth_user_id, channeldm_id, message):
    '''Creates a notification if a registered user has been tagged in a message 
    in a channel/dm the registered user is in

    Arguments:
        auth_user_id (int) - user id of the sender,
        channeldm_id (int) - the id of the channel/dm the message was sent to,
        message (str) - message that has been sent

    Exceptions:
        N/A

    Return Value:
        (void): no return
    '''
    store = src.persistence.get_pickle()

    new_notif, name = initialise_notif(channeldm_id, store)

    valid_ids = []
    for idx, char in enumerate(message):
        if char == "@":
            id = find_valid_handle(message[idx + 1:], new_notif, store)
            if id != -1 and id not in valid_ids:
                valid_ids.append(id)

    message = message[:20]
    new_notif['notification_message'] = f"{store['users'][auth_user_id]['handle_str']} tagged you in {name}: {message}"

    for u_id in valid_ids:
        if store['users'][u_id]['notifications'][0]['channel_id'] == None:
            store['users'][u_id]['notifications'] = []
        store['users'][u_id]['notifications'].append(new_notif)
    
    src.persistence.set_pickle(store)

    return


def create_react_notification(auth_user_id, message_id):
    '''Creates a notification if someone has reacted to a message in a channel/dm
    that the sender is still in

    Arguments:
        auth_user_id (int) - user id of the 'reactor',
        message_id (int) - id of the message that has been reacted to

    Exceptions:
        N/A

    Return Value:
        (void): no return
    '''
    store = src.persistence.get_pickle()

    u_id = store['messages'][message_id]['u_id']
    channeldm_id = src.error_help.check_message_id(store, message_id)

    new_notif, name = initialise_notif(channeldm_id, store)
    
    valid_id = check_in_channeldm(store, new_notif, u_id)
    if valid_id == -1:
        return

    new_notif['notification_message'] = f"{store['users'][auth_user_id]['handle_str']} reacted to your message in {name}"

    if store['users'][u_id]['notifications'][0]['channel_id'] == None:
        store['users'][u_id]['notifications'] = []
    store['users'][u_id]['notifications'].append(new_notif)

    src.persistence.set_pickle(store)

    return


def notifications_get(token):
    '''Return the user's most recent 20 notifications, ordered from most recent to least recent.

    Arguments:
        token (str) - jwt passed in

    Exceptions:
        AccessError - Occurs when:
            token passed in is not valid

    Return Value:
        (dict): returns a dictionary containing channel_id, dm_id, and notification message
    '''
    store = src.persistence.get_pickle()
    
    auth_user_id = src.error_help.check_valid_token(token, store)

    if store['users'][auth_user_id]['notifications'][0]['channel_id'] == None:
        store['users'][auth_user_id]['notifications'] = []
    notifications = store['users'][auth_user_id]['notifications']
    notifications.reverse()
    notifications = notifications[:20]

    return {
        'notifications': notifications
    }

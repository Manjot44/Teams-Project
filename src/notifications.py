import src.persistence
import src.error_help

def initialise_notif(channeldm_id, store):
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
    if new_notif['channel_id'] == -1:
        dm_id = new_notif['dm_id']
        if valid_id not in store['dms'][dm_id]['member_ids']:
            valid_id = False
    else:
        channel_id = new_notif['channel_id']
        if valid_id not in store['channels'][channel_id]['member_ids']:
            valid_id = False

    return valid_id


def find_valid_handle(message, new_notif, store):
    handle = ""
    for char in message:
        if char.isalnum():
            handle += char
        else:
            break
    
    valid_id = False
    for user in store['users'].values():
        if user['handle_str'] == handle:
            valid_id = user['u_id']

    valid_id = check_in_channeldm(store, new_notif, valid_id)

    return valid_id   


def create_add_notification(auth_user_id, channeldm_id, u_id):
    store = src.persistence.get_pickle()
    new_notif, name = initialise_notif(channeldm_id, store)
    
    new_notif['notification_message'] = f"{store['users'][auth_user_id]['handle_str']} added you to {name}"
    
    if store['users'][u_id]['notifications'][0]['channel_id'] == None:
        store['users'][u_id]['notifications'] = []
    store['users'][u_id]['notifications'].append(new_notif)

    src.persistence.set_pickle(store)

    return


def create_tag_notification(auth_user_id, channeldm_id, message):
    store = src.persistence.get_pickle()

    new_notif, name = initialise_notif(channeldm_id, store)

    valid_ids = []
    for idx, char in enumerate(message):
        if char == "@":
            id = find_valid_handle(message[idx + 1:], new_notif, store)
            if id != False and id not in valid_ids:
                valid_ids.append(id)

    message = message[:20]
    new_notif['notification_message'] = f"{store['users'][auth_user_id]['handle_str']} tagged you in {name}: {message}"

    for u_id in valid_ids:
        if store['users'][u_id]['notifications'][0]['channel_id'] == None:
            store['users'][u_id]['notifications'] = []
        store['users'][u_id]['notifications'].append(new_notif)
    
    src.persistence.set_pickle(store)

    return


def create_react_notification(auth_user_id, message_id): #check if the user is still in the channel
    store = src.persistence.get_pickle()

    u_id = store['messages'][message_id]['u_id']
    channeldm_id = src.error_help.check_message_id(store, message_id)

    new_notif, name = initialise_notif(channeldm_id, store)
    
    valid_id = check_in_channeldm(store, new_notif, u_id)
    if valid_id == False:
        return

    new_notif['notification_message'] = f"{store['users'][auth_user_id]['handle_str']} reacted to your message in {name}"

    if store['users'][u_id]['notifications'][0]['channel_id'] == None:
        store['users'][u_id]['notifications'] = []
    store['users'][u_id]['notifications'].append(new_notif)

    src.persistence.set_pickle(store)

    return


def notifications_get(token):
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

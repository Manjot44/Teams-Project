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


def find_handle(message, store):
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

    return valid_id   


def create_add_notification(auth_user_id, channeldm_id, u_id):
    store = src.persistence.get_pickle()
    new_notif, name = initialise_notif(channeldm_id, store)
    
    new_notif['notification_message'] = f"{store['users'][auth_user_id]['handle_str']} added you to {name}"
    
    if store['users'][u_id]['notifications']['channel_id'] == None:
        store['users'][u_id]['notifications'] = []
    store['users'][u_id]['notifications'].append(new_notif)

    src.persistence.set_pickle(store)

    return


def create_tag_notification(auth_user_id, channeldm_id, message, u_id):
    store = src.persistence.get_pickle()

    valid_ids = []
    for idx, char in enumerate(message):
        if char == "@":
            id = find_handle(message[idx + 1:], store)
            if valid_ids != False and id not in valid_ids:
                valid_ids.append(id)

    new_notif, name = initialise_notif(channeldm_id, store)
    message = message[:20]
    new_notif['notification_message'] = f"{store['users'][auth_user_id]['handle_str']} tagged you in {name}: {message}"

    for u_id in valid_ids:
        if store['users'][u_id]['notifications']['channel_id'] == None:
            store['users'][u_id]['notifications'] = []
        store['users'][u_id]['notifications'].append(new_notif)
    
    src.persistence.set_pickle(store)

    return

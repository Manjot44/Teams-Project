from src.data_store import data_store
from src.error import InputError, AccessError
from src.error_help import check_valid_id, check_valid_token

OWNER = 1
MEMBER = 2

def admin_userpermission_change(token, u_id, permission_id):
    ''' Given a user by their user ID, set their permissions to new 
        permissions described by permission_id.

        Arguments:
            token (str) - token string (for user that is changing permission)
            u_id (int) - user authentication id number (of user whos perm_id is being changed)
            permission_id (int) - permission identification number

        Exceptions:
            InputError  - Occurs when:
                u_id does not refer to a valid user
                u_id refers to a user who is the only global owner and they are being demoted to a user
                permission_id is invalid
                the user already has the permissions level of permission_id

            AccessError - Occurs when:
                the authorised user is not a global owner

        Return Value:
            Returns {}
    '''
    store = data_store.get()

    auth_user = check_valid_token(token, store)
    check_valid_id(u_id, store)

    if permission_id != OWNER and permission_id != MEMBER:
        raise InputError(f"Error: {permission_id} invalid permission id, permission id must either be 1 or 2.")
    if permission_id == store['users'][u_id]['perm_id']:
        raise InputError(f"Error: Perm_id already set to {permission_id}")
    if store['users'][auth_user]['perm_id'] == MEMBER:
        raise AccessError(f"Error: {auth_user} is not a global owner")
    

    if permission_id == OWNER and store['users'][u_id]['perm_id'] == MEMBER:
        store['users'][u_id]['perm_id'] = permission_id
    if permission_id == MEMBER and store['users'][u_id]['perm_id'] == OWNER:
        
        global_count = 0
        for user in store['users'].values():
            if user['perm_id'] == OWNER:
                global_count += 1
        
        if global_count > 1:
            store['users'][u_id]['perm_id'] = permission_id
        else:
            raise InputError(f"Error: Need to at least have one one global owner")

    data_store.set(store)
    return {
    }

def admin_user_remove(token, u_id):
    ''' Given a user by their u_id, remove them from the Seams. 
        This means they should be removed from all channels/DMs, and will not be included in the list of users returned by users/all. 
        Seams owners can remove other Seams owners (including the original first owner). 
        Once users are removed, the contents of the messages they sent will be replaced by 'Removed user'. 
        Their profile must still be retrievable with user/profile, however name_first should be 'Removed' and name_last should be 'user'. 
        The user's email and handle should be reusable.

        Arguments:
            token (str) - token string (for user that removing other user)
            u_id (int) - user authentication id number (for user that is being removed)

        Exceptions:
            InputError  - Occurs when:
                u_id does not refer to a valid user
                u_id refers to a user who is the only global owner

            AccessError - Occurs when:
                the authorised user is not a global owner

        Return Value:
            Returns {}
    '''
    store = data_store.get()

    auth_user = check_valid_token(token, store)
    check_valid_id(u_id, store)

    if store['users'][auth_user]['perm_id'] == MEMBER:
        raise AccessError(f"Error: {auth_user} is not a global owner")

    global_count = 0
    for user in store['users'].values():
        if user['perm_id'] == OWNER:
            global_count += 1
    if global_count == 1 and store["users"][u_id]["perm_id"] == OWNER:
        raise InputError(f"Error: Need to at least have one one global owner")
    
    if None in store["removed_users"].keys():
        store['removed_users'] = {}
    add_removed_user = {
        'u_id': u_id,
        'email': None,
        'name_first': 'Removed',
        'name_last': 'user',
        'handle_str': None,
    }
    store["removed_users"][u_id] = add_removed_user
    
    store["users"].pop(u_id)

    for channel in store["channels"].values():
        if u_id in channel["all_members"].keys():
            channel["all_members"].pop(u_id)
        if u_id in channel["owner_members"].keys():
            channel["owner_members"].pop(u_id)
                
    for dm in store["dms"].values():
        if u_id in dm["all_members"].keys():
            dm["all_members"].pop(u_id)

    for dm_message in store["dm_messages"].values():
        if dm_message["u_id"] == u_id:
            dm_message["message"] = 'Removed user'

    for msg in store["channel_messages"].values():
        if msg["u_id"] == u_id:
            msg["message"] = 'Removed user'
    
    data_store.set(store)
    return {
    }
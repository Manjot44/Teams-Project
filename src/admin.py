from src.data_store import data_store
from src.error import InputError, AccessError
from src.error_help import check_valid_id, check_valid_token

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
    check_valid_id(auth_user, store)

    # Check for Errors
    if permission_id < 1 or permission_id > 2:
        raise InputError(f"Error: {permission_id} invalid permission id, permission id must either be 1 or 2.")
    if permission_id == store['users'][u_id]['perm_id']:
        raise InputError(f"Error: Perm_id already set to {permission_id}")
    if store['users'][auth_user]['perm_id'] == 2:
        raise AccessError(f"Error: {auth_user} is not a global owner")
    
    # Change the perm_id of u_id
    if permission_id == 1 and store['users'][u_id]['perm_id'] == 2:
        store['users'][u_id]['perm_id'] = permission_id
    if permission_id == 2 and store['users'][u_id]['perm_id'] == 1:
        
        # Count how many global owners there are
        global_count = 0
        for user in store['users']:
            if user['perm_id'] == 1:
                global_count += 1
        # Ensure that there is at least 1 global owner in Seams
        if global_count > 1:
            store['users'][u_id]['perm_id'] = permission_id
        else:
            raise InputError(f"Error: Need to at least have one one global owner")

    data_store.set(store)
    return {
    }

# Prevents a 'removed user' from being added to the removed_user list twice
def check_removed_user_in_list(u_id, data_store):
    has_removed_user = False
    for removed_user in data_store["removed_users"]:
        if removed_user["u_id"] == u_id:
            has_removed_user = True

    return has_removed_user

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

    # Check if auth_user_id and u_id are valid
    auth_user = check_valid_token(token, store)
    check_valid_id(u_id, store)
    check_valid_id(auth_user, store)

    # AccessError if auth_user is not a global owner
    if store['users'][auth_user]['perm_id'] == 2:
        raise AccessError(f"Error: {auth_user} is not a global owner")

    # Ensures that there is at least one global owner
    global_count = 0
    if store['users'][auth_user]['perm_id'] == 1:
        for user in store['users']:
            if user['perm_id'] == 1:
                global_count += 1
    if global_count == 1:
        raise InputError(f"Error: Need to at least have one one global owner")

    # Remove from channel
    for channel in store["channels"]:
        for user in channel["all_members"]:
            if user["u_id"] == u_id:
                del user

                add_removed_user = {
                    'u_id': u_id,
                    'email': None,
                    'name_first': 'Removed',
                    'name_last': 'user',
                    'handle_str': None,
                }
                
                has_removed_user = check_removed_user_in_list(u_id, store)
                if has_removed_user == False:
                    store["removed_users"].append(add_removed_user)
        
        for user1 in channel["owner_members"]: # meant to remove from both the all_members and owner_members list 
            if user1["u_id"] == u_id:
                del user1
                
                add_removed_user = {
                    'u_id': u_id,
                    'email': None,
                    'name_first': 'Removed',
                    'name_last': 'user',
                    'handle_str': None,
                }
                
                has_removed_user = check_removed_user_in_list(u_id, store)
                if has_removed_user == False:
                    store["removed_users"].append(add_removed_user)
            
    # Remove from DM
    for dm in store["dms"]:
        for user_dm in dm["all_members"]:
            if user_dm["u_id"] == u_id:
                del user_dm 

                add_removed_user = {
                    'u_id': u_id,
                    'email': None,
                    'name_first': 'Removed',
                    'name_last': 'user',
                    'handle_str': None,
                }
                
                has_removed_user = check_removed_user_in_list(u_id, store)
                if has_removed_user == False:
                    store["removed_users"].append(add_removed_user)
        
        for user_dm1 in dm["owner_members"]:
            if user_dm1["u_id"] == u_id:
                del user_dm1
        
                add_removed_user = {
                    'u_id': u_id,
                    'email': None,
                    'name_first': 'Removed',
                    'name_last': 'user',
                    'handle_str': None,
                }
                
                has_removed_user = check_removed_user_in_list(u_id, store)
                if has_removed_user == False:
                    store["removed_users"].append(add_removed_user)

        # Replace all dms sent with "Replace user"
        for dm_message in dm["messages"]:
            if dm_message["u_id"] == u_id:
                dm_message["message"] = 'Removed user'

    # Remove Channel messages 
    for msg in store["messages"]:
        if msg["u_id"] == u_id:
            msg["message"] = 'Removed user'

    data_store.set(store)
    return {
    }
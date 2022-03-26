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
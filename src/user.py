from operator import contains
from src import auth, channel, channels, error, other
from src.data_store import data_store
from src.channels import channels_create_v1
from src.error import InputError, AccessError
from src.error_help import check_valid_token, check_valid_id
import re

def user_profile_v1(token, u_id):
    '''For a valid user, returns information about their user_id, email, first name,
    last name, and handle.

    Arguments:
        token (str) - user authentication
        u_id (int) - user identification number

    Exceptions:
        InputError - Occurs when:
            - when u_id does not refer to a valid user
        AccessError - Occurs when:
            - token passed in is not valid

    Return Value:
        Returns {
            'user': { u_id, email, name_first, name_last, handle_str, profile_img_url },
        }
    
    '''

    store = data_store.get()
    
    check_valid_token(token, store)

    valid_u_id = "invalid"
    if u_id in store["users"].keys() and u_id != None:
        valid_u_id = "valid_user"
    if u_id in store["removed_users"].keys() and u_id != None:
        valid_u_id = "valid_removed_user"

    if valid_u_id == "invalid":
        raise InputError(f"u_id does not refer to a valid user")
 
    user_info_dict = {
        'user': {}
    }
    
    if valid_u_id == "valid_user":
        user_info_dict['user'] = {k: store["users"][u_id][k] for k in ('u_id', 'email', 'name_first', 'name_last', 'handle_str')}
    elif valid_u_id == "valid_removed_user":
        user_info_dict['user'] = {k: store["removed_users"][u_id][k] for k in ('u_id', 'email', 'name_first', 'name_last', 'handle_str')}
        
    return user_info_dict
                
def user_profile_setname_v1(token, name_first, name_last):
    '''Update the authorised user's first and last name.

    Arguments:
        token (str) - user authentication
        name_first (str) - first name to be changed to
        name_last (str) - last name to be changed to

    Exceptions:
        InputError - Occurs when:
            - when length of name_first is not between 1 and 50 characters (incl.)
            - when length of name_last is not between 1 and 50 characters (incl.)
        AccessError - Occurs when:
            - token passed in is not valid

    Return Value:
        Returns {}
    
    '''

    store = data_store.get()
    u_id = check_valid_token(token, store)

    if len(name_first) > 50 or len(name_first) < 1:
            raise InputError(f"length of name_first is not between 1 and 50 characters inclusive")
    if len(name_last) > 50 or len(name_last) < 1:
        raise InputError(f"length of name_last is not between 1 and 50 characters inclusive") 
     
    store['users'][u_id]['name_first'] = name_first
    store['users'][u_id]['name_last'] = name_last

    return {
    }

def user_profile_setemail_v1(token, email):
    '''Update the authorised user's email address.

    Arguments:
        token (str) - user authentication
        email (str) - email to be changed to

    Exceptions:
        InputError - Occurs when:
            - when email entered is not valid email
            - when email address is already being used by another user
        AccessError - Occurs when:
            - token passed in is not valid

    Return Value:
        Returns {}
    
    '''

    store = data_store.get()

    u_id = check_valid_token(token, store)

    for user in store['users'].values():
        if user['email'] == email and user['u_id'] != u_id:
            raise InputError(f"email address is already being used by another user")

    regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
    if not (re.search(regex, email)):
        raise InputError(f"Error: email entered is not valid")
    
    store['users'][u_id]['email'] = email

    return {
    }    

def user_profile_sethandle_v1(token, handle_str):
    '''Update the authorised user's handle (i.e. display name).

    Arguments:
        token (str) - user authentication
        handle_str (str) - handle to be changed to

    Exceptions:
        InputError - Occurs when:
            - when length of handle_str is not between 3 and 20 characters (incl.)
            - when handle_str contains characters that are not alphanumeric
            - when handle is already used by another user
        AccessError - Occurs when:
            - token passed in is not valid

    Return Value:
        Returns {}
    
    '''

    store = data_store.get()

    u_id = check_valid_token(token, store)

    if len(handle_str) > 20 or len(handle_str) < 3:
        raise InputError(f"length of handle_str is not between 3 and 20 characters inclusive")
    
    if not handle_str.isalnum():
        raise InputError(f"handle_str contains characters that are not alphanumeric")

    for user in store['users'].values():
        if user['handle_str'] == handle_str and user['u_id'] != u_id:
            raise InputError(f"the handle is already used by another user")

    store['users'][u_id]['handle_str'] = handle_str
    
    return {
    }

def users_all_v1(token):
    '''Returns all authorised users.

    Arguments:
        token (str) - user authentication

    Exceptions:
        AccessError - Occurs when:
            - token passed in is not valid

    Return Value:
        Returns {
            'users': [],
        }
    '''
    store = data_store.get()
    
    check_valid_token(token, store)
    
    users_all = {
        'users': []
    }

    for user in store['users'].values():
        if user['u_id'] != None:
            new_append = {k:user[k] for k in ('u_id', 'email', 'name_first', 'name_last', 'handle_str')}
            users_all['users'].append(new_append)

    return users_all

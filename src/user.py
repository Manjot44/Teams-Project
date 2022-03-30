from operator import contains
from src import auth, channel, channels, error, other
from src.data_store import data_store
from src.channels import channels_create_v1
from src.error import InputError, AccessError
from src.error_help import check_valid_token, check_valid_id
import re

def user_profile_v1(token, u_id):
    store = data_store.get()
    
    valid_u_id = "invalid"
    
    u_id_check = store['users']
    for user in u_id_check:
        if user['u_id'] == u_id:
            valid_u_id = "valid_user"
    
    removed_u_id_check = store['removed_users']
    for user in removed_u_id_check:
        if user['u_id'] == u_id:
            valid_u_id = "valid_removed_user"
    if valid_u_id == "invalid":
        raise InputError(f"u_id does not refer to a valid user")

    check_valid_token(token, store)
          
    user_info_dict = {}
    user_info_dict['user'] = {}
    user_info = store['users']
    removed_user_info = store['removed_users']
    if valid_u_id == "valid_user":
        for user in user_info:
            if user['u_id'] == u_id:  
                user_info_dict['user']['u_id'] = user['u_id']
                user_info_dict['user']['email'] = user['email']
                user_info_dict['user']['name_first'] = user['name_first']
                user_info_dict['user']['name_last'] = user['name_last']
                user_info_dict['user']['handle_str'] = user['handle_str']
    elif valid_u_id == "valid_removed_user":
        for user in removed_user_info:
            if user['u_id'] == u_id:  
                user_info_dict['user']['u_id'] = user['u_id']
                user_info_dict['user']['email'] = user['email']
                user_info_dict['user']['name_first'] = user['name_first']
                user_info_dict['user']['name_last'] = user['name_last']
                user_info_dict['user']['handle_str'] = user['handle_str']
    
    return user_info_dict

def user_profile_setname_v1(token, name_first, name_last):
    store = data_store.get()

    if len(name_first) > 50 or len(name_first) < 1:
            raise InputError(f"length of name_first is not between 1 and 50 characters inclusive")
    if len(name_last) > 50 or len(name_last) < 1:
        raise InputError(f"length of name_last is not between 1 and 50 characters inclusive")
    
    u_id = check_valid_token(token, store)
     
    user_info = store['users']
    for user in user_info:
        if user['u_id'] == u_id:
            user['name_first'] = name_first
            user['name_last'] = name_last       
    return {
    }

def user_profile_setemail_v1(token, email):
    store = data_store.get()

    user_info = store['users']
    for user in user_info:
        if user['email'] == email:
            raise InputError(f"email address is already being used by another user")

    valid_email = True
    regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
    if not re.match(regex, email):
        valid_email = False
    if valid_email == False:
        raise InputError(f"email entered is not a valid email ")

    u_id = check_valid_token(token, store)
    
    user_info = store['users']
    for user in user_info:
        if user['u_id'] == u_id:
            user['email'] = email
    return {
    }    

def user_profile_sethandle_v1(token, handle_str):
    store = data_store.get()

    if len(handle_str) > 20 or len(handle_str) < 3:
        raise InputError(f"length of handle_str is not between 3 and 20 characters inclusive")
    
    if not handle_str.isalnum():
        raise InputError(f"handle_str contains characters that are not alphanumeric")

    user_info = store['users']
    for user in user_info:
        if user['handle_str'] == handle_str:
            raise InputError(f"the handle is already used by another user")
    
    u_id = check_valid_token(token, store) 

    user_info = store['users']
    for user in user_info:
        if user['u_id'] == u_id:
            user['handle_str'] = handle_str
    return {
    }

def users_all_v1(token):
    '''Returns all authorised users.

    Arguments:
        token (str) - user authentication

    Exceptions:
        AccessError - Occurs when:
            token passed in is not valid

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
    for users in store['users']:
        user_dict = {
            'u_id': None,
            'email': None,
            'name_first': None,
            'name_last': None,
            'handle_str': None,
        }
        if users['u_id'] != None:
            user_dict['u_id'] = users['u_id']
            user_dict['email'] = users['email']
            user_dict['name_first'] = users['name_first']
            user_dict['name_last'] = users['name_last']
            user_dict['handle_str'] = users['handle_str']
            users_all['users'].append(user_dict)

    return users_all

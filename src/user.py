from operator import contains
from src import auth, channel, channels, error, other
from src.data_store import data_store
from src.channels import channels_create_v1
from src.error import InputError, AccessError
from src.error_help import check_valid_token, check_valid_id
import re

def user_profile_v1(token, u_id):
    store = data_store.get()
    
    valid_u_id = 0
    u_id_check = store['users']
    for user in u_id_check:
        if user['u_id'] == u_id:
            valid_u_id = 1

    if valid_u_id == 0:
        raise InputError

    u_id = check_valid_token(token, store)
          
    user_info_dict = {}
    user_info_dict['user'] = {}
    user_info = store['users']
    for user in user_info:
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
            raise InputError
    if len(name_last) > 50 or len(name_last) < 1:
        raise InputError
    
    u_id = check_valid_token(token, store)
     
    user_info = store['users']
    for user in user_info:
        if user['u_id'] == u_id:
            user['name_first'] = name_first
            user['name_last'] = name_last       
        return    

def user_profile_setemail_v1(token, email):
    store = data_store.get()

    user_info = store['users']
    for user in user_info:
        if user['email'] == email:
            raise InputError 

    valid_email = True
    regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
    if not re.match(regex, email):
        valid_email = False
    if valid_email == False:
        raise InputError

    u_id = check_valid_token(token, store)
    
    user_info = store['users']
    for user in user_info:
        if user['u_id'] == u_id:
            user['email'] = email
        return    

def user_profile_sethandle_v1(token, handle_str):
    store = data_store.get()

    if len(handle_str) > 20 or len(handle_str) < 3:
        raise InputError
    
    if not handle_str.isalnum():
        raise InputError

    user_info = store['users']
    for user in user_info:
        if user['handle_str'] == handle_str:
            raise InputError 
    
    u_id = check_valid_token(token, store) 

    user_info = store['users']
    for user in user_info:
        if user['u_id'] == u_id:
            user['handle_str'] = handle_str
        return   
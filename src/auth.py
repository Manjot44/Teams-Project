from src.error import InputError
import hashlib
import re
import jwt
import src.error_help
import src.persistence
import flask_mail
from src.server import MAIL

SECRET = 'jroilin'
OWNER = 1
MEMBER = 2

def auth_login_v1(email, password):
    '''Given a registered user's email and password, returns their 'auth_user_id' value and a new 'token'.

    Arguments:
        email (str) - inputted email,
        password (str) - inputted Password

    Exceptions:
        InputError - Occurs when:
            email entered does not belong to a user,
            password is not correct

    Return Value:
        (dict): returns a dictionary with the auth_user_id and the unique token for the current session
    '''

    store = src.persistence.get_pickle()
    
    valid_email = False
    u_id = 0
    for user in store["users"].items():
        if user[1]["email"] == email and email != None:
            valid_email = True
            u_id = user[0]
    if valid_email == False:
        raise InputError(f"Error: email does not belong to a user")
    
    user = store["users"][u_id]
    if user["password"] != hashlib.sha256(password.encode()).hexdigest():
        raise InputError(f"Error: password is incorrect")
    
    store["users"][u_id]["session_id"] += 1
    session_id = store["users"][u_id]["session_id"]
    encoded_jwt = jwt.encode({'handle_str': user["handle_str"], "session_id": session_id}, SECRET, algorithm='HS256')
    user["valid_tokens"].append(encoded_jwt)
    
    src.persistence.set_pickle(store)

    return {
        "auth_user_id": u_id,
        "token": encoded_jwt,
    }



def generate_handle(name_first, name_last):
    '''Given a first name and last name, generates a unique handle for the user

    Arguments:
        name_first (str) - inputted first name,
        name_last (str) - inputted last name
    
    Exceptions:
        N/A
    
    Return Value:
        (str): returns the unique handle
    '''

    store = src.persistence.get_pickle()

    alpha_nfirst = ''.join(filter(str.isalnum, name_first))
    alpha_nlast = ''.join(filter(str.isalnum, name_last))
    alpha_nfirst += alpha_nlast
    alpha_nfirst = alpha_nfirst.lower()
    handle = alpha_nfirst[:20]

    same_handle = -1
    for user in store["users"].values():
        if user["handle_str"] == handle:
            same_handle += 1
            if same_handle == 0:
                handle += str(same_handle)
            else:
                handle = handle[:-1] + str(same_handle)
    
    return handle



def auth_register_v1(email, password, name_first, name_last):
    '''Given a user's first and last name, email address, and password, create a new account for them and
    return a new 'auth_user_id' and 'token'.

    Arguments:
        email (str) - inputted email,
        password (str) - inputted password,
        name_first (str) - inputted first name,
        name_last (str) - inputted last name

    Exceptions:
        InputError  - Occurs when:
            email entered is not a valid email,
            email address is already being used by another user,
            length of password is less than 6 characters,
            length of name_first is not between 1 and 50 characters inclusive,
            length of name_last is not between 1 and 50 characters inclusive

    Return Value:
        (dict): returns a dictionary with the auth_user_id and the unique token for the current session 
    '''
    
    store = src.persistence.get_pickle()
    
    regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
    if not (re.search(regex, email)):
        raise InputError(f"Error: email entered is not valid")

    for user in store["users"].values():
        if user["email"] == email:
            raise InputError(f"Error: email address is already being used by another user")

    if len(password) < 6:
        raise InputError(f"Error: password must be at least 6 characters long")
    
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError(f"Error: first name must be between 1 and 50 characters long inclusive")
    
    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError(f"Error: last name must be between 1 and 50 characters long inclusive")

    handle = generate_handle(name_first, name_last)
    
    store["id"] += 1
    id = store["id"] 
    perm_id = MEMBER
    if id == 0:
        perm_id = OWNER
    encoded_jwt = jwt.encode({'handle_str': handle, 'session_id': 0}, SECRET, algorithm='HS256')

    new_user = {
        "u_id": id,
        "email": email,
        "password": hashlib.sha256(password.encode()).hexdigest(),
        "name_first": name_first,
        "name_last": name_last,
        "handle_str": handle,
        "perm_id": perm_id,
        "valid_tokens": [encoded_jwt],
        "profile_img_url": None,
        "notifications": [
            {
            "channel_id": None,
            "dm_id": None,
            "notification_message": None,
            }
        ],
        "reset_codes": [],
        "session_id": 0,
        "reset_id": -1,
    }

    if -1 in store["users"].keys():
        store["users"] = {}
    store["users"][id] = new_user
    
    src.persistence.set_pickle(store)

    return {
        "auth_user_id": id,
        "token": encoded_jwt,
    }



def auth_logout_v1(token):
    '''Given an active token, invalidates the token to log the user out.

    Arguments:
        token (str) - jwt passed in

    Exceptions:
        AccessError - Occurs when:
            token passed in is not valid

    Return Value:
        (dict): returns an empty dictionary
    '''
    store = src.persistence.get_pickle()
    
    auth_user_id = src.error_help.check_valid_token(token, store)
    store["users"][auth_user_id]["valid_tokens"].remove(token)
    
    if store["users"][auth_user_id]["valid_tokens"] == []:
        store["users"][auth_user_id]["session_id"] = -1

    src.persistence.set_pickle(store)

    return {
    }



def auth_passwordreset_request(email):
    store = src.persistence.get_pickle()

    valid_email_uid = src.error_help.check_valid_email(store, email)
    if valid_email_uid == -1:
       print("this should not be happening")
       return {}
    
    store['users'][valid_email_uid]['reset_id'] += 1
    reset_id = store['users'][valid_email_uid]['reset_id']

    encoded_jwt = jwt.encode({'email': email, 'reset_id': reset_id}, SECRET, algorithm='HS256')
    store['users'][valid_email_uid]['reset_codes'].append(encoded_jwt)

    msg = flask_mail.Message('Password Reset Code', recipients = [email])
    
    msg.body = (
        f"Hey {store['users'][valid_email_uid]['handle_str']},\n\n"
        "This is your password reset code:\n"
        f"{encoded_jwt}\n\n"
        "Kind Regards,\n"
        "Microsoft Seams Team"        
    )

    MAIL.send(msg)
    print("sending complete")
    
    src.persistence.set_pickle(store)

    return {}

def auth_passwordreset_reset(reset_code, new_password):
    store = src.persistence.get_pickle()

    auth_user_id = src.error_help.check_valid_reset_code(store, reset_code)
    if len(new_password) < 6:
        raise InputError(f"Error: password must be at least 6 characters long")

    store['users'][auth_user_id]['password'] = hashlib.sha256(new_password.encode()).hexdigest()
    store['users'][auth_user_id]['reset_codes'].remove(reset_code)
    if store['users'][auth_user_id]['reset_codes'] == []:
        store['users'][auth_user_id]['reset_id'] = -1
    
    src.persistence.set_pickle(store)

    return {}

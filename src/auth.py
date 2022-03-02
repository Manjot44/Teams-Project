from src.data_store import data_store
from src.error import InputError

def auth_login_v1(email, password):
    store = data_store.get()
    
    valid_email = 0
    nth_user = 0
    for idx, user in enumerate(store["users"]):
        if user["email"] == email:
            valid_email = 1
            nth_user = idx
            break

    if valid_email == 0:
        raise InputError()
    
    if store["users"][nth_user]["password"] != password:
        raise InputError()
    
    id = store["users"][nth_user]["id"]

    return id 

def auth_register_v1(email, password, name_first, name_last):
    return {
        'auth_user_id': 1,
    }

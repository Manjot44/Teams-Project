import re
from webbrowser import get
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
        raise InputError(f"Error: email does not belong to a user")
    
    if store["users"][nth_user]["password"] != password:
        raise InputError(f"Error: password is incorrect")
    
    id = store["users"][nth_user]["u_id"]

    return id 

def auth_register_v1(email, password, name_first, name_last):
    store = data_store.get()
    
    regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
    if not (re.search(regex, email)):
        raise InputError(f"Error: email entered is not valid")

    for user in store["users"]:
        if user["email"] == email:
            raise InputError(f"Error: email address is already being used by another user")

    if len(password) < 6:
        raise InputError(f"Error: password must be at least 6 characters long")
    
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError(f"Error: first name must be between 1 and 50 characters long inclusive")
    
    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError(f"Error: last name must be between 1 and 50 characters long inclusive")

    alpha_nfirst = ''.join(filter(str.isalnum, name_first))
    alpha_nlast = ''.join(filter(str.isalnum, name_last))
    alpha_nfirst += alpha_nlast
    alpha_nfirst = alpha_nfirst.lower()
    handle = alpha_nfirst[:20]

    store = data_store.get()
    same_handle = 0
    for user in store["users"]:
        if user["handle_str"] == handle:
            same_handle += 1
        
    handle += str(same_handle)
    id = len(store["users"])

    new_user = {
        "email": email,
        "password": password,
        "name_first": name_first,
        "name_last": name_last,
        "handle_str": handle,
        "u_id": id,
    }
    store["users"].append(new_user)

    data_store.set(store)

    return id
import re
from webbrowser import get
from src.data_store import data_store
from src.error import InputError

def auth_login_v1(email, password):
    return {
        'auth_user_id': 1,
    }

def auth_register_v1(email, password, name_first, name_last):
    regex = '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
    if not (re.search(regex, email)):
        raise InputError()

    if len(password) < 6:
        raise InputError()
    
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError()
    
    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError()

    alpha_nfirst = ''.join(filter(str.isalnum, name_first))
    alpha_nlast = ''.join(filter(str.isalnum, name_last))
    alpha_nfirst += alpha_nlast
    alpha_nfirst = alpha_nfirst.lower()
    handle = alpha_nfirst[:20]

    store = data_store.get()
    same_handle = 0
    for user in store["users"]:
        if user["handle"] == handle:
            same_handle += 1
        
    handle += str(same_handle)
    id = len(store["users"])

    new_user = {
        "email": email,
        "password": password,
        "handle": handle,
        "id": id,
    }
    store["users"].append(new_user)

    data_store.set(store)

    return id

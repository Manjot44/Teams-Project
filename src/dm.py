from src.data_store import data_store
from src.error import InputError, AccessError
from src.error_help import check_valid_id, validate_channel, check_channel_priv, check_channel_user, user_not_in_channel, check_valid_token


def dm_create_v1(token, u_ids):
    '''Creates a new dm with the given user list.
    The user who created it automatically joins the channel.

    Arguments:
        token (str) - user authentication
        u_ids (list of ints) - list of users to be added to dm

    Exceptions:
        InputError - Occurs when:
            - any u_id in u_ids does not refer to a valid user
            - there are duplicate 'u_id's in u_ids
        AccessError - Occurs when:
            token passed in is not valid

    Return Value:
        Returns {
            'dm_id': dm_id,
        }
    '''
    # Getting Data from data storage file
    store = data_store.get()

    # Checking valid token and ids
    check_valid_token(token, store)
    if u_ids == []:
        raise InputError(f"Error: Enter a valid ID")
    for u_id in u_ids:
        check_valid_id(u_id, store)

    # Checking for duplicates
    if(len(set(u_ids)) != len(u_ids)):
        raise InputError(f"Duplicate users in u_ids list")

    # Assigning new dm details
    dm_id = len(store["dms"]) - 1
    user_handles = []
    user_details_list = []

    # Append the creators handle and save owner info
    for user in store["users"]:
        for token_check in user["valid_tokens"]:
            if(token_check == token):
                user_handles.append(user["handle_str"])
                owner_details = user
                user_details_list.append(user)

    # Append all u_id handles and save user info
    for u_id in u_ids:
        for user in store["users"]:
            if(user['u_id'] == u_id):
                user_handles.append(user["handle_str"])
                user_details_list.append(user)

    # Sort and join to create dm name
    alph_handle = sorted(user_handles)
    joined_name = ", ".join([str(item) for item in alph_handle])

    # Creating new dm
    new_dm = {
        "dm_id": dm_id,
        "name": joined_name,
        "owner_members": [owner_details],
        "all_members": user_details_list,
        "messages": [
            {
                'message_id': None,
                'u_id': None,
                'message': None,
                'time_sent': None,
            },
        ]
    }

    # Saving to datastore
    store["dms"].append(new_dm)
    data_store.set(store)

    return {
        'dm_id': dm_id,
    }


def dm_list_v1(u_id):
    '''Provide a list of all dms that the authorised user is part of.

    Arguments:
        token (string) - user authentication

    Exceptions:
        AccessError - Occurs when:
            token passed in is not valid

    Return Value:
        Returns {
            'dm_id': dm_id (int)
            'namme': name (string)
        }
    '''

    # Getting Data from data storage file
    store = data_store.get()

    dm_list = []

    for dm in store["dms"]:
        for dm_user in dm["all_members"]:
            if dm_user["u_id"] == u_id:
                dm_list.append({
                    'dm_id': dm['dm_id'],
                    'name': dm['name']
                })

    return dm_list


def dm_remove_v1(u_id, dm_id):
    '''Remove an existing DM, so all members are no longer in the DM. 
    This can only be done by the original creator of the DM.

    Arguments:
        u_id (int) - user authentication int
        dm_id (ints) - dm identification number

    Exceptions:
        InputError - Occurs when:
            - dm_id does not refer to a valid DM
        AccessError - Occurs when:
            - token is not valid
            - dm_id is valid and the authorised user is not the original DM creator
            - dm_id is valid and the authorised user is no longer in the DM

    Return Value:
        Returns {}
    '''

# Getting Data from data storage file
    store = data_store.get()

    valid_dm_id = False
    for dm in store["dms"]:
        if dm["dm_id"] == dm_id:
            valid_dm_id = True
    if valid_dm_id == False:
        raise InputError(f"dm_id is not valid")

    dm_member = False
    for user in store["dms"][dm_id + 1]["all_members"]:
        if user["u_id"] == u_id:
            dm_member = True
    if dm_member == False:
        raise AccessError(f"You are not part of this dm")

    if u_id != store["dms"][dm_id + 1]["owner_members"][0]["u_id"]:
        raise AccessError(f"Only the original creator can remove a dm")

    del store["dms"][dm_id + 1]

    # Saving to datastore
    data_store.set(store)

    return

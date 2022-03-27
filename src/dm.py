from src.data_store import data_store
from src.error import InputError, AccessError
from src.error_help import check_valid_id, validate_channel, check_channel_priv, check_channel_user, user_not_in_channel, check_valid_token
from src.other import clear_v1


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
    if store["dms"][0]["dm_id"] == None:
        store["dms"] = []
    dm_id = len(store["dms"])
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
    for user in store["dms"][dm_id]["all_members"]:
        if user["u_id"] == u_id:
            dm_member = True
    if dm_member == False:
        raise AccessError(f"You are not part of this dm")

    if u_id != store["dms"][dm_id]["owner_members"][0]["u_id"]:
        raise AccessError(f"Only the original creator can remove a dm")

    if dm_id == 0:
        store['dms'] = [
            {
                'dm_id': None,
                'name': None,
                'owner_members': [
                    {
                        'u_id': None,
                        'email': None,
                        'name_first': None,
                        'name_last': None,
                        'handle_str': None,
                    }
                ],
                'all_members': [
                    {
                        'u_id': None,
                        'email': None,
                        'name_first': None,
                        'name_last': None,
                        'handle_str': None,
                    }
                ],
                'messages': [
                    {
                        'message_id': None,
                        'u_id': None,
                        'message': None,
                        'time_sent': None,
                    },
                ]
            }
        ]
    else:
        del store["dms"][dm_id]

    # Saving to datastore
    data_store.set(store)

    return

def dm_leave_v1(token, dm_id):
    '''User in DM is removed from members list.

    Arguments:
        token (string) - user authentication
        dm_id (int) - dm that is specified

    Exceptions:
        AccessError - Occurs when:
            token passed in is not valid
        InputError - Occurs when:
            dm_id passed is not valid
        AccessError - Occurs when:
            user is not member of DM

    '''
    store = data_store.get()
    # Checks if token is valid
    leaver_id = check_valid_token(token, store)
    # Checks if dm_id is valid
    if store['dms'][0]['dm_id'] == None:
        raise InputError(f"dm_id is not valid because there are no DMs")
    valid_dm = False
    dm_index = 0
    for dm in store['dms']:
        if dm['dm_id'] == dm_id:
            valid_dm = True
            break
        dm_index += 1
    if valid_dm == False:
        raise InputError(f"dm_id = {dm_id} is not valid")
    # Checks if user is member of DM
    valid_member = False
    member_index = 0
    for members in store['dms'][dm_index]['all_members']:
        if members['u_id'] == leaver_id:
            valid_member = True
            break
        member_index += 1
    if valid_member == False:
        raise AccessError(f"User is not member of DM")
    # User is verified member from this point on
    # Check if member is owner member
    valid_owner = False
    owner_index = 0
    for members in store['dms'][dm_index]['owner_members']:
        if members['u_id'] == leaver_id:
            valid_owner = True
            break
        owner_index += 1
    # Removing leaver from member lists
    if valid_owner == True:
        store['dms'][dm_index]['owner_members'].remove(store['dms'][dm_index]['all_members'][owner_index])
    store['dms'][dm_index]['all_members'].remove(store['dms'][dm_index]['all_members'][member_index])
    return {}


def dm_details_v1(u_id, dm_id):
    '''Given a DM with ID dm_id that the authorised user is a member of, 
    provide basic details about the DM.

    Arguments:
        u_id (int) - user authentication int
        dm_id (ints) - dm identification number

    Exceptions:
        InputError - Occurs when:
            - dm_id does not refer to a valid DM
        AccessError - Occurs when:
            - dm_id is valid and the authorised user is not a member of the DM

    Return Value:
        Returns {
            'name': name
            'members': [
                {
                    'u_id': None,
                    'email': None,
                    'name_first': None,
                    'name_last': None,
                    'handle_str': None,
                }
            ]
        }
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
    for user in store["dms"][dm_id]["all_members"]:
        if user["u_id"] == u_id:
            dm_member = True
    if dm_member == False:
        raise AccessError(f"You are not part of this dm")

    return {
        "name": store["dms"][dm_id]["name"],
        "members": store["dms"][dm_id]["all_members"]
    }

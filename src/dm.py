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
        (dict): returns a dictionary with the newly created dm_id 
    '''

    store = data_store.get()

    check_valid_token(token, store)
    if u_ids == []:
        raise InputError(f"Error: Enter a valid ID")
    for u_id in u_ids:
        check_valid_id(u_id, store)

    if(len(set(u_ids)) != len(u_ids)):
        raise InputError(f"Duplicate users in u_ids list")

    store["dm_id"] += 1
    dm_id = store["dm_id"]

    if None in store["dms"].keys():
        store["dms"] = {
            }

    user_handles = []
    all_members = {}

    for user in store["users"].items():
        if token in user[1]["valid_tokens"]:
            user_handles.append(user[1]["handle_str"])
            add_owner = {k: user[1][k] for k in ('email', 'name_first', 'name_last', 'handle_str')}
            add_owner["is_creator"] = True
            all_members[user[0]] = add_owner

    for user in store["users"].items():
        if u_id == user[0]:
            user_handles.append(user[1]["handle_str"])
            add_member = {k: user[1][k] for k in ('email', 'name_first', 'name_last', 'handle_str')}
            add_member["is_creator"] = False
            all_members[user[0]] = add_member

    alph_handle = sorted(user_handles)
    joined_name = ", ".join([str(item) for item in alph_handle])

    store["dms"][dm_id] = {
        "name": joined_name,
        "all_members": all_members
    }

    data_store.set(store)

    return {
        'dm_id': dm_id,
    }


def dm_list_v1(token):
    '''Provide a list of all dms that the authorised user is part of.

    Arguments:
        token (string) - user authentication

    Exceptions:
        AccessError - Occurs when:
            token passed in is not valid

    Return Value:
        Returns (dict): returns a dictionary which contains "dms", a list of dictionaries which each contain dm_id(int) and name(string)
    '''

    store = data_store.get()
    dm_list = []
    u_id = check_valid_token(token, store)

    for dm in store["dms"].items():
        if u_id in dm[1]["all_members"]:
            dm_list.append({
                'dm_id': dm[0],
                'name': dm[1]['name']
            })

    return {
        "dms": dm_list
    }

def dm_remove_v1(token, dm_id):
    '''Remove an existing DM, so all members are no longer in the DM. 
    This can only be done by the original creator of the DM.

    Arguments:
        token (str) - user authentication 
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

    store = data_store.get()
    u_id = check_valid_token(token, store)
    if dm_id not in store["dms"]:
        raise InputError(f"dm_id is not valid")

    if u_id not in store["dms"][dm_id]["all_members"]:
        raise AccessError(f"You are not part of this dm")

    if store["dms"][dm_id]["all_members"][u_id]["is_creator"] == False:
        raise AccessError(f"Only the original creator can remove a dm")

    if len(store["dms"]) == 1:
        store['dms'] = {None:
        {
            'name': None,
            'all_members': {None:
                {
                    'email': None,
                    'name_first': None,
                    'name_last': None,
                    'handle_str': None,
                    'is_creator': None,
                }
            }, 
        }
        },
    else:
        store["dms"].pop(dm_id)

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
        store['dms'][dm_index]['owner_members'].remove(store['dms'][dm_index]['owner_members'][owner_index])
    store['dms'][dm_index]['all_members'].remove(store['dms'][dm_index]['all_members'][member_index])
    return {}


def dm_details_v1(token, dm_id):
    '''Given a DM with ID dm_id that the authorised user is a member of, 
    provide basic details about the DM.

    Arguments:
        token (str) - user authentication 
        dm_id (ints) - dm identification number

    Exceptions:
        InputError - Occurs when:
            - dm_id does not refer to a valid DM
        AccessError - Occurs when:
            - dm_id is valid and the authorised user is not a member of the DM

    Return Value:
        Returns (dict): returns a dictionary which contains name(str) and members() of specified dm       
    '''

    store = data_store.get()
    u_id = check_valid_token(token, store)

    if dm_id not in store["dms"]:
        raise InputError(f"dm_id is not valid")

    if u_id not in store["dms"][dm_id]["all_members"]:
        raise AccessError(f"You are not part of this dm")

    members = []
    for member in store["dms"][dm_id]["all_members"].values():
        members.append(member)
    
    #THIS NEEDS TO BE EDITED AFTER USER IS FIXED
    return {
        "name": store["dms"][dm_id]["name"],
        "members": members
    }


def dm_messages_v1(token, dm_id, start):
    ''' DOC STRING ''' # Throw token, dm_id into help function
    
    store = data_store.get()
    # Checks if token is valid
    u_id = check_valid_token(token, store)
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
        if members['u_id'] == u_id:
            valid_member = True
            break
        member_index += 1
    if valid_member == False:
        raise AccessError(f"User is not member of DM")
    # Checks if start is greater than number of messages
    total_message_list = store['dms'][dm_index]['messages']
    if start == None:
        raise InputError(f"Invalid value for 'start' variable")
    if start > len(total_message_list):
        raise InputError(f"Start greater than number of messages in DM.")
    if total_message_list[0]['message_id'] == None:
        if start > 0:
            raise InputError(f"List is empty, start value higher than 0 not valid")

    # Returning messages
    end = start + 50
    messages = {
        'messages': [],
        'start': start,
        'end': end,
    }
    last_idx = len(total_message_list)
    if len(total_message_list[start:last_idx]) <= 50:
        messages['end'] = -1
        messages['messages'] = total_message_list[start:last_idx]
    else:
        messages['messages'] = total_message_list[start:start + 50]

    return messages
    

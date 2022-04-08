from src.error import InputError, AccessError
from src.error_help import check_valid_id, check_valid_token
import src.persistence


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

    store = src.persistence.get_pickle()

    owner_id = check_valid_token(token, store)
    for u_id in u_ids:
        check_valid_id(u_id, store)

    if(len(set(u_ids)) != len(u_ids)):
        raise InputError(f"Duplicate users in u_ids list")

    store["id"] += 1
    dm_id = store["id"]

    if -1 in store["dms"].keys():
        store["dms"] = {}

    u_ids.append(owner_id)
    member_ids = u_ids

    user_handles = []
    for u_id in u_ids:
        user_handles.append(store["users"][u_id]["handle_str"])

    alph_handle = sorted(user_handles)
    joined_name = ", ".join([str(item) for item in alph_handle])

    store["dms"][dm_id] = {
        "dm_id": dm_id,
        "name": joined_name,
        "creator_id": owner_id,
        "member_ids": member_ids,
        "message_ids": []
    }

    src.persistence.set_pickle(store)

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
        (dict): returns a dictionary which contains "dms", a list of dictionaries which each contain dm_id(int) and name(string)
    '''

    store = src.persistence.get_pickle()
    
    u_id = check_valid_token(token, store)

    dm_list = []
    for dm in store["dms"].values():
        if u_id in dm["member_ids"]:
            dm_list.append({
                'dm_id': dm["dm_id"],
                'name': dm['name']
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
        (dict): returns an empty dictionary
    '''

    store = src.persistence.get_pickle()
    u_id = check_valid_token(token, store)
    if dm_id not in store["dms"].keys() or dm_id == -1:
        raise InputError(f"dm_id is not valid")

    if u_id not in store["dms"][dm_id]["member_ids"]:
        raise AccessError(f"You are not part of this dm")

    if u_id != store["dms"][dm_id]["creator_id"] or u_id == None:
        raise AccessError(f"Only the original creator can remove a dm")

    if len(store["dms"]) == 1:
        store['dms'] = {None:
            {
                'dm_id': None,
                'name': None,
                'creator_id': None,
                'member_ids': [],
                'message_ids': [],    
            }
        },
    else:
        store["dms"].pop(dm_id)

    src.persistence.set_pickle(store)
    return


def dm_leave_v1(token, dm_id):
    '''User in DM is removed from members list.

    Arguments:
        token (string) - user authentication
        dm_id (int) - dm that is specified

    Exceptions:
        InputError - Occurs when:
            - dm_id does not refer to a valid DM
        AccessError - Occurs when:
            - dm_id is valid but authorised user is not a member of the DM
            - when token does not refer to authorised user
    Return value:
        Returns {}

    '''
    store = src.persistence.get_pickle()

    leaver_id = check_valid_token(token, store)

    if dm_id == -1 or dm_id not in store['dms'].keys():
        raise InputError(f"dm_id = {dm_id} is not valid")
    
    if leaver_id not in store['dms'][dm_id]['member_ids']:
        raise AccessError(f"User is not member of DM")
    
    dm = store['dms'][dm_id]
    dm['member_ids'].remove(leaver_id)
    if dm['creator_id'] == leaver_id:
        dm['creator_id'] = None

    src.persistence.set_pickle(store)
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
        Returns (dict): returns a dictionary which contains name(str) and members(list) of specified dm       
    '''

    store = src.persistence.get_pickle()
    u_id = check_valid_token(token, store)

    if dm_id == -1 or dm_id not in store["dms"]:
        raise InputError(f"dm_id is not valid")

    if u_id not in store["dms"][dm_id]["member_ids"]:
        raise AccessError(f"You are not part of this dm")

    members = []
    for member in store["dms"][dm_id]["member_ids"]:
        add_new = {k:store['users'][member][k] for k in ('u_id', 'email', 'name_first', 'name_last', 'handle_str', 'profile_img_url')}
        members.append(add_new)
    
    return {
        "name": store["dms"][dm_id]["name"],
        "members": members
    }


def dm_messages_v1(token, dm_id, start):
    '''Returns up to 50 messages in DM for given user and dm_id. 

    Arguments:
        token (str) - user authentication
        dm_id (int) - dm identification number
        start (int) - index number of message

    Exceptions:
        InputError - Occurs when:
            - when dm_id does not refer to valid DM
            - start is greater than total messages in DM
        AccessError - Occurs when:
            - when dm_id is valid but authorised user is not member of DM

    Return Value:
        (dict): returns a dictionary with messages(list of dict), start(int), end(int )
    '''
    
    store = src.persistence.get_pickle()
    u_id = check_valid_token(token, store)

    if dm_id == -1 or dm_id not in store['dms'].keys():
        raise InputError(f"dm_id = {dm_id} is not valid")

    if u_id not in store['dms'][dm_id]['member_ids']:
        raise AccessError(f"User is not member of DM")
    
    if start == None or start > len(store['dms'][dm_id]['message_ids']):
        raise InputError(f"Start greater than number of messages in DM.")

    end = start + 50
    messages = {
        'messages': [],
        'start': start,
        'end': end,
    }
    for message_id in store['dms'][dm_id]['message_ids']:
        messages['messages'].append(store['messages'][message_id])
    messages['messages'].reverse()

    if len(messages['messages']) <= 50:
        messages['end'] = -1
        messages['messages'] = messages['messages'][start:]
    else:
        messages['messages'] = messages['messages'][start:start + 50]

    return messages

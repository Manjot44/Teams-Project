from src.data_store import data_store
from src import auth, channel, channels, error, other

def channel_invite_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_details_v1(auth_user_id, channel_id):
    # dictionary that is to be returned with function
    details = {
        'name': None,
        'is_public': None,
        'owner_members': [],
        'all_members': [],
    }
    #                           AUTHENTICATION
    # validate auth user id
    saved_data = data_store.get()
    valid_user = False
    for user in saved_data['users']:
        if auth_user_id == user['u_id']:
            valid_user = True
    if valid_user == False:
        raise error.AccessError()   # error as user id is not valid

    # validate channel id
    valid_channel = False
    for channel in saved_data['channels']:
        if channel_id == channel['channel_id']:
            selected_channel = channel
            valid_channel = True
    if valid_channel == False:
        raise error.InputError()   # error as channel id is not valid

    # validate user is member of channel
    is_member = False
    for members in saved_data['channels'][channel_id - 1]['all_members']:
        if auth_user_id == members:
            is_member = True
            break
    if is_member != True:
        raise error.AccessError()   # error as user is valid but not a member of channel

    # configuring 'name' key
    details['name'] = saved_data['users'][auth_user_id]['name_first']
    
    # configuring 'is_public' key
    public = saved_data['channels'][channel_id - 1]['is_public']
    details['is_public'] = public

    # configuring 'owner_members' key
    saved_owners = saved_data['channels'][channel_id - 1]['owner_members']
    saved_users = saved_data['users']
    for owner_ids in saved_owners:
        details['owner_members'].append({
            'u_id': saved_users[owner_ids]['u_id'],
            'email': saved_users[owner_ids]['email'],
            'name_first': saved_users[owner_ids]['name_first'],
            'name_last': saved_users[owner_ids]['name_last'],
            'handle_str': saved_users[owner_ids]['handle_str'],
        })

    # configuring 'all_members' key
    saved_members = saved_data['channels'][channel_id - 1]['all_members']
    for member_ids in saved_members:
        details['all_members'].append({
            'u_id': saved_users[member_ids]['u_id'],
            'email': saved_users[member_ids]['email'],
            'name_first': saved_users[member_ids]['name_first'],
            'name_last': saved_users[member_ids]['name_last'],
            'handle_str': saved_users[member_ids]['handle_str'],
        })

    return details

    '''
    return {
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'email': 'example@gmail.com',
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
                'handle_str': 'haydenjacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'email': 'example@gmail.com',
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
                'handle_str': 'haydenjacobs',
            }
        ],
    }
    '''

def channel_messages_v1(auth_user_id, channel_id, start):

    store = data_store.get()

    is_user_valid = False
    for user in store['users']:
        if auth_user_id == user['u_id']:
            is_user_valid = True
            break

    if is_user_valid == False:
        raise error.AccessError(f"invalid user")

    channel_id_valid = False
    store_channel = 0
    for idx, valid_id in enumerate(store['channels']):
        
        if channel_id == valid_id['channel_id']:        
            channel_id_valid = True
            store_channel = idx
            break

    if channel_id_valid == False: 
        raise error.InputError(f"Invalid channel id")  

    valid_member = False

    for member in store['channels'][channel_id - 1]['all_members']:
        if auth_user_id == member:
            valid_member = True
            break

    if valid_member == False:
        raise error.AccessError(f"member is not part of the channel")

    messagesreturn = {
        'messages': [],
        'start': start, 
        'end': start + 50
    }
    
    messages = store['channels'][store_channel]['messages']

    if start > len(messages):
        raise error.InputError(f"start must be smaller than total amount of messages")

    if start + 50 > len(messages):
        messagesreturn['end'] = -1
        messagesreturn['messages'] = messages
    else:
        messagesreturn['messages'] = messages[:50]

    return messagesreturn        

def channel_join_v1(auth_user_id, channel_id):
    return {
    }

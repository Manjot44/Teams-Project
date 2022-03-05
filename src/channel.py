import data_store

def channel_invite_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_details_v1(auth_user_id, channel_id):
    # dictionary that is to be returned with function
    details = {
        'name': None,
        'owner_members': [],
        'all_members': [],
    }
    #                           AUTHENTICATION
    # validate auth user id
    saved_data = data_store.get()
    valid_user = False
    for user in saved_data['users']['u_id']:
        if auth_user_id == user:
            valid_user = True
    if valid_user == False:
        raise error.AccessError()   # error as user id is not valid

    # validate channel id
    valid_channel = False
    for channel in saved_data['channels']['channel_id']:
        if channel_id == channel:
            selected_channel = channel
            valid_channel = True
    if valid_channel == False:
        raise error.AccessError()   # error as channel id is not valid

    # validate user is member of channel
    is_member = False
    for members in saved_data['channels'][channel_id - 1]['members']['all_members']:
        if auth_user_id == members:
            is_member = True
    if is_member != True:
        raise error.AccessError()   # error as user is valid but not a member of channel

    # configuring 'name' key
    details['name'] = saved_data['users'][auth_user_id]['name_first']
    
    # configuring 'owner_members' key
    saved_owners = saved_data['channels'][channel_id - 1]['members']['owner_members']
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
    saved_members = saved_data['channels'][channel_id - 1]['members']['all_members']
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
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }

def channel_join_v1(auth_user_id, channel_id):
    return {
    }

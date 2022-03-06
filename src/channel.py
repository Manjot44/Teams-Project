from src.data_store import data_store
from src import auth, channel, channels, error, other
from src.data_store import data_store
from src.channels import channels_create_v1
from src.error import InputError, AccessError

def channel_invite_v1(auth_user_id, channel_id, u_id):
    store = data_store.get()

    # Checks if the auth_user_id is valid
    has_auth_user = 0
    for auth_user in store["users"]:
        if auth_user["u_id"] == auth_user_id:
            has_auth_user = 1
    if has_auth_user == 0:
        raise AccessError('Error: auth_user does not have a valid ID')

    # Checks if u_id is valid 
    has_u_id = 0
    for u_user in store["users"]:
        if u_user["u_id"] == u_id:
            has_u_id = 1
    if has_u_id == 0:
        raise InputError('Error: User does not have a valid ID')

    # Raise InputError if channel_id does not refer to valid channel
    # Loop through existing channels to see if any of them have the same ID as 'channel_id'
    channel_valid = 0
    for channel in store["channels"]:
        if channel["channel_id"] == channel_id:
            channel_valid = 1
    if channel_valid == 0:
        raise InputError('Error: Channel ID does not refer to a valid channel')

    # Checks if auth_user is in the channel of channel_id
    in_channel = 0
    check_user = store["channels"][channel_id - 1]["members"]["all_members"]
    for check in check_user:
        if check == auth_user_id:
            in_channel = 1
            break
    if in_channel == 0:
        raise AccessError('Error: user that is not in a specific channel cannot add other users to that channel')

    # Checks if u_id is in the channel 
    users = store["channels"][channel_id - 1]["members"]["all_members"]
    for user in users:
        if user == u_id:
            raise InputError(f"Error: user is already member of the channel")

    
    # Once the above functions run and confirm that the auth_user is in channel and that u_id valid, u_id will be added to channel 
    users.append(u_id)
    data_store.set(store)
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
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_sent': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }

def channel_join_v1(auth_user_id, channel_id):
    store = data_store.get()

    # Checks if the auth_user_id is valid
    has_auth_user = 0
    for auth_user in store["users"]:
        if auth_user["u_id"] == auth_user_id:
            has_auth_user = 1
    if has_auth_user == 0:
        raise InputError('Error: User does not have a valid ID')

    # Raise InputError if channel_id does not refer to valid channel
    # Loop through existing channels to see if any of them have the same ID as 'channel_id'
    channel_valid = 0
    for channel in store["channels"]:
        if channel["channel_id"] == channel_id:
            channel_valid = 1
    if channel_valid == 0:
        raise InputError('Error: Channel ID does not refer to a valid channel')
    
    # AccessError if the channel user is trying to join is private
    if store["channels"][channel_id - 1]["ispublic"] == False:
        raise AccessError('Error: Cannot join private channel without being invited')

    # Checks if authorised user is already part of the channel by looping through the channel users
    users = store["channels"][channel_id - 1]["members"]["all_members"]
    for user in users:
        if user == auth_user_id:
            raise InputError('Error: User is already member of the channel')
    
    # Once confirmed that user is not in channel, user will be added
    users.append(auth_user_id)
    data_store.set(store)

    return {
    }

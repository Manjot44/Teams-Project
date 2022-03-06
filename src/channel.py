from src.data_store import data_store
from src import auth, channel, channels, error, other

# from src.error import AccessError, InputError
# from src.data_store import data_store
# from src.auth import auth_register_v1
# from src.channels import channels_create_v1

def channel_invite_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_details_v1(auth_user_id, channel_id):
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

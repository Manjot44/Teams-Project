from src.error import AccessError, InputError
from src.data_store import data_store
from src.auth import auth_register_v1
from src.channels import channels_create_v1

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
    # return {
    #     'messages': [
    #         {
    #             'message_id': 1,
    #             'u_id': 1,
    #             'message': 'Hello world',
    #             'time_created': 1582426789,
    #         }
    #     ],
    #     'start': 0,
    #     'end': 50,
    # }

    store = data_store.get()
    # start = int(start)

    messagesreturn = {
        'messages': [],
        'start': start, 
        'end': start + 50
    }
    
    # 1. Access the channel
    # 2. Test if channel_id is valid
    # 3. Assign all the messages is the channel to 'messages'
    # 4. Tests if start value is valid (must be less than the amount of messages)
    # 5. If 'start + 50' is larger than len(messages) ---> end = -1
    # 6. Run through all the messages and ensure there a no messages (iteration 1 requirement)
    # Notice: Also have to make sure the user is a member of the channel

    channel_id_valid = False
    valid_member = False

    for valid_id in enumerate(store['channels']):
        
        if channel_id == store['channels'][valid_id]['channel_id']:        
            channel_id_valid = True
            
        if auth_user_id == store['channels'][channel_id - 1]['members'][0]:
            valid_member = True
            messages = store['channels']['messages']

            if start > len(messages):
                raise(InputError)

            if start + 50 > len(messages):
                messagesreturn['end'] = -1

        for message_amount in store['channels']['messages']:
            if message_amount < len(messages):
                messagesreturn['messages'].append(messages)
            else:
                return messagesreturn        

    if channel_id_valid == False: 
        raise InputError("Invalid channel id")        
    if valid_member == False:
             raise(AccessError)
        
    # for data in store['channel']:
        
    #     messages = c['messages']

    #     if start > len(messages):
    #         raise InputError("start is larger than messages")
    
    # return {
    #     'messages': [
    #         {
    #             'message_id': 1,
    #             'u_id': 1,
    #             'message': 'Hello world',
    #             'time_created': 1582426789,
    #         }
    #     ],
    #     'start': 0,
    #     'end': 50,
    # }

    # channel_id = 1
    # if channel_id != 10:
    #     raise InputError("channel_id is invalid")

    # auth_user_id = 1
    # if auth_user_id != 10:
    #     raise AccessError("invalid user id")

    # if start > len(messagesreturn["messages"]):
    #     raise InputError("start should not be greater than the amount of messages"

def channel_join_v1(auth_user_id, channel_id):
    return {
    }

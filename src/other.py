import src.persistence

def clear_v1():
    '''Resets the internal data of the application to its initial state

    Arguments:
        N/A

    Exceptions:
        N/A

    Return Value:
        Returns {}
    '''
    store = src.persistence.get_pickle()

    store = {
        'users': {-1: 
            {
                'u_id': None,
                'email': None,
                'name_first': None,
                'name_last': None,
                'handle_str': None,
                'password': None,
                'perm_id': None,
                'valid_tokens': [],
                'profile_img_url': None,
                'notifications': [
                    {
                    'channel_id': None,
                    'dm_id': None,
                    'notification_message': None,
                    }
                ],
            }
        },
        'channels': {-1:
            {
                'channel_id': None,
                'name': None,
                'owner_ids': [],
                'member_ids': [],
                'is_public': None,
                'message_ids': [],
                'standup': {
                    'is_active': False,
                    'time_finish': None,
                    'queue': [],
                },
            }
        },
        'dms': {-1:
            {
                'dm_id': None,
                'name': None,
                'creator_id': None,
                'member_ids': [], 
                'message_ids': [],
            }
        },
        'removed_users': {-1:
            {
                'u_id': None,
                'email': None,
                'name_first': None,
                'name_last': None,
                'handle_str': None,
                'profile_img_url': None,
            }
        },
        'messages': {-1:
            {
                'message_id': None,
                'u_id': None,
                'shared_message_length': None,
                'message': None,
                'time_sent': None,
                'reacts': {-1:
                    {
                        'react_id': None,
                        'u_ids': [],
                        'is_this_user_reacted': None,
                    }
                },
                'is_pinned': None,
            },
        },
        'id': -1,
    }

    src.persistence.set_pickle(store)

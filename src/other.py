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

    
    store['users'] = {-1: 
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
    }
    store['channels'] = {-1:
        {
            'channel_id': None,
            'name': None,
            'owner_ids': [],
            'member_ids': [],
            'is_public': None,
            'message_ids': [],
        }
    }
    store['dms'] = {-1:
        {
            'dm_id': None,
            'name': None,
            'creator_id': None,
            'member_ids': [], 
            'message_ids': [],
        }
    }
    store['removed_users'] = {-1:
        {
            'u_id': None,
            'email': None,
            'name_first': None,
            'name_last': None,
            'handle_str': None,
            'profile_img_url': None,
        }
    }
    store['messages'] = {-1:
        {
            'message_id': None,
            'u_id': None,
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
    }
    store['id'] = -1

    src.persistence.set_pickle(store)

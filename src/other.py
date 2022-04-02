from src.data_store import data_store

def clear_v1():
    '''Resets the internal data of the application to its initial state

    Arguments:
        N/A

    Exceptions:
        N/A

    Return Value:
        Returns {}
    '''
    store = data_store.get()
    store['users'] = {None: 
        {
            'email': None,
            'name_first': None,
            'name_last': None,
            'handle_str': None,
            'password': None,
            'perm_id': None,
            'valid_tokens': [],
        }
    }
    store['channels'] = {None:
        {
            'name': None,
            'owner_members': {None:
                {
                    'email': None,
                    'name_first': None,
                    'name_last': None,
                    'handle_str': None,
                }
            },
            'all_members': {None:
                {
                    'email': None,
                    'name_first': None,
                    'name_last': None,
                    'handle_str': None,
                }
            },
            'is_public': None,
        }
    }
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
    }
    store['removed_users'] = {None:
        {
            'u_id': None,
            'email': None,
            'name_first': None,
            'name_last': None,
            'handle_str': None,
        }
    }
    store['channel_messages'] = {None:
        {
            'channel_id': None,
            'u_id': None,
            'message': None,
            'time_sent': None,
        },
    }
    store['dm_messages'] = {None:
        {
            'dm_id': None,
            'u_id': None,
            'message': None,
            'time_sent': None,
        },
    }
    store['u_id'] = -1
    store['channel_id'] = -1
    store['dm_id'] = -1
    store['message_id'] = -1

    data_store.set(store)

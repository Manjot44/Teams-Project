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
    store['users'] = [
        {
            'u_id': None,
            'email': None,
            'name_first': None,
            'name_last': None,
            'handle_str': None,
            'password': None,
            'perm_id': None,
            'valid_tokens': []
        }
    ]
    store['channels'] = [
        {
            'channel_id': None,
            'name': None,
            'owner_members': [
                {
                    'u_id': None,
                    'email': None,
                    'name_first': None,
                    'name_last': None,
                    'handle_str': None,
                    'perm_id': None,
                }
            ],
            'all_members': [
                {
                    'u_id': None,
                    'email': None,
                    'name_first': None,
                    'name_last': None,
                    'handle_str': None,
                    'perm_id': None,
                }
            ],
            'is_public': None,
            'messages': [
                {
                    'message_id': None,
                    'u_id': None,
                    'message': None,
                    'time_sent': None,
                },
            ]
        }  
    ]

    data_store.set(store)

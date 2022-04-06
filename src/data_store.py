'''
data_store.py

This contains a definition for a Datastore class which you should use to store your data.
You don't need to understand how it works at this point, just how to use it :)

The data_store variable is global, meaning that so long as you import it into any
python file in src, you can access its contents.

Example usage:

    from data_store import data_store

    store = data_store.get()
    print(store) # Prints { 'names': ['Nick', 'Emily', 'Hayden', 'Rob'] }

    names = store['names']

    names.remove('Rob')
    names.append('Jake')
    names.sort()

    print(store) # Prints { 'names': ['Emily', 'Hayden', 'Jake', 'Nick'] }
    data_store.set(store)
'''

# YOU SHOULD MODIFY THIS OBJECT BELOW
initial_object = {
    'users': {None: 
        {
            'u_id': None,
            'email': None,
            'name_first': None,
            'name_last': None,
            'handle_str': None,
            'password': None,
            'perm_id': None,
            'valid_tokens': [],
        }
    },
    'channels': {None:
        {
            'channel_id': None,
            'name': None,
            'owner_members': {None:
                {
                    'u_id': None,
                    'email': None,
                    'name_first': None,
                    'name_last': None,
                    'handle_str': None,
                }
            },
            'all_members': {None:
                {
                    'u_id': None,
                    'email': None,
                    'name_first': None,
                    'name_last': None,
                    'handle_str': None,
                }
            },
            'is_public': None,
        }
    },
    'dms': {None:
        {
            'dm_id': None,
            'name': None,
            'creator_id': None,
            'all_members': {None:
                {
                    'u_id': None,
                    'email': None,
                    'name_first': None,
                    'name_last': None,
                    'handle_str': None,
                }
            }, 
        }
    },
    'removed_users': {None:
        {
            'u_id': None,
            'email': None,
            'name_first': None,
            'name_last': None,
            'handle_str': None,
        }
    },
    'channel_messages': {None:
        {
            'message_id': None,
            'channel_id': None,
            'u_id': None,
            'message': None,
            'time_sent': None,
        },
    },
    'dm_messages': {None:
        {
            'message_id': None,
            'dm_id': None,
            'u_id': None,
            'message': None,
            'time_sent': None,
        },
    },
    'u_id': -1,
    'channel_id': -1,
    'dm_id': -1,
    'message_id': -1,
}

# YOU SHOULD MODIFY THIS OBJECT ABOVE

# YOU ARE ALLOWED TO CHANGE THE BELOW IF YOU WISH


class Datastore:
    def __init__(self):
        self.__store = initial_object

    def get(self):
        return self.__store

    def set(self, store):
        if not isinstance(store, dict):
            raise TypeError('store must be of type dictionary')
        self.__store = store


global data_store
data_store = Datastore()

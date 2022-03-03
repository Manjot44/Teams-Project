from data_store import data_store


def channels_list_v1(auth_user_id):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

def channels_listall_v1(auth_user_id):
    listall = {
        'channels': []
    }
    store = data_store.get()
    stored_channel_list = store['channels']
    for channel in stored_channel_list:
        listall['channels'].append(channel)
    
    return listall

    '''
    return 
    {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel 1',
                'members' = [],
                'ispublic' = True,
        	},
            {
                'channel_id': 2,
        		'name': 'My Channel 2',
            },
        ],
    }
    '''


def channels_create_v1(auth_user_id, name, is_public):
    return {
        'channel_id': 1,
    }

if __name__ == '__main__':
    
    list_all = channels_listall_v1(0)
    print(list_all)
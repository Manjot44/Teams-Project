from src import data_store


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
    # dictionary that is to be returned by function
    listall = {
        'channels': []
    }

    # validate auth user id
    saved_data = data_store.get()
    valid_user = False
    for user in saved_data['users']['u_id']:
        if auth_user_id == user:
            valid_user = True
    if valid_user == False:
        raise error.AccessError()
          

    # getting current channel data from src/data_store 
    saved_channels = saved_data['channels']

    # copying channels to 'listall' dict from saved channel data
    for channel in saved_channels:
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
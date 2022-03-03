if __name__ == '__main__':
    from error import InputError
    from data_store import data_store
else:
    from src.error import InputError
    from src.data_store import data_store

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
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

def channels_create_v1(auth_user_id, name, is_public):
    #Assessing for exception
    namelen = len(name)
    if namelen < 1 or namelen > 20:
        raise InputError(f"Name must be between 1 and 20 characters long")
    
    #Assigning variable to check if this is the first channel created
    initialchannel = False

    #Getting Data from data storage file
    store = data_store.get()

    #Creates list of all channels if it does not already exist
    if "channels" not in store:
        nc = {      
        }
        nc["channel_id"] = 1
        store["channels"] = [nc]
        initialchannel = True
    
    #Creating new channel ID and adding to the channels list
    channel_id = 1
    i = 0
    while True:
        if initialchannel == True:
            break
        if i == len(store["channels"]):
            nnc = {
            }
            nnc["channel_id"] = channel_id
            store["channels"].append(nnc)
            break
        channel_id += 1
        i += 1
    
    #Assigning variable to newly created channel
    current_channel = store["channels"][i]

    #Assigning user inputs
    current_channel["channel_id"] = channel_id
    current_channel["members"] = [auth_user_id]
    current_channel["name"] = name
    current_channel["ispublic"] = is_public

    #Saving to datastore
    data_store.set(store)

    #Testing
    print(current_channel)
    return channel_id


if __name__ == '__main__':
    channels_create_v1("abcdefgh", "test-channel-1", False)
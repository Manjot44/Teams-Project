if __name__ == '__main__':
    from error import InputError
    from data_store import data_store
else:
    from src.error import InputError
    from src.data_store import data_store

def channels_list_v1(auth_user_id):
    #Getting Data from data storage file
    store = data_store.get()

    #Creating empty list for the channels the user is part of
    channels = []
    no_channels = len(store["channels"])
    i = 0

    #Looping through all channels and adding the channels that the user is part of to "channels"
    while i != no_channels:
        j = 0
        no_members = len(store["channels"][i]["members"])
        while j != no_members:
            if auth_user_id == store["channels"][i]["members"][j]:
                channels.append(store["channels"][i])
            j += 1
        i += 1
    return channels

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

    #Creates the initial channel if channels list is empty
    if len(store["channels"]) == 0:
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

    return channel_id


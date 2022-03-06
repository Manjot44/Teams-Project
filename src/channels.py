if __name__ == '__main__':
    from error import InputError, AccessError
    from data_store import data_store

else:
    from src.error import InputError, AccessError
    from src.data_store import data_store

def channels_list_v1(auth_user_id):
    #Getting Data from data storage file
    store = data_store.get()

    #Assessing for Access Error
    valid_user = False
    for user in store["users"]:
        if user["u_id"] == auth_user_id:
            valid_user = True
    if valid_user == False:
        raise AccessError("User ID must be registered")

    #Creating empty list for the channels the user is part of
    channels_list = []

    #Looping through all channels and adding the channels that the user is part of to "channels_list"
    for idx1, channel in enumerate(store["channels"]):
        for member in store["channels"][idx1]["members"]:
            if auth_user_id == member:
                channels_list.append(store["channels"][idx1])

    fixstore = {
        "channels": channels_list
    }
    return fixstore

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
    #Getting Data from data storage file
    store = data_store.get()

    #Assessing for exception
    namelen = len(name)
    if namelen < 1 or namelen > 20:
        raise InputError(f"Name must be between 1 and 20 characters long")
    valid_user = False
    for user in store["users"]:
        if user["u_id"] == auth_user_id:
            valid_user = True
    if valid_user == False:
        raise AccessError("User ID must be registered")

    #Creates and adds the new channel to the channels list
    channel_id = len(store["channels"]) + 1
    nc = {}
    nc["channel_id"] = channel_id
    store["channels"].append(nc)

    #Assigning variable to newly created channel
    current_channel = store["channels"][channel_id - 1]

    #Assigning user inputs
    current_channel["channel_id"] = channel_id
    current_channel["members"] = [auth_user_id]
    current_channel["name"] = name
    current_channel["ispublic"] = is_public
    current_channel["messages"] = []

    #Saving to datastore
    data_store.set(store)

    return {
        'channel_id': channel_id,
    }


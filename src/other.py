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
    store['users'] = []
    store['channels'] = []
    data_store.set(store)

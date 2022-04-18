from src.data_store import data_store
import pickle

def set_pickle(store):
    '''Pickles the store dict in src/persist.p 

    Arguments:
        store (dict) - all stored data

    Exceptions:
        N/A

    Return Value:
        (void): no return
    '''
    data_store.set(store)
    with open("src/persist.p", 'wb') as new_pickle:
        pickle.dump(store, new_pickle)

def get_pickle():
    '''Unpickles the data in src/persist.p and returns it in store

    Arguments:
        N/A

    Exceptions:
        N/A

    Return Value:
        (dict): all stored data
    '''
    store = data_store.get()
    with open("src/persist.p", 'rb') as reading:
        store = pickle.load(reading)
    return store

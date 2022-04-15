from src.data_store import data_store
import pickle

def set_pickle(store):
    data_store.set(store)
    with open("src/persist.p", 'wb') as new_pickle:
        pickle.dump(store, new_pickle)

def get_pickle():
    store = data_store.get()
    with open("src/persist.p", 'rb') as reading:
        store = pickle.load(reading)
    return store

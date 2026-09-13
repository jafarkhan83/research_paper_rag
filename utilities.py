import pickle

def find_neighbors(child, children):
    neighbor_siblings = []
    for c in children:
        if c.metadata['parent'] == child.metadata['parent'] and (c.metadata['position'] == child.metadata['position'] - 1 or c.metadata['position'] == child.metadata['position'] + 1):
            neighbor_siblings.append(c)
    return neighbor_siblings

def serialize_object(obj, file_path):
    with open(file_path, 'wb') as f:
        pickle.dump(obj, f)

def deserialize_object(file_path):
    with open(file_path, 'rb') as f:
        return pickle.load(f)
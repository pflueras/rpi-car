import json

class StorageObject:
    def __init__(self, start_index, start_position, storage_object_type = 'object', end_index = -1, end_position = 0):
        self.storage_object_type = storage_object_type
        self.start_index = start_index
        self.start_position = start_position
        self.end_index = end_index
        self.end_position = end_position

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
import os
import json

class WatchedChannels:
    def __init__(self):
        self.filepath = 'bot/data/watched_channels.json'
        self.json_file = open(self.filepath, 'r+')
        if not os.stat(self.filepath).st_size:
            self._data = []
        else:
            self._data = json.load(self.json_file)
            self.json_file.truncate(0)
            self.json_file.close()

    
    def __del__(self):
        if not self.json_file.closed:
            # dumps = json.dumps(self._data)
            # self.json_file.write(dumps)
            self.json_file.close()
        print("destructor call")

    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, __channels):
        self._data = __channels
        print("value setted")
        # self._save()
    
    # def append(self, value):
    #     self.data = self.data + [value]
    #     print("value appended")
    #     self._save()
    
    def save(self):
        if self.json_file.closed:
            self.json_file = open(self.filepath, 'w+')
        json.dump(self.data, self.json_file)
        self.json_file.close()
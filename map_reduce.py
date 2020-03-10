import json


class MapReduce:
    def __init__(self, id):
        self.id = id
        self.key_values = dict()

    def map(self, key, value):
        if value not in self.key_values:
            temp_list = [key]
            self.key_values[value] = temp_list
        else:
            temp_list = self.key_values.get(value)
            if key not in temp_list:
                temp_list.append(key)
                self.key_values[value] = temp_list

    def reduce(self):
        print("[" + str(self.id) + "] > Running reducer")

    def store_values(self):
        file_name = "output/map-" + str(id) + ".json"
        with open(file_name, 'w+', encoding='utf-8') as outfile:
            json.dump(self.key_values, outfile, ensure_ascii=False, indent=4)
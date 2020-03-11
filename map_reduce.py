import json
import os


class MapReduce:
    def __init__(self, rank):
        self.id = rank
        self.key_values = dict()
        self.__create_directory("output/map/")
        self.__create_directory("output/reduce/")

    def map(self, key, value):
        if value not in self.key_values:
            temp_list = [key]
            self.key_values[value] = temp_list
        else:
            temp_list = self.key_values.get(value)
            if key not in temp_list:
                temp_list.append(key)
                self.key_values[value] = temp_list

    def reduce(self, key, value):
        file_name_raw = "output/reduce/" + key + ".txt"
        file_name = file_name_raw.replace('/', '_')
        file_name = file_name.replace('%', '')

        if os.path.exists(file_name):
            append_write = 'a'  # append if already exists
        else:
            append_write = 'w'  # make a new file if not

        with open(file_name, append_write, encoding='utf-8') as outfile:
            outfile.writelines(["%s\n" % item for item in value])

    def store_values(self):
        file_name = "output/map/map-" + str(self.id) + ".json"
        with open(file_name, 'w+', encoding='utf-8') as outfile:
            json.dump(self.key_values, outfile, ensure_ascii=False, indent=4)

    @staticmethod
    def __create_directory(path):
        if not os.path.exists(path):
            os.makedirs(path)
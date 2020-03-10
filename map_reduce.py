import json


class MapReduce:
    def __init__(self, id):
        self.worker_id = id

    def map(self):
        print("[" + self.worker_id + "] > Running mapper")
        file_name = 'output/adjacency_list.json'
        with open(file_name, 'r', encoding='utf-8') as infile:
            json_data = json.load(infile)

        json_urls = []
        keys = dict()

        for data in json_data:
            json_urls.append(data)

        for url in json_urls:
            for link in json_data[url]:
                if link not in keys:
                    temp_list = [url]
                    keys[link] = temp_list
                else:
                    temp_list = keys.get(link)
                    if url not in temp_list:
                        temp_list.append(url)
                        keys[link] = temp_list

        file_name = "output/map-" + id + ".json"
        with open(file_name, 'w+', encoding='utf-8') as outfile:
            json.dump(keys, outfile, ensure_ascii=False, indent=4)

    def reduce(self):
        print("[" + self.worker_id + "] > Running reducer")

import urllib.request
import urllib.parse
import urllib.robotparser
from bs4 import BeautifulSoup
import os
import time
import json
import pickle
from signal import signal, SIGINT
from sys import exit


urls_map = dict()


class Crawler:
    def __init__(self, urls, limit):
        self.urls = urls
        self.folder_name = "files"
        self.rp = urllib.robotparser.RobotFileParser()
        self.links_dict = {}
        self.limit = limit

    def crawl(self):
        print("Crawling:")

        try:
            file_name = self.folder_name + "/visited_urls.txt"
            with open(file_name, 'rb') as fp:
                items = pickle.load(fp)
                global urls_map
                urls_map = items

            print(urls_map)

        except FileNotFoundError:
            urls_map = dict()

        index = 0
        while len(self.urls) != 0 and index < self.limit:
            url = self.urls.pop(0)
            self.__crawl_url(url)
            index += 1

        # add urls to external file
        file_name = self.folder_name + "/visited_urls.txt"
        with open(file_name, 'wb') as fp:
            pickle.dump(urls_map, fp)

    def __crawl_url(self, url):
        print(" - " + url)

        hash_value = hash(url)
        urls_map[hash_value] = url

        try:
            req = urllib.request.Request(
                url,
                headers={
                    'User-Agent': 'TBD Crawler'
                }
            )
            page = urllib.request.urlopen(req)
        except urllib.error.HTTPError:
            print(" - HTTP Error")
            return
        except urllib.error.URLError:
            print(" - SSL Certificate Error")
            return

        soup = BeautifulSoup(page, 'html.parser')

        plain_text = soup.prettify()
        urls = []

        o = urllib.parse.urlparse(url)

        # define the name of the directory to be created
        scheme = o.scheme
        domain = o.netloc
        path = o.path

        self.robot_parse_read(scheme + "://" + domain)

        if not self.robot_parse_url(url):
            print(" - Cannot parse")
            return

        self.robot_parse_delay()

        path_only, resource = self.generate_sections_of_url(path)

        link = self.folder_name + "/" + domain + "/" + path_only
        self.create_directory(link)

        if not resource:
            resource = "index.html"

        file_name = self.folder_name + "/" + domain + "/" + path_only + resource
        with open(file_name, "w+", encoding="utf-8") as f:
            f.write(plain_text)

        links_list = []

        for a in soup.find_all('a', href=True):
            raw_url = a['href']
            l = urllib.parse.urlparse(raw_url)
            parsed_url = ""

            if not l.scheme:
                parsed_url = scheme + "://" + domain + l.path
            else:
                parsed_url = raw_url

            # verify if link is not already parsed
            if hash(parsed_url) not in urls_map:
                links_list.append(parsed_url)
                self.urls.append(parsed_url)
            else:
                print(" - link already parsed")

        self.links_dict[url] = links_list

    def map(self):
        print("Generate Map")

        self.create_directory("output")

        file_name = 'output/map.txt'
        with open(file_name, 'w+', encoding='utf-8') as outfile:
            json.dump(self.links_dict, outfile, ensure_ascii=False, indent=4)

    @staticmethod
    def reduce():
        print("Generate Reduce")

        file_name = 'output/map.txt'
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
                    temp_list = keys[link]
                    if url not in temp_list:
                        temp_list.append(url)
                        keys[link] = temp_list

        file_name = 'output/reduce.txt'
        with open(file_name, 'w+', encoding='utf-8') as outfile:
            json.dump(keys, outfile, ensure_ascii=False, indent=4)

    def robot_parse_read(self, link):
        self.rp.set_url(link + "/robots.txt")
        self.rp.read()

    def robot_parse_url(self, url):
        return self.rp.can_fetch("*", url)

    def robot_parse_delay(self):
        try:
            delay_time = self.rp.crawl_delay("*")
            time.sleep(float(delay_time))
        except AttributeError:
            time.sleep(1)

    @staticmethod
    def create_directory(path):
        if not os.path.exists(path):
            os.makedirs(path)

    @staticmethod
    def generate_sections_of_url(path):
        sections = []
        temp = ""
        while path != '/':
            temp = os.path.split(path)
            path = temp[0]
            sections.append(temp[1])

        path_only = ""
        resource = ""
        while len(sections):
            temp = sections.pop()
            if "." in temp:
                resource = temp
            else:
                path_only += temp + "/"

        return path_only, resource


def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Storing data and exiting!')

    # add urls to external file
    file_name = "files/visited_urls.txt"
    with open(file_name, 'wb') as fp:
        pickle.dump(urls_map, fp)

    exit(0)


def main():
    urls = ["https://dmoztools.net/", "https://dmoz-odp.org/"]
    limit = 5

    c = Crawler(urls, limit)
    #c.crawl()
    #c.map()
    c.reduce()


if __name__ == "__main__":
    signal(SIGINT, handler)
    main()

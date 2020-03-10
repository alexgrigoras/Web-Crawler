import json
import os
import pickle
import urllib.parse
import urllib.request

from bs4 import BeautifulSoup

from robot_parser import RobotParser


class Crawler:
    def __init__(self, urls, limit):
        self.urls = urls
        self.folder_name = "files"
        self.rp = RobotParser()
        self.links_dict = {}
        self.limit = limit
        self.urls_map = dict()

    def crawl(self):
        print("> Crawling:")

        try:
            file_name = self.folder_name + "/visited_urls.txt"
            with open(file_name, 'rb') as fp:
                items = pickle.load(fp)
                self.urls_map = items

        except FileNotFoundError:
            self.urls_map = dict()

        index = 0
        while len(self.urls) != 0 and index < self.limit:
            url = self.urls.pop(0)
            self.__crawl_url(url)
            index += 1

        # add urls to external file
        file_name = self.folder_name + "/visited_urls.txt"
        with open(file_name, 'wb') as fp:
            pickle.dump(self.urls_map, fp)

    def __crawl_url(self, url):
        print("\t- " + url)

        hash_value = hash(url)
        self.urls_map[hash_value] = url

        try:
            req = urllib.request.Request(
                url,
                headers={
                    'User-Agent': 'TBD Crawler'
                }
            )
            page = urllib.request.urlopen(req)
        except urllib.error.HTTPError:
            print("\t- HTTP Error")
            return
        except urllib.error.URLError:
            print("\t- SSL Certificate Error")
            return

        soup = BeautifulSoup(page, 'html.parser')

        plain_text = soup.prettify()
        urls = []

        o = urllib.parse.urlparse(url)

        # define the name of the directory to be created
        scheme = o.scheme
        domain = o.netloc
        path = o.path

        self.rp.robot_parse_read(scheme + "://" + domain)

        if not self.rp.robot_parse_url(url):
            print("\t- Cannot parse")
            return

        self.rp.robot_parse_delay()

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
            if hash(parsed_url) not in self.urls_map:
                links_list.append(parsed_url)
                self.urls.append(parsed_url)
            else:
                print("\t- link already parsed")

        self.links_dict[url] = links_list

    def generate_adjacency_list(self):
        print("> Generate Adjacency list")

        self.create_directory("output")

        file_name = 'output/adjacency_list.json'
        with open(file_name, 'w+', encoding='utf-8') as outfile:
            json.dump(self.links_dict, outfile, ensure_ascii=False, indent=4)

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

import urllib.request
import urllib.parse
import urllib.robotparser
from bs4 import BeautifulSoup
import os
import time
import json


class Crawler:
    def __init__(self, urls, limit):
        self.urls = urls
        self.folder_name = "files"
        self.rp = urllib.robotparser.RobotFileParser()
        self.links_dict = {}
        self.limit = limit

    def crawl(self):
        print("Crawling:")
        index = 0
        while len(self.urls) != 0 and index < self.limit:
            url = self.urls.pop(0)
            self.__crawl_url(url)
            index += 1

        self.create_directory("output")

        file_name = 'output/links.txt'
        with open(file_name, 'w+', encoding='utf-8') as outfile:
            json.dump(self.links_dict, outfile, ensure_ascii=False, indent=4)

    def __crawl_url(self, url):
        print(" - " + url)
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

            if parsed_url not in self.urls:
                links_list.append(parsed_url)
                self.urls.append(parsed_url)

        self.links_dict[url] = links_list

        # for i in urls:
        # print(i)

    def robot_parse_read(self, link):
        self.rp.set_url(link + "/robots.txt")
        self.rp.read()

    def robot_parse_url(self, url):
        return self.rp.can_fetch("*", url)

    def robot_parse_delay(self):
        delay_time = self.rp.crawl_delay("*")
        time.sleep(float(delay_time))

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


def main():
    urls = ["https://dmoztools.net/", "https://dmoz-odp.org/"]
    limit = 6

    c = Crawler(urls, limit)
    c.crawl()


if __name__ == "__main__":
    main()

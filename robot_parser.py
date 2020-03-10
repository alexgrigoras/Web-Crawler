import time
import urllib.robotparser


class RobotParser:
    def __init__(self):
        self.rp = urllib.robotparser.RobotFileParser()

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

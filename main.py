from crawler import Crawler


def main():
    urls = ["https://dmoztools.net/", "https://dmoz-odp.org/"]
    limit = 10

    c = Crawler(urls, limit)
    c.crawl()
    c.generate_adjacency_list()


if __name__ == "__main__":
    main()

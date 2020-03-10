from crawler import Crawler
import os

def main():
    urls = ["https://dmoztools.net/", "https://dmoz-odp.org/"]
    limit = 50
    nr_nodes = 12

    c = Crawler(urls, limit)
    c.crawl()
    c.generate_adjacency_list()
    os.system('mpiexec -np ' + str(nr_nodes) + ' python master_worker.py')

if __name__ == "__main__":
    main()

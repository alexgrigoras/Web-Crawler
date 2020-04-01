# Map-Reduce Web Crawler

## Description
Map Reduce Web Crawler application for the course Big Data Techniques

## Architecture
The main components of the application are:

1. <b>Information Gathering</b> - web crawler
    1. Web Crawler (crawler.py) -> inputs a queue and crawls the websites by storing the html resource and parsing all the links found in the pages
    1. Robot Parser (robot_parser.py) -> checks if the robot protocol allows to crawl that page 

1. <b>MapReduce</b> - parallel application using MPI
    1. Master -> sends the links to the workers to be processed in two phase: map and reduce
    1. Worker -> process the links and store the data to the file system
    
## Application structure
```
map-reduce-crawler
├── application
|   ├── files
|   ├── output
|   ├── modules
|   |   ├── __init__.py
|   |   ├── crawler.py
|   |   ├── map_reduce.py
|   |   ├── master_worker.py
|   |   └── robot_parser.py
|   ├── __init__.py
|   └── __main__.py
├── README.md
├── requirements.txt
└── setup.py
```

## Execution
It is done in two phases:

1. Cloning from the git: `git clone https://github.com/grigoras.alexandru/map-reduce-crawler.git`
1. Selecting the application folder: `cd map-reduce-crawler/`
1. Creating virtual environment: `virtualenv ENVIRONMENT_NAME`
1. Selecting virtual environment: `source ENVIRONMENT_NAME/bin/activate`
1. Installing: `python setup.py install`
1. Running:
    1. Crawler + MapReduce: `python -m application`
    1. <i>(Optional)</i> MapReduce: `mpiexec -np NUMBER_OF_PROCESSES python application/modules/master_worker.py`
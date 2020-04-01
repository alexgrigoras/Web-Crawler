from pip._internal.download import PipSession
from pip._internal.req import parse_requirements
from setuptools import setup, find_packages

requirements = [
    str(req.req) for req in parse_requirements('requirements.txt', session=PipSession())
]

setup(
    name="",
    version="1.0",
    author="Alexandru Grigoras",
    author_email="alexandru.grigoras@student.tuiasi.ro",
    description="Map Reduce Web Crawler application for the course Big Data Techniques",
    url="https://github.com/grigoras.alexandru/map-reduce-crawler",
    packages=find_packages(),
    keywords='map-reduce application',
    install_requires=requirements,
    zip_safe=True,
    classifiers=[
        'Development Status :: 1.0 - Development',
        "Programming Language :: Python :: 3.5",
        "Crawler :: Youtube API metadata",
        "MapReduce :: MapReduce model",
        "Operating System :: OS Independent"
    ]
)
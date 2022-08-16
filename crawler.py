import argparse
import logging
# from urllib import requests
import requests
from bs4 import BeautifulSoup
logger = None
def parse_args():
    parser = argparse.ArgumentParser(description="Web crawler")
    parser.add_argument(
        "-d", "--debug", help="Enable debug logging", bs4action="store_true")
    return parser.parse_args()
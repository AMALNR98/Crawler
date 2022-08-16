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

def main():
    # args = parse_args()
    # artist = get_artists_name()
    # songs = get_songs_name()
    # lyrics = get_lyrics()
    # if args.debug:
    #     configure_logging(logging.DEBUG)
    # else:
    #     configure_logging(logging.INFO)
    # logger.debug("Here's a debug message")
    # logger.info("Here's an info message!")
    # logger.warning("Here's an warning message!")
    # logger.critical("Here's an critical message!")
    # crawl()
if __name__ == "__main__":
    main()
# artist
# songs
# lyrics
import argparse
import logging
import os

# from urllib import requests
import requests
from bs4 import BeautifulSoup
logger = None


def parse_args():
    parser = argparse.ArgumentParser(description="Web crawler")
    parser.add_argument(
        "-d", "--debug", help="Enable debug logging", action="store_true")
    return parser.parse_args()


def get_artists_name(base):
    # args = parse_args()
    resp = requests.get("https://www.songlyrics.com/top-artists-lyrics.html")
    soup = BeautifulSoup(resp.content, "lxml")
    track_list = soup.find("table", attrs={"class": "tracklist"})
    track_link = track_list.find_all('h3')
    # print(track_link)
    if track_link:
        logger.debug("artist list parsed successfully")
    else:
        logger.debug("couldn't parse artist list")
    artists_name_and_links = {}

    for link in track_link[0:5]:

        # if link.find('img') not in link:

            # artist_name = link.text
            # print(artist_name)
        artists_name_and_links[link.text] = link.a['href']
        # logger.info("getting artist name")
            # artists_name_and_links[link.text]=link
            # print(link)
            # print("artist name:", link.text)
            # artists.append(link.text)
            # print(artists)

    # print(artists_name_and_links)
    return artists_name_and_links

def get_songs(artists_name):
     song_list = {}
     resp = requests.get(artists_name)
     soup = BeautifulSoup(resp.content,'lxml')
     songs = soup.find("table", attrs= {"class": "tracklist"})
     song_link = songs.find_all('a')
     for songs in song_link[0:5]:
        #print(songs.text)
        song_list[songs.text]= songs["href"]
        #  if songs.find('img') not in songs:
        #     song_list[]
     return song_list


def get_lyrics(lyrics):
    resp = requests.get("https://www.songlyrics.com/hillsong/oceans-where-feet-may-fail-lyrics/")
    soup = BeautifulSoup(resp.content, "lxml")
    # print(soup)
    lyrics = soup.find("p", attrs={"id": "songLyricsDiv"})
    # lyrics_link =  lyrics.find_all('a')
    # print(lyrics.text)
    # for line in lyrics:
    #     print(line)
    return lyrics.text


def configure_logging(level=logging.INFO):
    global logger
    logger = logging.getLogger("crawler")
    logger.setLevel(level)
    screen_handler = logging.StreamHandler()
    screen_handler.setLevel(level)
    formatter = logging.Formatter(
        "[%(levelname)s] : %(filename)s(%(lineno)d) : %(message)s")
    screen_handler.setFormatter(formatter)
    logger.addHandler(screen_handler)


def crawl(download_directory_path):
#     #     logger.debug("Crawling starting")
#     #     for i in range(10):
#     #         logger.debug("Fetching URL %s", i)
#     #         print("https://....")
#     #     logger.debug("Completed crawling")
#     # x= get_artists_name("http://www.songlyrics.com/top-artists-lyrics.html").items()
#     # print(x.items())
    for artist_name, artist_link in get_artists_name("http://www.songlyrics.com/top-artists-lyrics.html").items():
        artist_dir = os.path.join(download_directory_path, artist_name)
        os.makedirs(artist_dir, exist_ok=True)
        for song_name, song_link in get_songs(artist_link).items():
            # print(song_name)
            formatted_song_name = song_name.replace("/","-")
            file = open(f"{artist_dir}/{formatted_song_name}.txt",'w')
            file.write(get_lyrics(song_link))
            file.close()
            
        


def main():
    args = parse_args()
    # artist = get_artists_name()
    # songs = get_songs('https://www.songlyrics.com/hillsong-lyrics/')
    # print(songs)
    lyrics = get_lyrics('https://www.songlyrics.com/hillsong/oceans-where-feet-may-fail-lyrics/')
    # print(lyrics)

    # songs = get_songs_name()
    # lyrics = get_lyrics()
    if args.debug:
        configure_logging(logging.DEBUG)
    else:
        configure_logging(logging.INFO)
    # logger.debug("Here's a debug message")
    # logger.info("Here's an info message!")
    # logger.warning("Here's an warning message!")
    # logger.critical("Here's an critical message!")
    # crawl()
if __name__ == "__main__":
    main()
    crawl("/home/amalnr/Hamon/Crawler")
# artist
# songs
# lyrics

import argparse
import logging
import os

import requests
from bs4 import BeautifulSoup

import db
import web

logger = None
dbname = "lyrics"

def parse_args():
    parser = argparse.ArgumentParser(description="Web crawler")
    parser.add_argument("-d", "--debug", help="Enable debug logging", action="store_true")
    parser.add_argument("--download", help = "creates a directory for lyrics", action ="store")
    parser.add_argument("--db", help = "Name of the date base", action = "store", default ="lyrics" )
    subcommands = parser.add_subparsers(help= "commandsa", dest="command", required= True)
    subcommands.add_parser("initdb", help="Initializing the database")
    subcommands.add_parser("crawl", help = "Crawling")
    subcommands. add_parser("web", help = "start browser" )
    subcommands.add_parser("add_directory", help = "Create a directory to store lyrics")
    return parser.parse_args()


def get_artists_name(base):
    resp = requests.get("https://www.songlyrics.com/top-artists-lyrics.html")
    soup = BeautifulSoup(resp.content, "lxml")
    track_list = soup.find("table", attrs={"class": "tracklist"})
    track_link = track_list.find_all('h3')
    if track_link:
        logger.debug("artist list parsed successfully")
    else:
        logger.debug("couldn't parse artist list")
    artists_name_and_links = {}
    for link in track_link [:5]:
        artists_name_and_links[link.text] = link.a['href']
    logger.debug("artist name and link added to ditinoary")
    return artists_name_and_links

def get_songs(artists_name):
     song_list = {}
     resp = requests.get(artists_name)
     soup = BeautifulSoup(resp.content,'lxml')
     songs = soup.find("table", attrs= {"class": "tracklist"})
     song_link = songs.find_all('a')
     for songs in song_link [:5]:
        song_list[songs.text]= songs["href"]

     return song_list


def get_lyrics(lyrics):
    resp = requests.get(lyrics)
    soup = BeautifulSoup(resp.content, "lxml")
    lyrics = soup.find("p", attrs={"id": "songLyricsDiv"})
    # print(lyrics.text)
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
    for artist_name, artist_link in get_artists_name("http://www.songlyrics.com/top-artists-lyrics.html").items():
        artist_dir = os.path.join(download_directory_path, artist_name)
        os.makedirs(artist_dir, exist_ok=True)
        for song_name, song_link in get_songs(artist_link).items():
            formatted_song_name = song_name.replace("/","-")
            if formatted_song_name:
                logger.debug("song name: '%s'", formatted_song_name)
            else :
                logger.debug("song not found")
            logger.debug("creating folder with song name :'%s'",formatted_song_name)
            file = open(f"{artist_dir}/{formatted_song_name}.txt",'w')
            file.write(get_lyrics(song_link))
            logger.debug("downloading songs lyrics of '%s'",formatted_song_name)
            file.close()

def create_table(db_name):
    conn = db.get_connection(db_name)
    with conn.cursor() as cursor: 
        with open("init.sql") as f:
            sql = f.read()
            cursor.execute(sql)
        conn.commit()
        conn.close()          

def add_artists():
    for artist_name, artist_link in get_artists_name('http://www.songlyrics.com/top-artists-lyrics.html').items():
        last_id = db.add_artist(artist_name)
        for song_name, song_link in get_songs(artist_link).items():
            lyrics = get_lyrics(song_link)
            db.add_song(song_name, last_id,  lyrics)



def main():
    args = parse_args()
    if args.debug:
        configure_logging(logging.DEBUG)
    else:
        configure_logging(logging.INFO)
    if args.command == "initdb":
        logger.info("Initializing the database")
        create_table(args.db)
        logger.info("Database initialized")
    if args.command == "crawl":
        logger.info("Crawling")
        add_artists()
        logger.info("Crawling completed")
    if args.command == "add_directory":
        logger.info("Crawling to directory")
        crawl("artists")
    
    if args.command == "web":
        logger.info("web starting")
        web.app.run(port=5001,debug = True)    
if __name__ == "__main__":
    main()
# artist
# songs
# lyrics



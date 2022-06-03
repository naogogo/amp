#!/usr/bin/env python3

import argparse
import json
import logging

from flask import Flask, request

from album import *
from artist import *
from database import *
from song import *
from player import *

class Server(object):

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.database = Database()
        self.database.connect()
        self.listen_host = "127.0.0.1"
        self.listen_port = 5000
        self.mpd_host = "127.0.0.1"
        self.mpd_port = 6600
        self.data_from = None

    def insert_data(self):
        with open(self.data_from, "r") as f:
            data = json.load(f)

        self.database.insert_json(data)

    def create_tables(self):
        self.database.execute(Artist.create_query)
        self.database.execute(Album.create_query)
        self.database.execute(Song.create_query)

    def parse_args(self):
        parser = argparse.ArgumentParser(
            description="Start the API server"
        )

        parser.add_argument("--data-from", type=str)
        parser.add_argument("--listen-host", type=str)
        parser.add_argument("--listen-port", type=int)
        parser.add_argument("--mpd-host", type=str)
        parser.add_argument("--mpd-port", type=int)

        args = parser.parse_args()

        if "data_from" in args:
            self.data_from = args.data_from
        if "listen_host" in args:
            self.listen_host = args.listen_host
        if "listen_port" in args:
            self.listen_port = args.listen_port
        if "mpd_host" in args:
            self.mpd_host = args.mpd_host
        if "mpd_port" in args:
            self.mpd_port = args.mpd_port

    @property
    def data_from(self):
        return self._data_from

    @data_from.setter
    def data_from(self, data_from):
        self.logger.debug("Settings data source to `%s'", data_from)
        self._data_from = data_from

    @property
    def logger(self):
        return self._logger

    @logger.setter
    def logger(self, logger):
        self._logger = logger

    @property
    def listen_host(self):
        return self._listen_host

    @listen_host.setter
    def listen_host(self, listen_host):
        self.logger.debug("Setting listen_host to `%s'", listen_host)
        self._listen_host = listen_host

    @property
    def database(self):
        return self._database

    @database.setter
    def database(self, database):
        self._database = database

    @property
    def listen_port(self):
      return self._listen_port

    @listen_port.setter
    def listen_port(self, listen_port):
        self.logger.debug("Setting listen_port to `%d'", listen_port)
        self._listen_port = listen_port

    @property
    def mpd_host(self):
        return self._mpd_host

    @mpd_host.setter
    def mpd_host(self, mpd_host):
        self.logger.debug("Setting mpd_host to `%s'", mpd_host)
        self._mpd_host = mpd_host

    @property
    def mpd_port(self):
        return self._mpd_port

    @mpd_port.setter
    def mpd_port(self, mpd_port):
        self.logger.debug("Setting mpd_port to `%d'", mpd_port)
        self._mpd_port = mpd_port

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>hello</p>"

@app.route("/play", methods=["POST"])
def play():
    d = Database()
    d.connect()
    cursor = d.cursor()

    p = Player("172.28.192.1")

    try:
        artists = json.loads(request.form["artists"])
    except KeyError:
        artists = []
    try:
        albums = json.loads(request.form["albums"])
    except KeyError:
        albums = []
    try:
        songs = json.loads(request.form["songs"])
    except KeyError:
        songs = []

    print(albums)

    p.play(cursor, [albums])
    cursor.close()
    d.close()
    return json.dumps({"status": "OK"})


@app.route("/search", methods=["POST"])
def search():
    d = Database()
    d.connect()

    album_list = AlbumList()
    artist_list = ArtistList()
    song_list = SongList()

    # TODO: need to split the other components
    query = " ".join(request.json["query"])

    cur = d.cursor()

    album_list.find(cur, query)
    artist_list.find(cur, query)
    song_list.find(cur, query)

    cur.close()

    data = {
        "albums": [],
        "artists": [],
        "songs": [],
    }

    for album in album_list.albums:
        data["albums"].append(album.to_dict())

    for artist in artist_list.artists:
        data["artists"].append(artist.to_dict())

    for song in song_list.songs:
        data["songs"].append(song.to_dict())

    return json.dumps(data)

@app.teardown_appcontext
def close_server(error):
    pass

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    server = Server()
    server.create_tables()
    server.parse_args()

    if server.data_from:
        server.insert_data()

    app.run(
        host=server.listen_host,
        port=server.listen_port
    )

#!/usr/bin/env python3

import json

from flask import Flask, request

from album import *
from artist import *
from database import *
from song import *

app = Flask(__name__)
db = Database()

@app.route("/")
def hello_world():
    return "<p>hello</p>"

@app.route("/search", methods=["POST"])
def search():
    album_list = AlbumList()
    artist_list = ArtistList()
    song_list = SongList()

    query = request.form["query"]
    print("query " + query)

    cur = db._con.cursor()

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

if __name__ == "__main__":
    db.connect()
    db.testdata("songs.json")

    app.run()
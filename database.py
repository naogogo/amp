#!/usr/bin/env python3

import json
import pykakasi
import sqlite3

from album import Album, AlbumList
from artist import Artist, ArtistList
from song import Song, SongList

kks = pykakasi.kakasi()

class Database(object):

    def __init__(self, path="file::memory:?cache=shared", uri=True):
        self.path = path
        self.connection = None

    def connect(self):
        self.connection = sqlite3.connect(self.path)

    def execute(self, query, params=()):
        cursor = self.cursor()
        result = cursor.execute(query, params).fetchall()
        cursor.close()
        return result

    def cursor(self):
        return self.connection.cursor()

    def close(self):
        if self.connection:
            self.connection.close()

    def kakasi(self,s):
        res = ""
        rows = kks.convert(s)
        for row in rows:
            res += row["hepburn"]
        return res

    def testdata(self, path):
        cur = self.cursor()

        with open(path, "r") as f:
            data = json.load(f)

        albums = []
        artists = []
        songs = []

        al = ArtistList()
        al.from_json(self.connection, data)

        ab = AlbumList()
        ab.from_json(self.connection, data)

        sl = SongList()
        sl.from_json(self.connection, data)

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path):
        self._path = path

    @property
    def connection(self):
        return self._connection

    @connection.setter
    def connection(self, connection):
        self._connection = connection

#!/usr/bin/env python3

import json
import pykakasi
import sqlite3

from album import Album
from artist import Artist
from song import Song

kks = pykakasi.kakasi()

class Database(object):

    def __init__(self, path=":memory:"):
        self.path = path

        self._con = None

    def connect(self):
        self._con = sqlite3.connect(self.path, check_same_thread=False)

    def execute(self, query, params=()):
        cursor = self.cursor()
        result = cursor.execute(query, params).fetchall()
        cursor.close()
        return result

    def cursor(self):
        return self._con.cursor()

    def close(self):
        if self._con:
            self._con.close()

    def kakasi(self,s):
        res = ""
        rows = kks.convert(s)
        for row in rows:
            res += row["hepburn"]
        return res

    def testdata(self, path):
        cur = self._con.cursor()

        with open(path, "r") as f:
            data = json.load(f)

        albums = []
        artists = []
        songs = []


        album_insert_query = """
        INSERT INTO albums (
                title,
                title_s,
                artist,
                date,
                disc
        ) VALUES (
                ?,
                ?,
                ?,
                ?,
                ?
        );
        """

        artist_insert_query = """
        INSERT INTO artists (
                title,
                title_s
        ) VALUES (
                ?,
                ?
        );
        """

        song_insert_query = """
        INSERT INTO songs (
                file,
                last_modified,
                format,
                album,
                artist,
                title,
                title_s,
                track,
                time,
                duration
        ) VALUES (
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?
        )
        """



        cur.execute("BEGIN TRANSACTION;")

        for row in data:
            artist = Artist()
            artist.title = row["artist"]
            try:
                artist.title_s = self.kakasi(row["artist"])
            except:
                artist.title_s = ""

            if not artist in artists:
                artists.append(artist)
                cur.execute(artist_insert_query, (
                    artist.title,
                    artist.title_s
                ))

            if "albumartist" in row:
                albumartist = Artist()
                albumartist.title = row["albumartist"]
                try:
                    albumartist.title_s = self.kakasi(row["artist"])
                except:
                    albumartist.title_s = ""

                if not albumartist in artists:
                    artists.append(albumartist)
                    cur.execute(artist_insert_query, (
                        albumartist.title,
                        albumartist.title_s
                    ))

        cur.execute("COMMIT;")
        cur.execute("BEGIN TRANSACTION;")

        for row in data:
            album = Album()
            album.from_json(cur, row)
            try:
                album.title_s = self.kakasi(row["album"])
            except:
                album.title_s = ""

            if album in albums:
                continue

            albums.append(album)
            cur.execute(album_insert_query, (
                album.title,
                album.title_s,
                album.artist.id,
                album.date,
                album.disc,
            ))

        cur.execute("COMMIT;")
        cur.execute("BEGIN TRANSACTION;")

        for row in data:
            song = Song()
            song.from_json(cur, row)
            try:
                song.title_s = self.kakasi(row["title"])
            except:
                song.title_s = ""

            if not song in songs:
                songs.append(song)
                cur.execute(song_insert_query, (
                    song.file,
                    song.last_modified,
                    song.format,
                    song.album.id,
                    song.artist.id,
                    song.title,
                    song.title_s,
                    song.track,
                    song.time,
                    song.duration
                ))

        cur.execute("COMMIT;")
        cur.close()

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

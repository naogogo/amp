#!/usr/bin/env python3

from album import Album
from artist import Artist

class SongList(object):

        DB_FIND_SELECT_QUERY = """
SELECT id FROM songs
"""

        def __init__(self):
                self.songs = []

        def like(self, what):
                return "%%{0}%%".format(what)

        def where(self, where):
                i = 0
                query = ""
                ss = where.strip().split()
                for s in ss:
                        if i > 0:
                                query += "AND "
                        else:
                                query += "WHERE "
                        query += "(title LIKE ? OR title_s LIKE ?)"
                        i += 1
                return query

        def where_params(self, where):
                params = ()
                ss = where.strip().split()
                for s in ss:
                        params += (self.like(s), self.like(s))
                return params

        def find(self, con, title):
                songs = []
                res = con.execute(self.DB_FIND_SELECT_QUERY + self.where(title), self.where_params(title)).fetchall()
                for row in res:
                        song = Song()
                        song.from_db_by_id(con, row[0])
                        songs.append(song)

                self.songs = songs

        @property
        def songs(self):
                return self._songs

        @songs.setter
        def songs(self, songs):
                self._songs = songs

class Song(object):

        create_query = """
CREATE TABLE IF NOT EXISTS songs (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        file            TEXT,
        last_modified   TEXT,
        format          TEXT,
        album           INTEGER,
        artist          INTEGER,
        title           TEXT,
        title_s         TEXT,
        track           INTEGER,
        time            INTEGER,
        duration        REAL
);
"""

        DB_ID_SELECT_QUERY = """
SELECT * FROM songs WHERE id = ?
"""

        def __init__(self):
                pass

        def from_db_by_id(self, con, id):
                res = con.execute(self.DB_ID_SELECT_QUERY, (id, )).fetchall()
                if len(res) != 1:
                        return False

                row = res[0]

                album = Album()
                if not album.from_db_by_id(con, row[4]):
                        return False
                artist = Artist()
                if not artist.from_db_by_id(con, row[5]):
                        return False


                self.id = row[0]
                self.file = row[1]
                self.last_modified = row[2]
                self.format = row[3]
                self.album = album
                self.artist = artist
                self.title = row[6]
                self.title_s = row[7]
                self.track = row[8]
                self.time = row[9]
                self.duration = row[10]

                return True

        def from_json(self, con, data):
                self.file = data["file"]
                self.last_modified = data["last-modified"]
                self.format = data["format"]
                self.title = data["title"]
                self.track = data["track"]
                self.time = data["time"]
                self.duration = data["duration"]

                album = Album()
                artist = Artist()

                try:
                        albumartist = data["albumartist"]
                except KeyError:
                        albumartist = data["artist"]

                try:
                        disc = int(data["disc"])
                except KeyError:
                        disc = 0

                if not artist.from_db_by_title(con, data["artist"]):
                        print("artist from_db_by_title")
                        return False

                if not album.from_db_by_title(con, albumartist, data["album"], int(data["date"]), disc):
                        print("album from_db_by_title: {0} {1} {2} {3}".format(albumartist, data["album"], data["date"], disc))
                        return False

                self.album = album
                self.artist = artist

                return True

        def to_dict(self):
            return {
                "file": self.file,
                "last_modified": self.last_modified,
                "format": self.format,
                "title": self.title,
                "track": self.track,
                "time": self.time,
                "duration": self.duration,
                "album": self.album.to_dict(),
                "artist": self.artist.to_dict(),
            }

        @property
        def file(self):
                return self._file

        @file.setter
        def file(self, file):
                self._file = file

        @property
        def last_modified(self):
                return self._last_modified

        @last_modified.setter
        def last_modified(self, last_modified):
                self._last_modified = last_modified

        @property
        def format(self):
                return self._format

        @format.setter
        def format(self, format):
                self._format = format

        @property
        def album(self):
                return self._album

        @album.setter
        def album(self, album):
                if album and not isinstance(album, Album):
                        raise Exception("not isinstance Album")

                self._album = album

        @property
        def artist(self):
                return self._artist

        @artist.setter
        def artist(self, artist):
                if artist and not isinstance(artist, Artist):
                        raise Exception("not isinstance Artist")

                self._artist = artist

        @property
        def title(self):
                return self._title

        @title.setter
        def title(self, title):
                self._title = title

        @property
        def title_s(self):
                return self._title_s

        @title_s.setter
        def title_s(self, title_s):
                self._title_s = title_s

        @property
        def track(self):
                return self._track

        @track.setter
        def track(self, track):
                self._track = int(track)

        @property
        def time(self):
                return self._time

        @time.setter
        def time(self, time):
                self._time = int(time)

        @property
        def duration(self):
                return self._duration

        @duration.setter
        def duration(self, duration):
                self._duration = float(duration)


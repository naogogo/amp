#!/usr/bin/env python3

from song import Song

import pykakasi

class SongList(object):

    DB_FIND_SELECT_QUERY = """
        SELECT id FROM songs
    """

    def __init__(self):
        self.songs = []
        self._kakasi = pykakasi.kakasi()

    # TODO: remove
    def kakasi(self,s):
        res = ""
        rows = self._kakasi.convert(s)
        for row in rows:
            res += row["hepburn"]
        return res

    def from_json(self, connection, data):
        cursor = connection.cursor()

        cursor.execute("BEGIN TRANSACTION;")

        for row in data:
            song = Song()
            song.from_json(cursor, row)
            try:
                song.title_s = self.kakasi(row["title"])
            except:
                song.title_s = ""

            if not song in self.songs:
                self.songs.append(song)
                song.to_database(cursor)

        cursor.execute("COMMIT;")
        cursor.close()

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
            w = "%%{0}%%".format(s)
            params += (w, w)
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


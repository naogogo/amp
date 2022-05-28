#!/usr/bin/env python3

from album import Album

import pykakasi

class AlbumList(object):

    DB_FIND_SELECT_QUERY = """
        SELECT id FROM albums
    """

    def __init__(self):
        self.albums = []
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
            album = Album()
            album.from_json(cursor, row)
            try:
                album.title_s = self.kakasi(row["album"])
            except:
                album.title_s = ""

            if album in self.albums:
                continue

            self.albums.append(album)
            album.to_database(cursor)

        cursor.execute("COMMIT;")
        cursor.close()

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
            query += "(title LIKE ? OR title_s LIKE ?) "
            i += 1
        return query

    def where_params(self, where):
        params = ()
        ss = where.strip().split()
        for s in ss:
            params += (self.like(s), self.like(s))
        return params


    def find(self, con, title):
        albums = []

        res = con.execute(self.DB_FIND_SELECT_QUERY + self.where(title), self.where_params(title)).fetchall()
        for row in res:
            album = Album()
            album.from_db_by_id(con, row[0])
            albums.append(album)

        self.albums = albums

    @property
    def albums(self):
        return self._albums

    @albums.setter
    def albums(self, albums):
        self._albums = albums

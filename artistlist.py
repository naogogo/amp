#!/usr/bin/env python3

from artist import Artist

import pykakasi

class ArtistList(object):

    DB_FIND_SELECT_QUERY = """
        SELECT id FROM artists
    """

    def __init__(self):
        self.artists = []
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
            artist = self.artist_from_json(row["artist"])
            if not artist in self.artists:
                self.artists.append(artist)
                artist.to_database(cursor)

            if "albumartist" in row:
                albumartist = self.artist_from_json(row["albumartist"])
                if not albumartist in self.artists:
                    self.artists.append(albumartist)
                    albumartist.to_database(cursor)

        cursor.execute("COMMIT;")
        cursor.close()

    def artist_from_json(self, title):
        artist = Artist()
        artist.title = title
        try:
            artist.title_s = self.kakasi(title)
        except:
            artist.title_s = ""
        return artist

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
        artists = []
        res = con.execute(self.DB_FIND_SELECT_QUERY + self.where(title), self.where_params(title)).fetchall()
        for row in res:
            artist = Artist()
            artist.from_db_by_id(con, row[0])
            artists.append(artist)

        self.artists = artists

    @property
    def artists(self):
        return self._artists

    @artists.setter
    def artists(self, artists):
        self._artists = artists

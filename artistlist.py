#!/usr/bin/env python3

from artist import Artist
from language import Language

import logging

class ArtistList(object):

    DB_FIND_SELECT_QUERY = """
        SELECT id FROM artists
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.artists = []
        self.language = Language()

    def from_json(self, connection, data):
        counter = 0
        cursor = connection.cursor()
        cursor.execute("BEGIN TRANSACTION;")

        for row in data:
            counter += 1
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
        self.logger.info("Processed %d entries, added %d artists", counter, len(self.artists))

    def artist_from_json(self, title):
        artist = Artist()
        artist.title = title
        artist.title_s = self.language.convert(title)
        return artist

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
            w = "%%{0}%%".format(s)
            params += (w, w)
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

    @property
    def logger(self):
        return self._logger

    @logger.setter
    def logger(self, logger):
        self._logger = logger

    @property
    def language(self):
        return self._language

    @language.setter
    def language(self, language):
        self._language = language
